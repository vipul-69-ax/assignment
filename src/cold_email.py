import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyPDF2 import PdfReader
import re

def extract_details_from_pdf(file_path):
    details = []
    reader = PdfReader(file_path)
    for page in reader.pages:
        text = page.extract_text()
        matches = re.findall(r"\d+\s+([^@\s]+\s[^@\s]+)\s+([^\s]+@[^\s]+)\s+([^\n]+?)\s{2,}([^\n]+)", text)
        for match in matches:
            details.append({
                "name": match[0],
                "email": match[1],
                "title": match[2].strip(),
                "company": match[3].strip()
            })
    return details

# Function to send an email
def send_email(to_email, subject, body, from_email, from_password):
    try:
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

if __name__ == "__main__":
    pdf_path = "/home/hp/Desktop/scripts/files/hr.pdf"
    extracted_details = extract_details_from_pdf(pdf_path)

    your_email = "your_email@gmail.com"
    your_password = "your_password" # Use app password

    # Email content
    email_subject = "Application for Internship"
    email_body_template = """Dear {name},

I hope this message finds you well. I am writing to express my interest in an internship opportunity at {company}. With my skills and enthusiasm, I am eager to contribute to your team and learn from the experience.

Thank you for considering my application. I look forward to the opportunity to discuss how I can be an asset to your company.

Best regards,
Your Name
"""
    print(len(extracted_details))
    for detail in extracted_details:
        email_body = email_body_template.format(name=detail['name'], company=detail['company'])
        print(email_body)
        # send_email(detail['email'], email_subject, email_body, your_email, your_password)
