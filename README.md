#ProjectScrapeAI

ProjectScrapeAI is a web scraping and data extraction tool designed to collect and structure project information from various municipal websites. It utilizes Selenium for web scraping and OpenAI's GPT-3.5-turbo model for data extraction and structuring.

##Features

Automated Web Scraping: Uses Selenium to scrape data from specified municipal project websites.
Change Detection: Checks for changes in website content before scraping to avoid redundant operations.
Data Structuring: Utilizes OpenAI's GPT-3.5-turbo model to extract and structure project details from unstructured text.
Standardized Output: Produces a standardized CSV file containing project information for easy analysis.
##Requirements
Python 3.7+
ChromeDriver (compatible version with your Chrome browser)
Selenium
BeautifulSoup
pandas
openai
