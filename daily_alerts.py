import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

def find_part_time_jobs(job_title, location):
    job_title = job_title.replace(" ", "+")
    location = location.replace(" ", "+")
    url = f"https://ca.indeed.com/jobs?q={job_title}&l={location}&jt=parttime"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("a", class_="tapItem")

    results = []
    for job in jobs[:10]:
        title = job.find("h2").text.strip()
        company = job.find("span", class_="companyName")
        link = "https://ca.indeed.com" + job['href']
        results.append({
            "title": title,
            "company": company.text.strip() if company else "N/A",
            "link": link
        })
    return results

def send_email(jobs, job_title, location):
    subject = f"Daily Job Alert: {job_title.title()} in {location}"
    body = f"<h3>Top Part-Time Jobs for {job_title.title()} in {location}</h3><ul>"

    for job in jobs:
        body += f"<li><strong>{job['title']}</strong> at {job['company']} - <a href='{job['link']}'>View</a></li>"

    body += "</ul>"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    job_title = "cashier"
    location = "Stoney Creek, ON"

    jobs = find_part_time_jobs(job_title, location)
    if jobs:
        send_email(jobs, job_title, location)
    else:
        print("❌ No jobs found.")

# ... (keep the previous imports and load_dotenv part)

def find_part_time_jobs(job_title, location):
    job_title_encoded = job_title.replace(" ", "+")
    location_encoded = location.replace(" ", "+")
    url = f"https://ca.indeed.com/jobs?q={job_title_encoded}&l={location_encoded}&jt=parttime"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("a", class_="tapItem")

    results = []
    for job in jobs[:5]:  # Reduce to 5 per combo for cleaner email
        title = job.find("h2").text.strip()
        company = job.find("span", class_="companyName")
        link = "https://ca.indeed.com" + job['href']
        results.append({
            "title": title,
            "company": company.text.strip() if company else "N/A",
            "link": link
        })
    return results

def send_email(all_results):
    subject = "📬 Daily Part-Time Job Alerts (Multiple Locations)"
    body = "<h2>🧠 Your Daily Job Digest</h2>"

    for combo in all_results:
        job_title = combo['job_title']
        location = combo['location']
        jobs = combo['jobs']

        body += f"<h3>{job_title.title()} in {location}</h3><ul>"
        if jobs:
            for job in jobs:
                body += f"<li><strong>{job['title']}</strong> at {job['company']} - <a href='{job['link']}'>View</a></li>"
        else:
            body += "<li>No jobs found.</li>"
        body += "</ul><hr>"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    job_titles = ["cashier", "barista"]
    locations = ["Stoney Creek, ON", "Hamilton, ON", "Toronto, ON"]

    all_results = []
    for job_title in job_titles:
        for location in locations:
            print(f"Searching for {job_title} in {location}...")
            jobs = find_part_time_jobs(job_title, location)
            all_results.append({
                "job_title": job_title,
                "location": location,
                "jobs": jobs
            })

    send_email(all_results)
