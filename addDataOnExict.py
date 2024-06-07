import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from tempfile import NamedTemporaryFile
import shutil
import os
# Specify the path to the ChromeDriver executable
# plaese change according of you 
chrome_driver_path = 'path/of/chromedriver.exe'

# Set up Selenium WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# URL of the website you want to scrape
url = 'https://marryjewelry.in/#/win'

# Navigate to the webpage
driver.get(url)

# Locate and interact with the login elements
mobile_number_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Mobile Number"]')
password_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]')
login_button = driver.find_element(By.CSS_SELECTOR, 'button.login_btn')

# Input mobile number and password
mobile_number_field.send_keys("Your mobile number")  # Replace with your mobile number
password_field.send_keys("Passward")  # Replace with your password

# Click on the login button
login_button.click()

# Wait for the login process to complete and dynamic content to load (adjust the timeout as needed)
time.sleep(1)  # Add a delay to ensure login is successful and dynamic content is loaded
# Wait for the login process to complete
WebDriverWait(driver, 10).until(EC.url_contains("#/mine"))

# Redirect to the goal URL
driver.get('https://marryjewelry.in/#/win')

# Wait for dynamic content to load (adjust the timeout as needed)
time.sleep(1)  # Add a delay to ensure dynamic content is loaded

# Extract the HTML content after the dynamic content is loaded
html_content = driver.page_source

# Define the RGB values for the colors
color1 = (76, 175, 80)
color2 = (244, 67, 54)
color3 = (156, 39, 176)

# Initialize an empty list to store data from all pages
all_data = []

# Read existing data from the CSV file, if it exists
csv_file_path = 'marry_jewelry_data.csv'
existing_codes = set()
if os.path.isfile(csv_file_path):
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            existing_codes.add(row[0])
        
while True:
    # Extract the HTML content after the dynamic content is loaded
    html_content = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the tbody element
    tbody = soup.find('tbody')

    if tbody:
        # Find all rows (tr elements) within the tbody
        rows = tbody.find_all('tr')

        # Initialize an empty list to store data from the current page
        data = []

        # Loop through each row and extract text from each cell (td elements)
        for row in rows:
            cells = [cell.get_text(strip=True) for cell in row.find_all('td')]
            # Extract the style attribute from the span element
            span_style = row.find('span', class_='red').get('style')
            # Extract RGB values from the style attribute
            rgb_values = tuple(int(value) for value in span_style.split("(")[1].split(")")[0].split(","))
            # Determine the color based on the RGB values
            if cells[2] == '0' or cells[2] == '5':
                cells[-1] = '3'
            elif rgb_values == color1:
                cells[-1] = '1'
            elif rgb_values == color2:
                cells[-1] = '2'
            data.append(cells)

        # Add the data from the current page to the list of all data
        all_data.extend(data)
        
        time.sleep(0.07)

    else:
        print("Unable to locate tbody element. Dynamic content may not have loaded.")
        break

    if any(row[0] in existing_codes for row in data):
        print("Matching data found. Exiting the loop.")
        break
    if "Last Page Now!" in driver.page_source:
        print("Last Page Now!")
        break
    # Locate the next page button and click it
    next_page_button = driver.find_element(By.CSS_SELECTOR, 'li.page_btn i.van-icon-arrow')
    driver.execute_script("arguments[0].click();", next_page_button)

# csv_file_path = 'data collect file/marry_jewelry_data.csv'

# Open the CSV file in write mode and create a CSV writer object
if os.path.isfile(csv_file_path):
    # Read existing data from the CSV file
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        existing_data = list(reader)

    # Combine new data with existing data
    combined_data = all_data + existing_data
    unique_codes = set()
    # Write the combined data to a temporary file
    with NamedTemporaryFile(mode='w', delete=False, newline='') as temp_file:
        temp_file_path = temp_file.name
        writer = csv.writer(temp_file)
        for row in combined_data:
            code = row[0]  # Assuming the unique code is in the first column
            if code not in unique_codes:
                writer.writerow(row)
                unique_codes.add(code)
    # Replace the original file with the temporary file
    shutil.move(temp_file.name, csv_file_path)
else:
    # If the file does not exist, write the new data directly to the file
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        unique_codes = set()
        for row in all_data:
            code = row[0]  # Assuming the unique code is in the first column
            if code not in unique_codes:
                writer.writerow(row)
                unique_codes.add(code)
