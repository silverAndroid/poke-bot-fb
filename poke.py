import re
import time

from bs4 import BeautifulSoup

import login

poke_url = 'https://m.facebook.com/pokes'


def poke(session):
    global poke_url
    poke_page = session.get(poke_url)
    # print poke_page.text

    soup = BeautifulSoup(poke_page.text, 'html.parser')

    poke_container = soup.findAll('div', {'class': 'g'})[0] \
        .findAll('table', {'class': 'n'})[0] \
        .findAll('tr')[0] \
        .findAll('td', {'class': 'u'})[0] \
        .findAll('div', {'id': 'poke_area'})[0]

    i = 0
    while True:
        try:
            poke_name = poke_container.findAll('div', {'class': 'bq'})[i + 1] \
                .findAll('div', {'class': ['bx', 'bw']})[0].text
            substrings = [m.start() for m in
                          re.finditer('( poked you [0-9]+ times in a row)', poke_name.replace(',', ''))]

            poke_link = poke_container.findAll('div', {'class': 'bq'})[i] \
                .findAll('div')[7] \
                .findAll('a', {'class': ['ca', 'bz']})[0]['href']
        except IndexError:
            break

        # print poke_container
        # print poke_link
        poke_response = session.get('https://m.facebook.com' + poke_link)
        # print poke_response.text

        if "poke_status=success" in poke_response.url:
            time_formatted = time.strftime("%H:%M %Z")
            print 'Successfully poked {0} at {1}!'.format(poke_name[:substrings[0]].strip(), time_formatted)
        i += 2
    if i == 0:
        print 'No one to poke :('


if __name__ == '__main__':
    login_obj = login.Login()
    login_response = {'logged_in': False}
    while not login_response['logged_in']:
        login_response = login_obj.login()
        if login_response['logged_in']:
            print 'Logged into Facebook!'
        else:
            print "Your email or password is incorrect. Please try again.."

    refresh_seconds = raw_input('How many seconds would you like the bot to wait before checking for new pokes? ')

    while True:
        poke(login_response['session'])
        print "{0} seconds left till next poke..".format(refresh_seconds)
        time.sleep(float(refresh_seconds))
