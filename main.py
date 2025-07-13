#!/usr/bin/env python3
"""
This script automates the process of:
1. Scraping LinkedIn job listings
2. Finding HR contacts through email pattern guessing
3. Sending personalized emails with CV attachments
4. Scheduling daily runs

Author: Shehr Bano
Version: 1.0
"""

import os
import sys
import csv
import time
import random
import logging
import smtplib
import schedule
import requests
import pandas as pd
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from urllib.parse import urljoin, urlparse
import dns.resolver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('job_application.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class LinkedInJobScraper:
    """LinkedIn job scraper using Selenium and BeautifulSoup"""
    
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(config.WEBDRIVER_TIMEOUT)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def login_to_linkedin(self):
        """Login to LinkedIn"""
        try:
            logger.info("Logging into LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for login form
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Enter credentials
            username_field = self.driver.find_element(By.ID, "username")
            password_field = self.driver.find_element(By.ID, "password")
            
            username_field.send_keys(config.LINKEDIN_EMAIL)
            password_field.send_keys(config.LINKEDIN_PASSWORD)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "jobs" in self.driver.current_url:
                logger.info("LinkedIn login successful")
                return True
            else:
                logger.warning("LinkedIn login may have failed")
                return False
                
        except Exception as e:
            logger.error(f"LinkedIn login failed: {e}")
            return False
    
    def scrape_jobs(self, job_search_url):
        """Scrape jobs from LinkedIn job search page"""
        jobs = []
        
        try:
            logger.info(f"Scraping jobs from: {job_search_url}")
            self.driver.get(job_search_url)
            
            # Wait for job listings to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
            )
            
            # Scroll down to load more jobs
            self.scroll_to_load_jobs()
            
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Find job listings
            job_elements = soup.find_all('div', class_='job-search-card')
            
            for job_element in job_elements[:config.MAX_JOBS_PER_SESSION]:
                try:
                    job_data = self.extract_job_data(job_element)
                    if job_data:
                        jobs.append(job_data)
                        logger.info(f"Scraped job: {job_data['title']} at {job_data['company']}")
                except Exception as e:
                    logger.warning(f"Error extracting job data: {e}")
                    continue
                    
                # Random delay to avoid detection
                time.sleep(random.uniform(*config.DELAY_BETWEEN_REQUESTS))
            
            logger.info(f"Successfully scraped {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Error scraping jobs: {e}")
            return []
    
    def scroll_to_load_jobs(self):
        """Scroll down to load more job listings"""
        try:
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait for new content to load
                time.sleep(2)
                
                # Calculate new scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break
                    
                last_height = new_height
                
        except Exception as e:
            logger.warning(f"Error scrolling to load jobs: {e}")
    
    def extract_job_data(self, job_element):
        """Extract job data from job element"""
        try:
            job_data = {}
            
            # Extract job title
            title_element = job_element.find('h3', class_='base-search-card__title')
            job_data['title'] = title_element.get_text(strip=True) if title_element else 'N/A'
            
            # Extract company name
            company_element = job_element.find('h4', class_='base-search-card__subtitle')
            job_data['company'] = company_element.get_text(strip=True) if company_element else 'N/A'
            
            # Extract location
            location_element = job_element.find('span', class_='job-search-card__location')
            job_data['location'] = location_element.get_text(strip=True) if location_element else 'N/A'
            
            # Extract job URL
            link_element = job_element.find('a', class_='base-card__full-link')
            job_data['url'] = link_element['href'] if link_element else 'N/A'
            
            # Extract posting date
            date_element = job_element.find('time', class_='job-search-card__listdate')
            job_data['posted_date'] = date_element['datetime'] if date_element else 'N/A'
            
            # Add scraping metadata
            job_data['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error extracting job data: {e}")
            return None
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")

class HRContactFinder:
    """Find HR contacts using email pattern guessing and optional Clearbit API"""
    
    def __init__(self):
        self.clearbit_requests_made = 0
        self.clearbit_limit = 50  # Monthly limit
    
    def guess_company_domain(self, company_name):
        """Guess company domain from company name"""
        # Clean company name
        company_clean = company_name.lower().strip()
        company_clean = company_clean.replace(' ', '').replace(',', '').replace('.', '')
        company_clean = company_clean.replace('inc', '').replace('corp', '').replace('llc', '')
        company_clean = company_clean.replace('ltd', '').replace('co', '')
        
        # Try different domain patterns
        for pattern in config.DOMAIN_PATTERNS:
            domain = pattern.format(company=company_clean)
            if self.validate_domain(domain):
                return domain
        
        return None
    
    def validate_domain(self, domain):
        """Validate if domain exists using DNS lookup"""
        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except:
            try:
                dns.resolver.resolve(domain, 'A')
                return True
            except:
                return False
    
    def generate_hr_emails(self, company_name, domain):
        """Generate possible HR email addresses"""
        hr_emails = []
        
        if domain:
            for pattern in config.EMAIL_PATTERNS:
                email = pattern.format(domain=domain)
                hr_emails.append(email)
        
        return hr_emails
    
    def verify_email_with_clearbit(self, email):
        """Verify email using Clearbit API (optional, limited usage)"""
        if not config.CLEARBIT_API_KEY or self.clearbit_requests_made >= self.clearbit_limit:
            return None
        
        try:
            url = f"https://person.clearbit.com/v1/people/email/{email}"
            headers = {'Authorization': f'Bearer {config.CLEARBIT_API_KEY}'}
            
            response = requests.get(url, headers=headers, timeout=10)
            self.clearbit_requests_made += 1
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            logger.warning(f"Clearbit API error: {e}")
            return None
    
    def enrich_jobs_with_contacts(self, jobs):
        """Enrich job data with HR contact information"""
        enriched_jobs = []
        
        for job in jobs:
            try:
                company_name = job['company']
                logger.info(f"Finding HR contacts for {company_name}")
                
                # Guess company domain
                domain = self.guess_company_domain(company_name)
                
                if domain:
                    # Generate HR emails
                    hr_emails = self.generate_hr_emails(company_name, domain)
                    
                    # Use the first email as primary contact
                    primary_email = hr_emails[0] if hr_emails else None
                    
                    # Optionally verify with Clearbit
                    clearbit_data = None
                    if primary_email:
                        clearbit_data = self.verify_email_with_clearbit(primary_email)
                    
                    # Add contact information to job data
                    job['domain'] = domain
                    job['hr_emails'] = hr_emails
                    job['primary_email'] = primary_email
                    job['clearbit_verified'] = clearbit_data is not None
                    
                    logger.info(f"Found {len(hr_emails)} potential HR emails for {company_name}")
                else:
                    logger.warning(f"Could not determine domain for {company_name}")
                    job['domain'] = None
                    job['hr_emails'] = []
                    job['primary_email'] = None
                    job['clearbit_verified'] = False
                
                enriched_jobs.append(job)
                
                # Random delay
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"Error enriching job with HR contacts: {e}")
                job['domain'] = None
                job['hr_emails'] = []
                job['primary_email'] = None
                job['clearbit_verified'] = False
                enriched_jobs.append(job)
        
        return enriched_jobs

class EmailAutomation:
    """Email automation system using smtplib"""
    
    def __init__(self):
        self.smtp_server = config.EMAIL_SMTP_SERVER
        self.smtp_port = config.EMAIL_SMTP_PORT
        self.email_address = config.EMAIL_ADDRESS
        self.email_password = config.EMAIL_APP_PASSWORD
    
    def send_job_application_email(self, job_data):
        """Send job application email with CV attachment"""
        try:
            if not job_data['primary_email']:
                logger.warning(f"No email found for {job_data['company']}")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = job_data['primary_email']
            msg['Subject'] = config.EMAIL_SUBJECT_TEMPLATE.format(
                job_title=job_data['title'],
                company=job_data['company']
            )
            
            # Create email body
            body = config.EMAIL_BODY_TEMPLATE.format(
                job_title=job_data['title'],
                company=job_data['company']
            )
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach CV if exists
            if os.path.exists(config.CV_FILE):
                with open(config.CV_FILE, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(config.CV_FILE)}'
                    )
                    msg.attach(part)
            else:
                logger.warning(f"CV file not found: {config.CV_FILE}")
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {job_data['primary_email']} for {job_data['company']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {job_data.get('primary_email', 'unknown')}: {e}")
            return False
    
    def send_batch_emails(self, jobs_data):
        """Send emails to multiple recipients"""
        sent_count = 0
        failed_count = 0
        
        for job in jobs_data:
            try:
                if self.send_job_application_email(job):
                    sent_count += 1
                    # Record sent email
                    self.record_sent_email(job)
                else:
                    failed_count += 1
                
                # Random delay between emails
                time.sleep(random.uniform(10, 30))
                
            except Exception as e:
                logger.error(f"Error sending email for job: {e}")
                failed_count += 1
        
        logger.info(f"Email batch complete: {sent_count} sent, {failed_count} failed")
        return sent_count, failed_count
    
    def record_sent_email(self, job_data):
        """Record sent email to avoid duplicates"""
        try:
            sent_record = {
                'company': job_data['company'],
                'job_title': job_data['title'],
                'email': job_data['primary_email'],
                'sent_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Append to sent emails CSV
            file_exists = os.path.exists(config.SENT_EMAILS_CSV)
            with open(config.SENT_EMAILS_CSV, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=sent_record.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(sent_record)
                
        except Exception as e:
            logger.error(f"Error recording sent email: {e}")

class JobApplicationAutomation:
    """Main automation system orchestrating all components"""
    
    def __init__(self):
        self.scraper = None
        self.contact_finder = HRContactFinder()
        self.email_automation = EmailAutomation()
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(config.DATA_DIR, exist_ok=True)
        os.makedirs(config.CV_DIR, exist_ok=True)
    
    def load_sent_emails(self):
        """Load previously sent emails to avoid duplicates"""
        sent_emails = set()
        if os.path.exists(config.SENT_EMAILS_CSV):
            try:
                df = pd.read_csv(config.SENT_EMAILS_CSV)
                for _, row in df.iterrows():
                    sent_emails.add(f"{row['company']}|{row['job_title']}")
            except Exception as e:
                logger.warning(f"Error loading sent emails: {e}")
        return sent_emails
    
    def filter_new_jobs(self, jobs, sent_emails):
        """Filter out jobs we've already applied to"""
        new_jobs = []
        for job in jobs:
            job_key = f"{job['company']}|{job['title']}"
            if job_key not in sent_emails:
                new_jobs.append(job)
        
        logger.info(f"Filtered {len(new_jobs)} new jobs from {len(jobs)} total jobs")
        return new_jobs
    
    def save_jobs_to_csv(self, jobs, filename):
        """Save jobs data to CSV file"""
        try:
            if jobs:
                df = pd.DataFrame(jobs)
                df.to_csv(filename, index=False, encoding='utf-8')
                logger.info(f"Saved {len(jobs)} jobs to {filename}")
            else:
                logger.warning("No jobs to save")
        except Exception as e:
            logger.error(f"Error saving jobs to CSV: {e}")
    
    def run_daily_automation(self):
        """Run the complete automation process"""
        logger.info("Starting daily job application automation")
        
        try:
            # Initialize scraper
            self.scraper = LinkedInJobScraper()
            
            # Login to LinkedIn
            if not self.scraper.login_to_linkedin():
                logger.error("Failed to login to LinkedIn. Aborting automation.")
                return
            
            # Scrape jobs
            jobs = self.scraper.scrape_jobs(config.LINKEDIN_JOB_SEARCH_URL)
            
            if not jobs:
                logger.warning("No jobs found. Ending automation.")
                return
            
            # Save raw jobs data
            self.save_jobs_to_csv(jobs, config.JOBS_CSV)
            
            # Load sent emails to avoid duplicates
            sent_emails = self.load_sent_emails()
            
            # Filter new jobs
            new_jobs = self.filter_new_jobs(jobs, sent_emails)
            
            if not new_jobs:
                logger.info("No new jobs to apply to.")
                return
            
            # Enrich with HR contacts
            enriched_jobs = self.contact_finder.enrich_jobs_with_contacts(new_jobs)
            
            # Save enriched jobs data
            self.save_jobs_to_csv(enriched_jobs, config.CONTACTS_CSV)
            
            # Filter jobs with valid emails
            jobs_with_emails = [job for job in enriched_jobs if job['primary_email']]
            
            if not jobs_with_emails:
                logger.warning("No jobs with valid email addresses found.")
                return
            
            # Send emails
            sent_count, failed_count = self.email_automation.send_batch_emails(jobs_with_emails)
            
            logger.info(f"Daily automation complete: {sent_count} applications sent, {failed_count} failed")
            
        except Exception as e:
            logger.error(f"Error in daily automation: {e}")
        finally:
            # Clean up
            if self.scraper:
                self.scraper.close()
    
    def start_scheduler(self):
        """Start the daily scheduler"""
        if not config.SCHEDULE_ENABLED:
            logger.info("Scheduler disabled. Running once and exiting.")
            self.run_daily_automation()
            return
        
        logger.info(f"Starting scheduler. Daily run at {config.SCHEDULE_TIME}")
        schedule.every().day.at(config.SCHEDULE_TIME).do(self.run_daily_automation)
        
        # Run immediately on first start
        logger.info("Running initial automation...")
        self.run_daily_automation()
        
        # Keep scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main function"""
    try:
        # Check configuration
        if not config.LINKEDIN_EMAIL or not config.LINKEDIN_PASSWORD:
            logger.error("LinkedIn credentials not configured. Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env file.")
            return
        
        if not config.EMAIL_ADDRESS or not config.EMAIL_APP_PASSWORD:
            logger.error("Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_APP_PASSWORD in .env file.")
            return
        
        if not os.path.exists(config.CV_FILE):
            logger.warning(f"CV file not found at {config.CV_FILE}. Please place your CV in the cv directory.")
        
        # Start automation
        automation = JobApplicationAutomation()
        automation.start_scheduler()
        
    except KeyboardInterrupt:
        logger.info("Automation stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
