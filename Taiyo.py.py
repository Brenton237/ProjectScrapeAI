import os
import logging
from bs4 import BeautifulSoup
import pandas as pd
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to use OpenAI API for extracting and structuring data
def extract_and_structure_data(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Extract project details from the following text: {text}"}
            ],
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error(f"Error in extracting and structuring data: {e}")
        return text  # Return the original text if there's an error

# Helper function to append structured data to the data dictionary
def append_data(data, title, description, status, date):
    structured_description = extract_and_structure_data(description)
    data['title'].append(title)
    data['description'].append(structured_description)
    data['status'].append(status)
    data['date'].append(date)

# Function to detect changes in the website content
def detect_changes(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    content = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
    current_hash = hashlib.sha256(content.encode()).hexdigest()
    previous_hash = get_previous_hash(url)
    return current_hash != previous_hash, current_hash

# Function to retrieve the previously stored hash value for the URL
def get_previous_hash(url):
    try:
        with open(f'hash_{url.replace(":", "").replace("/", "_")}.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None

# Function to save the current hash value for the URL
def save_current_hash(url, current_hash):
    with open(f'hash_{url.replace(":", "").replace("/", "_")}.txt', 'w') as file:
        file.write(current_hash)

# Function to scrape data from a single source
def scrape_website(url):
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    data = {
        'title': [],
        'description': [],
        'status': [],
        'date': []
    }
    
    try:
        change_detected, current_hash = detect_changes(driver, url)
        if not change_detected:
            logging.info(f"No changes detected for {url}")
            return pd.DataFrame(data)
        
        logging.info(f"Changes detected for {url}, scraping data...")
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        if 'richmond' in url:
            scrape_richmond(driver, wait, data)
        elif 'eurekaca' in url:
            scrape_eurekaca(driver, wait, data)
        else:
            scrape_generic(driver, data)
        
        save_current_hash(url, current_hash)

    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
    finally:
        driver.quit()
    
    return pd.DataFrame(data)

# Function to scrape Richmond website
def scrape_richmond(driver, wait, data):
    target_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fr-view")))
    links = target_div.find_elements(By.CLASS_NAME, "Hyperlink")
    
    for link in links:
        link.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        title = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
        div = soup.find('div', class_='fr-view')
        description = div.find('p').text.strip() if div.find('p') else 'N/A'
        status = 'N/A'
        date = 'N/A'
        
        append_data(data, title, description, status, date)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

# Function to scrape EurekaCA website
def scrape_eurekaca(driver, wait, data):
    target_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cpTabPanels")))
    buttons = target_div.find_elements(By.CLASS_NAME, "tabButton")
    
    for button in buttons:
        button.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        title = soup.find('h2').text.strip() if soup.find('h2') else 'N/A'
        div = soup.find('div', class_='fr-view')
        description = div.find('p').text.strip() if div.find('p') else 'N/A'
        status = 'N/A'
        date = 'N/A'
        
        append_data(data, title, description, status, date)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

# Function to scrape generic website
def scrape_generic(driver, data):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find('table', class_='table')
    elements = table.find_all("tr")[1:]
    for element in elements:
        title = element.find_all('td')[0].text.strip() if element.find_all('td')[0] else 'N/A'
        description = element.find_all('td')[1].text.strip() if element.find_all('td')[1] else 'N/A'
        status = element.find_all('td')[7].text.strip() if element.find_all('td')[7] else 'N/A'
        date = 'N/A'
        
        append_data(data, title, description, status, date)

# Function to standardize the scraped data
def standardize_data(df, source_url):
    standardized_data = pd.DataFrame(columns=[
        'original_id', 'aug_id', 'country_name', 'country_code', 'map_coordinates', 'url', 
        'region_name', 'region_code', 'title', 'description', 'status', 'stages', 'date', 
        'procurementMethod', 'budget', 'currency', 'buyer', 'sector', 'subsector'
    ])
    
    standardized_data['title'] = df['title']
    standardized_data['description'] = df['description']
    standardized_data['status'] = df['status']
    standardized_data['date'] = df['date']
    standardized_data['url'] = source_url
    
    return standardized_data

# Main script execution
urls = [
    'https://www.ci.richmond.ca.us/1404/Major-Projects',
    'https://www.eurekaca.gov/744/Upcoming-Projects',
    'https://www.cityofsanrafael.org/major-planning-projects-2/'
]

all_data = pd.DataFrame()

for url in urls:
    scraped_data = scrape_website(url)
    if not scraped_data.empty:
        standardized_data = standardize_data(scraped_data, url)
        all_data = pd.concat([all_data, standardized_data], ignore_index=True)

# Save to CSV
all_data.to_csv('standardized_data.csv', index=False)
