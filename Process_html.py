from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Set the path to your Chromedriver executable including the ".exe" extension
chrome_driver_path = "C:\\Users\\Brian\\Downloads\\CPR_process\\chromedriver.exe"

# Define the URL of the webpage to load
url = "https://www.chicagopetrescue.org/foster-pet-update-form.html"

# Configure Chrome options for headless mode
chrome_options = ChromeOptions()
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode

# Set the Chromedriver executable path
chrome_service = ChromeService(chrome_driver_path)

# Create a WebDriver instance
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Load the webpage
driver.get(url)

# Wait for 5 seconds for the page to load (adjust the time as needed)
time.sleep(5)

# Save the page source to "original.html"
with open("original.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Define the base URL
base_url = "https://www.chicagopetrescue.org/"

# Create a list to store the replaced relative references
replaced_references = []

# Find all HTML elements with attributes that may contain relative URLs
elements_with_urls = soup.find_all(['a', 'img', 'link', 'script', 'iframe', 'embed', 'source'])

# Loop through each element and replace relative URLs with absolute ones
for element in elements_with_urls:
    for attribute in ['href', 'src', 'data-src', 'data-href']:
        if attribute in element.attrs:
            relative_url = element[attribute]
            absolute_url = urljoin(base_url, relative_url)
            element[attribute] = absolute_url
            replaced_references.append((relative_url, absolute_url))

# Print the list of replaced references
for relative, absolute in replaced_references:
    print(f"Replaced relative reference: {relative} -> {absolute}")

# Get the modified HTML as a string
modified_html = str(soup)

# Save the modified HTML to a file with UTF-8 encoding
with open("modified.html", "w", encoding="utf-8") as file:
    file.write(modified_html)

# Close the WebDriver
driver.quit()

print("Webpage saved to 'original.html'")
print("Modified HTML saved to 'modified.html'")
