from flask import Flask, jsonify, render_template, render_template_string
import subprocess
import pymongo

app = Flask(__name__)

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_trends"]
collection = db["trending_topics"]

@app.route("/")
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twitter Trends</title>
    <script>
        async function runScript() {
            const response = await fetch('/run_script');
            const data = await response.json();

            document.getElementById('result').innerHTML = `
                <p>These are the most happening topics as on ${new Date(data.date_time)}:</p>
                <ul>
                    <li>${data.trend1}</li>
                    <li>${data.trend2}</li>
                    <li>${data.trend3}</li>
                    <li>${data.trend4}</li>
                    <li>${data.trend5}</li>
                </ul>
                <p>The IP address used for this query was ${data.ip_address}.</p>
                <pre>${JSON.stringify(data, null, 2)}</pre>
            `;
        }
    </script>
</head>
<body>
    <button onclick="runScript()">Click here to run the script</button>
    <div id="result"></div>
</body>
</html>

                                  ''')

@app.route("/run_script")
def run_script():
    # Run the Selenium script
    subprocess.run(["python", "selenium_scraper.py"])
    
    # Fetch the latest record from MongoDB
    latest_record = collection.find_one(sort=[("date_time", pymongo.DESCENDING)])
    return jsonify(latest_record)

if __name__ == "__main__":
    app.run(debug=True)
