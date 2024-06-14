# ProjectScrapeAI

ProjectScrapeAI is a web scraping and data extraction tool designed to collect and structure project information from various municipal websites. It utilizes Selenium for web scraping and OpenAI's GPT-3.5-turbo model for data extraction and structuring.

## Features

Automated Web Scraping: Uses Selenium to scrape data from specified municipal project websites.
Change Detection: Checks for changes in website content before scraping to avoid redundant operations.
Data Structuring: Utilizes OpenAI's GPT-3.5-turbo model to extract and structure project details from unstructured text.
Standardized Output: Produces a standardized CSV file containing project information for easy analysis.

## Requirements

Python 3.7+

ChromeDriver (compatible version with your Chrome browser)

Selenium

BeautifulSoup

pandas

openai

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ProjectScrapeAI.git
cd ProjectScrapeAI
```

2. Install the required Python packages:

```bash
  pip install -r requirements.txt
```

3. Set up your OpenAI API key:

```bash
  export OPENAI_API_KEY='your_openai_api_key'
```

4. Download and place the ChromeDriver executable in the project directory or ensure it's accessible via your system's PATH.

## Usage

Run the script to scrape data from the predefined URLs and generate a standardized CSV file:

```bash
python project_scrape.py
```

## Configuration

### URLs to Scrape
The URLs to scrape are defined in the urls list in project_scrape.py. You can add or remove URLs as needed:

```python
urls = [
    'https://www.ci.richmond.ca.us/1404/Major-Projects',
    'https://www.eurekaca.gov/744/Upcoming-Projects',
    'https://www.cityofsanrafael.org/major-planning-projects-2/'
]
```

### Scheduling with Cron

To automate the script execution, you can set up a cron job:

1. Open the crontab file:

```bash
crontab -e
```

2. Add a cron job to run the script daily at midnight:

```bash
0 0 * * * /usr/bin/python3 /path/to/ProjectScrapeAI/project_scrape.py
```

### Logging

The script uses Python's built-in logging module to log information about its execution. Logs include details about data extraction, errors, and change detection.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

### License

This project is licensed under the MIT License. See the LICENSE file for details.
