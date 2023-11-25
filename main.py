# First step: get all data
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import os

text = """Здравствуйте!
\nМеня зовут Стас, я студент ИТМО, провожу исследование на тему «лучшие практики в маркетинге 2023 года» для курсовой работы.
\nЯ созваниваюсь с директорами по маркетингу и спрашиваю о лучших практиках за последний год. Вот вопросы, которые я задаю:

\n1. Какие маркетинговые инструменты сработали за последний год?
\n2. Почему вы считаете, что они сработали? На что опираетесь, когда делаете такой вывод?
\n3. Какие из этих маркетинговые решения вы делали силами инхуз-команды, а какие аутсорс-командой?
\n4. Как искали аутсорс команду для ваших задач?
\n5. С какой аутсорс командой у вас получилось сработаться? Почему?
\n6. С какой аутсорс командой у вас не получилось сработаться? Почему?
\n7. На какие каналы подписаны и почему?
\n8. Для чего используете Тенчат? Решает ли он ваш запрос?

\nПо запросу я могу поделиться результатами исследования.

\nЕсли же вы не захотите делиться этим публично, то вы можете так и сказать, и я не буду нигде публиковать наше с вами интервью.

\nЕсли вам интересно поучаствовать в таком, подскажите, когда вам было бы удобно созвониться онлайн?"""

links_tg = []

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
            telegram_link = telegram_anchor.get('href')

    if link_pattern.match(telegram_link):
        links_tg.append(telegram_link)

# navigate to the website
driver.get("https://web.telegram.org/a/")

# adjust the timeout as needed
time.sleep(60)

for link_t in links_tg:
    driver.get(link_t)
    time.sleep(60)
    # get link from a link open in web
    # open this link

driver.quit()
