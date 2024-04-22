from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to your chromedriver executable
chromedriver_path='C:/Users/mianw/OneDrive/Desktop/Side Projects/Keyboard/chromedriver-win64/chromedriver-win64/chromedriver.exe'


# URL to open
url = 'https://www.youtube.com/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_experimental_option("detach", True)


# Setup Chrome service to handle crashes
service = Service(executable_path=chromedriver_path)
service.start()

# Initialize Chrome driver with configured options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Detach the WebDriver session from the browser window
# original_window = driver.current_window_handle

# Navigate to the URL
driver.get(url)

# Script finishes here, but browser window stays open

# Quit the WebDriver session
# driver.quit()

# Stop the Chrome service
# service.stop()



# # Setup Chrome options to disable automated extensions prompting
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--disable-popup-blocking')
# chrome_options.add_experimental_option("detach", True)

# # Setup Chrome service to handle crashes
# service = Service(chromedriver_path)
# service.start()

# # Initialize Chrome driver with configured options
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # Detach the WebDriver session from the browser window
# original_window = driver.current_window_handle

# # Navigate to the URL
# driver.get(url)

# # Script finishes here, but browser window stays open

# # Quit the WebDriver session
# # driver.quit()

# # Stop the Chrome service
# # service.stop()
