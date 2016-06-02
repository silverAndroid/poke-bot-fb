import getpass
import re
import time

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14",
    "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
    "Accept-Language": "en-us,en;q=0.5",
    "Accept-Charset": "ISO-8859-1",
    "Content-type": "application/poke_page-www-form-urlencoded",
    "Host": "m.facebook.com"
}


def login():
    # print soup.prettify()
    login_form = soup.findAll('div', {'class': 'g'})[0] \
        .findAll('div', {'id': 'viewport'})[0] \
        .findAll('div', {'id': 'objects_container'})[0] \
        .findAll('div', {'class': 's'})[0] \
        .findAll('table', {'class': 't'})[0] \
        .findAll('tr')[0] \
        .findAll('td', {'class': 'u'})[0] \
        .findAll('div')[2] \
        .findAll('div', {'class': 'z'})[0] \
        .findAll('form', {'id': 'login_form'})[0]
    # print login_form
    login_url = login_form['action']
    lsd = login_form.findAll('input', {'name': 'lsd'})[0]['value']
    charset_test = login_form.findAll('input', {'name': 'charset_test'})[0]['value']
    version = login_form.findAll('input', {'name': 'version'})[0]['value']
    ajax = login_form.findAll('input', {'name': 'ajax'})[0]['value']
    width = login_form.findAll('input', {'name': 'width'})[0]['value']
    pxr = login_form.findAll('input', {'name': 'pxr'})[0]['value']
    gps = login_form.findAll('input', {'name': 'gps'})[0]['value']
    dimensions = login_form.findAll('input', {'name': 'dimensions'})[0]['value']
    m_ts = login_form.findAll('input', {'name': 'm_ts'})[0]['value']
    li = login_form.findAll('input', {'name': 'li'})[0]['value']
    login = login_form.findAll('ul', {'class': 'bc'})[0] \
        .findAll('li', {'class': 'bd'})[2] \
        .findAll('input', {'name': 'login'})[0]['value']

    params = {'lsd': lsd, 'charset_test': charset_test, 'version': version, 'ajax': ajax, 'width': width, 'pxr': pxr,
              'gps': gps, 'dimensions': dimensions, 'm_ts': m_ts, 'li': li, 'login': login, 'email': email,
              'pass': password}

    print "Logging into Facebook..."
    login_request = session.post(login_url, data=params, headers=headers)
    return login_request


def poke():
    poke_page = session.get('https://m.facebook.com/pokes')
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


while True:
    session = requests.Session()
    print "Loading Facebook..."
    load_facebook_request = session.get('https://m.facebook.com')
    soup = BeautifulSoup(load_facebook_request.text, 'html.parser')
    print "Loaded Facebook!"

    print "Login to Facebook"
    email = raw_input("Email: ")
    password = getpass.getpass("Password: ")
    login_request = login()

    if '/login' not in login_request.url:
        break
    print 'Your email or password is incorrect. Please try again..'
print "Logged into Facebook!"

refresh_seconds = raw_input('How many seconds would you like the bot to wait before checking for new pokes? ')

while True:
    poke()
    print "{0} seconds left till next poke..".format(refresh_seconds)
    time.sleep(float(refresh_seconds))
