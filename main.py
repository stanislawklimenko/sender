# First step: get all data
import pyautogui
import requests
import pyperclip
import keyboard
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import os

usernames = []

links = []
link_pattern = re.compile(r'https?://\S+')

print("Enter links. Type 'stop' to finish.")

while True:
    user_input = input("Enter a link: ")

    if user_input.lower() == 'stop':
        break

    # Check if the input is a valid link using the regular expression
    if link_pattern.match(user_input):
        links.append(user_input)
        # print("Link added.")
    else:
        print("Invalid link. Please enter a valid URL.")


# Second step: check if there telegram

# 2.1 Log in TenChat
geckodriver_path = 'geckodriver.exe'

# add the WebDriver path to the system's PATH variable
os.environ['PATH'] += os.pathsep + geckodriver_path

# initialize the Firefox WebDriver
driver = webdriver.Firefox()

# navigate to the website
driver.get("https://tenchat.ru/auth/sign-in")

# adjust the timeout as needed
time.sleep(60)

# 2.2 Open the links one by one and extract telegram
for link in links:
    driver.get(link)
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    telegram_link = None

    telegram_div = soup.find('div', {'data-cy': 'telegram'})

    # Check if the div is found
    if telegram_div:
        # Find the anchor tag within the div
        telegram_anchor = telegram_div.find('a')

        # Check if the anchor tag is found
        if telegram_anchor:
            # Extract the Telegram link from the href attribute
            telegram_text = telegram_anchor.get_text(strip=True)

            usernames.append(telegram_text[1:])

driver.quit()

text = """Здравствуйте!
\nМеня зовут Стас, я сооснователь бюро, которое делает сайты и их продвигает.
\nПишу, чтобы предложить бесплатную консультацию по улучшению сайта.
\nЕсли хотите сделать сайт с нуля для нового проекта, можем обсудить: зачем он вам может пригодиться, что на него добавить и как его продвигать.
\nК разбору сайта мы подключаем дизайнера и коммерческого редактора. Поэтому вы получаете комплексный ответ, а не просто мнение одного специалиста.
\nЕсли вам интересно, напишите время, когда вам было бы удобно созвониться."""

# Open the Telegram application
pyautogui.hotkey('winleft')
time.sleep(5)
pyautogui.write('Telegram', interval=0.25)
pyautogui.press('enter')
time.sleep(5)

# Loop through the usernames and send the message
for username in usernames:
    # Clear the existing text in the search field
    pyautogui.hotkey('ctrl', 'a')  # Select all text
    pyautogui.press('delete')  # Delete the selected text

    # Search for the user
    pyperclip.copy(username)
    pyautogui.hotkey('ctrl', 'v')  # Paste the username from the clipboard
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(2)

    # Type and send the message
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')  # Paste the message from the clipboard
    pyautogui.press('enter')

    # Go back to the main chat list
    pyautogui.hotkey('esc')

# Close the Telegram application
pyautogui.hotkey('alt', 'f4')