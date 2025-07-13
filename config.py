import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LinkedIn Configuration
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL', '')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD', '')
LINKEDIN_JOB_SEARCH_URL = os.getenv('LINKEDIN_JOB_SEARCH_URL', 'https://www.linkedin.com/jobs/search/?keywords=python%20developer&location=United%20States')

# Email Configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
EMAIL_APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD', '')
EMAIL_SMTP_SERVER = 'smtp.gmail.com'
EMAIL_SMTP_PORT = 587

# Clearbit Configuration (Optional)
CLEARBIT_API_KEY = os.getenv('CLEARBIT_API_KEY', '')

# File Paths
DATA_DIR = 'data'
CV_DIR = 'cv'
JOBS_CSV = os.path.join(DATA_DIR, 'jobs.csv')
CONTACTS_CSV = os.path.join(DATA_DIR, 'contacts.csv')
SENT_EMAILS_CSV = os.path.join(DATA_DIR, 'sent_emails.csv')
CV_FILE = os.path.join(CV_DIR, 'cv.pdf')  # Update with your CV filename

# Scraping Configuration
MAX_JOBS_PER_SESSION = 50
DELAY_BETWEEN_REQUESTS = (2, 5)  # Random delay range in seconds
WEBDRIVER_TIMEOUT = 10

# Email Template
EMAIL_SUBJECT_TEMPLATE = "Application for {job_title} at {company}"
EMAIL_BODY_TEMPLATE = """
Dear Hiring Manager,

I hope this email finds you well. I am writing to express my strong interest in the {job_title} position at {company} that I found on LinkedIn.

With my background in software development and passion for technology, I believe I would be a valuable addition to your team. I have attached my resume for your review.

I would welcome the opportunity to discuss how my skills and experience can contribute to {company}'s continued success.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
[Your Name]
[Your Phone Number]
[Your Email]
"""

# Common Email Patterns for HR Contacts
EMAIL_PATTERNS = [
    'hr@{domain}',
    'careers@{domain}',
    'jobs@{domain}',
    'recruiting@{domain}',
    'talent@{domain}',
    'hiring@{domain}',
    'contact@{domain}',
    'info@{domain}',
]

# Company Domain Guessing Patterns
DOMAIN_PATTERNS = [
    '{company}.com',
    '{company}.org',
    '{company}.net',
    '{company}.io',
    '{company}.co',
]

# Schedule Configuration
SCHEDULE_TIME = "09:00"  # Time to run daily (24-hour format)
SCHEDULE_ENABLED = True