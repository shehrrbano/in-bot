# Automated Job Application System

A Python-based automation system that scrapes LinkedIn job listings, finds HR contacts, and sends personalized job application emails with CV attachments.

## Features

- **LinkedIn Job Scraping**: Automatically extracts job listings from LinkedIn using Selenium and BeautifulSoup
- **HR Contact Discovery**: Finds HR contacts using email pattern guessing and optional Clearbit API verification
- **Email Automation**: Sends personalized job application emails with CV attachments via Gmail SMTP
- **Smart Duplicate Prevention**: Tracks sent emails to avoid duplicate applications
- **Scheduling**: Runs automatically on a daily schedule or on-demand
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **Free & Open Source**: Uses only free tools without usage caps for long-term sustainability

## Requirements

- Python 3.9+
- Chrome browser
- LinkedIn account
- Gmail account with 2FA enabled
- Internet connection

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.template .env
   # Edit .env with your credentials
   ```

3. **Add your CV**:
   ```bash
   # Place your CV as cv.pdf in the cv/ directory
   ```

4. **Test setup**:
   ```bash
   python test_setup.py
   ```

5. **Run automation**:
   ```bash
   python main.py
   ```

## Documentation

- **[Setup Instructions](SETUP_INSTRUCTIONS.md)**: Complete installation and configuration guide
- **[Configuration Guide](config.py)**: All configuration options explained
- **[Test Setup](test_setup.py)**: Verify your setup before running

## Key Components

### LinkedIn Job Scraper
- Uses Selenium for browser automation
- Handles JavaScript-heavy LinkedIn pages
- Extracts job details (title, company, location, URL)
- Implements anti-detection measures with random delays

### HR Contact Finder
- Intelligent email pattern guessing
- Domain validation using DNS lookups
- Optional Clearbit API integration (50 requests/month free)
- Generates multiple potential contact emails

### Email Automation
- Gmail SMTP integration with app passwords
- Personalized email templates
- Automatic CV attachment
- Batch email sending with rate limiting

### Scheduling System
- Daily automated runs
- Configurable schedule times
- One-time execution option
- Graceful error handling

## Data Management

The system creates and manages several CSV files:
- `data/jobs.csv`: Raw scraped job data
- `data/contacts.csv`: Jobs enriched with HR contact information
- `data/sent_emails.csv`: Record of sent emails to prevent duplicates

## Security & Privacy

- Environment variables for sensitive data
- Gmail app passwords for secure authentication
- No hardcoded credentials in source code
- CV files excluded from version control
- Comprehensive .gitignore for sensitive files

## Advantages Over Paid Tools

Unlike paid services with restrictive free tiers:
- **No usage caps**: Unlimited scraping and email sending
- **No monthly limits**: No restrictions on email lookups
- **No cost escalation**: Completely free to run indefinitely
- **Full control**: Customize behavior and templates
- **No vendor lock-in**: Own your data and process

## Getting Started

1. **Quick Test**: Run `python test_setup.py` to verify everything is working
2. **One-time Run**: Set `SCHEDULE_ENABLED = False` in config.py for testing
3. **Production Use**: Enable scheduling for daily automated runs
4. **Monitor**: Check logs and data files for results

## Best Practices

- Start with a small job search scope for testing
- Customize email templates for better response rates
- Monitor logs for any issues or rate limiting
- Keep CV updated and professional
- Respect LinkedIn's terms of service
- Follow email marketing best practices

## Contributing

This is an open-source project. Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Share your success stories

## Legal Disclaimer

This tool is for educational and personal use only. Users are responsible for:
- Complying with LinkedIn's terms of service
- Following applicable laws and regulations
- Ensuring emails are not spam
- Respecting company policies

Use responsibly and ethically.

## Success Tips

1. **Customize your LinkedIn search URL** for relevant jobs
2. **Personalize email templates** with your experience
3. **Keep your CV updated** and role-specific
4. **Start with a small test run** to verify everything works
5. **Monitor email delivery** and adjust if needed
6. **Be patient** - quality applications take time

Ready to automate your job search? Follow the [Setup Instructions](SETUP_INSTRUCTIONS.md) to get started!
