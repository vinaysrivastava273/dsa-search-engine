import random
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service('../../chromedriver.exe'))
url = "https://leetcode.com/problemset/all/"
prefix = "https://leetcode.com"
urls = open("urls.txt", "r", encoding="utf8").readlines()
# driver.get(url)

# for page_number in range(1, 26):
#     sleep_time = random.random() % 2 + 1
#     time.sleep(sleep_time)
#
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
#     questions = soup.find_all("a", {"class": "h-5 hover:text-blue-s dark:hover:text-dark-blue-s"})
#     for question in questions:
#         urls.append(prefix + question['href'])
#
#     if page_number == 25:
#         break
#     driver.get(url + "?page=" + str(page_number))
#
# with open("urls.txt", "w", encoding="utf8") as file:
#     file.write('\n'.join(urls))

for index in range(len(urls)):
    print(index)
    driver.get(urls[index])
    sleep_time = random.random() % 5 + 5
    time.sleep(sleep_time)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("div", {"class": "css-v3d350"}).text
    difficulty = soup.find("div", {"class": "css-10o4wqw"}).text

    problem_string = ""
    for c in title:
        if '0' <= c <= '9':
            continue
        problem_string += c

    problem_string += ' '
    for c in difficulty:
        if '0' <= c <= '9':
            break
        problem_string += c

    div = soup.find("div", {"class": "content__u3I1 question-content__JfgR"})
    statement = div.find_all("div")[0]
    if statement is not None:
        pos = statement.text.find("Example")
        problem_string += ' ' + statement.text[:pos-1]

    # related topics
    topics = soup.find_all("span", {"class": "tag__24Rd"})
    for topic in topics:
        problem_string += ' ' + topic.text

    # similar problems
    similar = soup.find_all("a", {"class": "title__1kvt"})
    for problem in similar:
        problem_string += '\n' + problem.text

    with open("Docs/doc_{}.txt".format(index), "w", encoding="utf8") as file:
        file.write(problem_string)
driver.close()
