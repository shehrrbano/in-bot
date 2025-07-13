#!/usr/bin/env python3
"""
This script tests the configuration and setup before running the main automation.
It verifies credentials, dependencies, and basic functionality.
"""

import os
import sys
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dns.resolver
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_python_version():
    """Test Python version compatibility"""
    print("Testing Python version...")
    if sys.version_info < (3, 9):
        print("Python 3.9 or higher required")
        return False
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def test_dependencies():
    """Test required Python dependencies"""
    print("\nTesting dependencies...")
    required_packages = [
        'selenium', 'beautifulsoup4', 'requests', 'schedule', 
        'pandas', 'webdriver_manager', 'python-dotenv', 'dnspython'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"{package}")
        except ImportError:
            print(f"{package} not found")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def test_env_file():
    """Test .env file configuration"""
    print("\nTesting .env file...")
    
    if not os.path.exists('.env'):
        print(" .env file not found")
        print("Copy .env.template to .env and fill in your credentials")
        return False
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception as e:
        print(f" Error loading .env file: {e}")
        return False
    
    # Check required variables
    required_vars = ['LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD', 'EMAIL_ADDRESS', 'EMAIL_APP_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == f'your_{var.lower()}':
            missing_vars.append(var)
            print(f" {var} not configured")
        else:
            print(f"{var} configured")
    
    if missing_vars:
        print(f"\nMissing environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def test_webdriver():
    """Test Chrome WebDriver setup"""
    print("\nTesting Chrome WebDriver...")
    
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test basic functionality
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"Chrome WebDriver working (tested with: {title})")
        return True
        
    except Exception as e:
        print(f"Chrome WebDriver error: {e}")
        print("Make sure Chrome browser is installed")
        return False

def test_email_connection():
    """Test email SMTP connection"""
    print("\nTesting email connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        email_address = os.getenv('EMAIL_ADDRESS')
        email_password = os.getenv('EMAIL_APP_PASSWORD')
        
        if not email_address or not email_password:
            print("Email credentials not configured")
            return False
        
        # Test SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        server.quit()
        
        print("Email SMTP connection successful")
        return True
        
    except Exception as e:
        print(f"Email connection error: {e}")
        print("Check your Gmail app password and 2FA settings")
        return False

def test_dns_resolution():
    """Test DNS resolution for domain validation"""
    print("\nTesting DNS resolution...")
    
    try:
        # Test with a known domain
        dns.resolver.resolve('google.com', 'A')
        print("DNS resolution working")
        return True
        
    except Exception as e:
        print(f"DNS resolution error: {e}")
        return False

def test_clearbit_api():
    """Test Clearbit API (optional)"""
    print("\nTesting Clearbit API (optional)...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('CLEARBIT_API_KEY')
        if not api_key or api_key == 'your_clearbit_api_key':
            print("Clearbit API key not configured (optional)")
            return True
        
        # Test API call
        url = "https://person.clearbit.com/v1/people/email/test@example.com"
        headers = {'Authorization': f'Bearer {api_key}'}
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code in [200, 404]:  # 404 is expected for test email
            print("Clearbit API connection successful")
            return True
        else:
            print(f"Clearbit API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Clearbit API error: {e}")
        return False

def test_file_structure():
    """Test file structure and permissions"""
    print("\nTesting file structure...")
    
    # Check required directories
    required_dirs = ['data', 'cv']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"{dir_name}/ directory exists")
        else:
            print(f"{dir_name}/ directory missing")
            return False
    
    # Check CV file
    cv_file = 'cv/cv.pdf'
    if os.path.exists(cv_file):
        print(f"CV file found: {cv_file}")
    else:
        print(f"CV file not found: {cv_file}")
        print("Place your CV as 'cv.pdf' in the cv/ directory")
    
    return True

def test_linkedin_url():
    """Test LinkedIn job search URL"""
    print("\nTesting LinkedIn job search URL...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        url = os.getenv('LINKEDIN_JOB_SEARCH_URL')
        if not url or 'linkedin.com' not in url:
            print("Invalid LinkedIn job search URL")
            return False
        
        print(f"LinkedIn job search URL configured: {url[:50]}...")
        return True
        
    except Exception as e:
        print(f"LinkedIn URL error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Job Application Automation Setup\n")
    
    tests = [
        test_python_version,
        test_dependencies,
        test_env_file,
        test_file_structure,
        test_webdriver,
        test_email_connection,
        test_dns_resolution,
        test_linkedin_url,
        test_clearbit_api,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"Test error: {e}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("All tests passed! You're ready to run the automation.")
        print("Run: python main.py")
    else:
        print("Some tests failed. Please fix the issues before running the automation.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
