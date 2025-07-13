# Automated Job Application System - Setup Instructions

## Overview
This system automates the process of applying for jobs on LinkedIn by:
1. Scraping LinkedIn job listings
2. Finding HR contacts through email pattern guessing
3. Sending personalized emails with CV attachments
4. Running on a daily schedule

## Prerequisites

### System Requirements
- Python 3.9 or higher
- Linux/macOS/Windows (tested on Linux)
- Internet connection
- Chrome browser (for WebDriver)

### Required Accounts
- LinkedIn account (for job scraping)
- Gmail account (for sending emails)
- Optional: Clearbit account (for email verification)

## Installation

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd job-application-automation
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
1. Copy the template environment file:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file with your credentials:
   ```bash
   nano .env
   ```

3. Fill in the required values:
   - `LINKEDIN_EMAIL`: Your LinkedIn email address
   - `LINKEDIN_PASSWORD`: Your LinkedIn password
   - `EMAIL_ADDRESS`: Your Gmail address
   - `EMAIL_APP_PASSWORD`: Your Gmail app password (see below for setup)
   - `LINKEDIN_JOB_SEARCH_URL`: Custom LinkedIn job search URL
   - `CLEARBIT_API_KEY`: Optional Clearbit API key

### 4. Set Up Gmail App Password

#### Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Navigate to "Security"
3. Enable "2-Step Verification"

#### Generate App Password
1. In Google Account Security settings
2. Click "App passwords"
3. Select "Mail" and "Other (custom name)"
4. Enter "Job Application Bot"
5. Copy the generated 16-character password
6. Use this password in the `.env` file as `EMAIL_APP_PASSWORD`

### 5. Add Your CV
1. Create the `cv` directory:
   ```bash
   mkdir cv
   ```
2. Place your CV file in the `cv` directory as `cv.pdf`
3. If your CV has a different name, update the `CV_FILE` path in `config.py`

### 6. Create Data Directory
```bash
mkdir data
```

## Configuration

### LinkedIn Job Search URL
Customize your job search by modifying the `LINKEDIN_JOB_SEARCH_URL` in the `.env` file:

Examples:
- Python Developer: `https://www.linkedin.com/jobs/search/?keywords=python%20developer&location=United%20States`
- Data Scientist: `https://www.linkedin.com/jobs/search/?keywords=data%20scientist&location=New%20York`
- Remote Jobs: `https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=Remote`

### Email Template Customization
Edit the `EMAIL_BODY_TEMPLATE` in `config.py` to customize your email message:

```python
EMAIL_BODY_TEMPLATE = """
Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company}.

[Your personalized message here]

Best regards,
[Your Name]
[Your Contact Information]
"""
```

### Schedule Configuration
By default, the system runs daily at 9:00 AM. To change this:

1. Edit `SCHEDULE_TIME` in `config.py`
2. To run only once (no scheduling), set `SCHEDULE_ENABLED = False`

### Scraping Limits
To avoid LinkedIn detection, adjust these settings in `config.py`:
- `MAX_JOBS_PER_SESSION`: Maximum jobs to scrape per run (default: 50)
- `DELAY_BETWEEN_REQUESTS`: Random delay between requests (default: 2-5 seconds)

## Usage

### Running the System

#### One-time Execution
```bash
python main.py
```

#### Daily Scheduled Execution
The system runs automatically with scheduling enabled. To stop, press `Ctrl+C`.

### Monitoring
- Check `job_application.log` for detailed logs
- Review `data/jobs.csv` for scraped job data
- Review `data/contacts.csv` for enriched contact information
- Review `data/sent_emails.csv` for sent email records

### Data Files
The system creates several CSV files in the `data/` directory:
- `jobs.csv`: Raw scraped job data
- `contacts.csv`: Job data enriched with HR contact information
- `sent_emails.csv`: Record of sent emails to avoid duplicates

## Troubleshooting

### Common Issues

#### LinkedIn Login Issues
- Ensure credentials are correct in `.env`
- Check if LinkedIn requires CAPTCHA (may need manual intervention)
- Consider using LinkedIn's "Sign in with Google" for better reliability

#### Email Sending Issues
- Verify Gmail app password is correct
- Ensure 2-factor authentication is enabled
- Check Gmail security settings
- Verify SMTP settings in `config.py`

#### WebDriver Issues
- Chrome browser must be installed
- WebDriver is automatically managed by `webdriver-manager`
- If issues persist, try updating Chrome browser

#### Rate Limiting
- LinkedIn may temporarily block scraping if detected
- Increase delays in `config.py`
- Consider running less frequently

### Log Analysis
Check the log file for detailed error information:
```bash
tail -f job_application.log
```

## Best Practices

### Compliance
- Respect LinkedIn's terms of service
- Don't scrape excessively (keep within reasonable limits)
- Ensure emails are not spam (personalize messages)
- Follow CAN-SPAM Act guidelines

### Email Effectiveness
- Customize the email template for better response rates
- Keep messages concise and professional
- Ensure your CV is up-to-date and relevant

### System Maintenance
- Regularly check logs for errors
- Update LinkedIn job search URL as needed
- Monitor email delivery rates
- Update email templates periodically

## Optional Features

### Clearbit Integration
1. Sign up for a free Clearbit account
2. Get your API key from the dashboard
3. Add the key to your `.env` file
4. The system will use Clearbit to verify emails (50 requests/month free)

### Custom Email Patterns
Add custom email patterns in `config.py`:
```python
EMAIL_PATTERNS = [
    'hr@{domain}',
    'careers@{domain}',
    'jobs@{domain}',
    'talent@{domain}',
    # Add your custom patterns here
]
```

### Domain Validation
The system validates company domains using DNS lookup. This helps ensure emails are sent to valid domains.

## Security Considerations

### Credential Security
- Never commit your `.env` file to version control
- Use strong, unique passwords
- Consider using OAuth instead of passwords where possible
- Regularly rotate your Gmail app password

### Email Security
- Use Gmail's app-specific passwords
- Enable 2-factor authentication
- Monitor sent emails for suspicious activity

## Support

### Getting Help
- Check the log file for error details
- Review this documentation
- Ensure all prerequisites are met
- Test individual components separately

### System Updates
- Regularly update Python packages: `pip install -r requirements.txt --upgrade`
- Update the system when LinkedIn changes their HTML structure
- Monitor for security updates

## Limitations

### Free Tier Limitations
- Clearbit: 50 email verifications per month
- Gmail: 500 emails per day (sufficient for most use cases)
- LinkedIn: No official API usage, relies on scraping

### Technical Limitations
- Depends on LinkedIn's HTML structure (may break with updates)
- Email pattern guessing may not always be accurate
- Some companies may have anti-scraping measures

## Legal Disclaimer

This tool is for educational and personal use only. Users are responsible for:
- Complying with LinkedIn's terms of service
- Following applicable laws and regulations
- Ensuring emails are not spam
- Respecting company policies

Use this tool responsibly and ethically.