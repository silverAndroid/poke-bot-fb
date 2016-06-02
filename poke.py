import getpass
import pickle
import re
import time
import login

import requests
from bs4 import BeautifulSoup


def save_cookies(filename):
    with open(filename, 'w') as f:
        pickle.dump(requests.utils.dict_from_cookiejar(session.cookies), f)


def load_cookies(filename):
    with open(filename) as f:
        return requests.utils.cookiejar_from_dict(pickle.load(f))


def poke(cookies):
    poke_url = 'https://m.facebook.com/pokes'
    if cookies is None:
        poke_page = session.get(poke_url)
    else:
        poke_page = session.get(poke_url, cookies=cookies)
    # print poke_page.text

    soup = BeautifulSoup(poke_page.text, 'html.parser')
    try:
        poke_container = soup.findAll('div', {'class': 'g'})[0] \
            .findAll('div', {'id': 'viewport'})[0] \
            .findAll('div', {'id': 'objects_container'})[0] \
            .findAll('div', {'id': 'root'})[0] \
            .findAll('table', {'class': 'm'})[0] \
            .findAll('tr')[0] \
            .findAll('td', {'class': 't'})[0] \
            .findAll('div', {'id': 'poke_area'})[0]

        poke_name = poke_container.findAll('div', {'class': 'bq'})[1] \
            .findAll('div', {'class': 'bx'})[0].text
        substrings = [m.start() for m in re.finditer('( poked you [0-9]+ times in a row)', poke_name.replace(',', ''))]

        poke_link = poke_container.findAll('div', {'class': 'bq'})[0] \
            .findAll('div')[7] \
            .findAll('a', {'class': 'ca'})[0]['href']

        # print poke_container
        # print poke_link
        poke_response = session.get('https://m.facebook.com' + poke_link)
        # print poke_response.text

        if "poke_status=success" in poke_response.url:
            time_formatted = time.strftime("%H:%M %Z")
            print 'Successfully poked {0} at {1}!'.format(poke_name[:substrings[0]].strip(), time_formatted)
    except IndexError:
        print 'No one to poke :('


cookies = None

while True:
    session = requests.Session()
    print "Loading Facebook..."
    load_facebook_request = session.get('https://m.facebook.com')
    soup = BeautifulSoup(load_facebook_request.text, 'html.parser')
    print "Loaded Facebook!"

    try:
        cookies = load_cookies('cookies')
        break
    except IOError as e:
        if "No such file or directory" not in e.strerror:
            raise

    print "Login to Facebook"
    email = raw_input("Email: ")
    password = getpass.getpass("Password: ")
    cookies_save = ''
    while cookies_save is not 'y' or not 'n':
        cookies_save = raw_input('Stay logged in? (y/n) ')
    cookies_save = cookies_save == 'y'
    login_obj = login.Login(email, password)
    login_request = login_obj.login(soup, session)

    if '/login' not in login_request.url:
        if cookies_save:
            save_cookies('cookies')
        break
    print 'Your email or password is incorrect. Please try again..'
print "Logged into Facebook!"

refresh_seconds = raw_input('How many seconds would you like the bot to wait before checking for new pokes? ')

while True:
    poke(cookies)
    print "{0} seconds left till next poke..".format(refresh_seconds)
    time.sleep(float(refresh_seconds))
