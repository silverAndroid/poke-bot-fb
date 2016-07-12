import getpass
import pickle

import requests
from bs4 import BeautifulSoup




def __delete_cookies__(filename):
    import os
    os.remove(filename)


class Login:
    def __init__(self, cookies_filename='cookies'):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14",
            "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,"
                      "*/*;q=0.5",
            "Accept-Language": "en-us,en;q=0.5",
            "Accept-Charset": "ISO-8859-1",
            "Content-type": "application/poke_page-www-form-urlencoded",
            "Host": "m.facebook.com"
        }
        self.cookies_filename = cookies_filename
        self.session = requests.session()
        self.session.headers = self.headers

        self.__init_fb__()

    def __load_cookies__(self, filename):
        with open(filename) as f:
            self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))

    def __init_fb__(self):
        print "Loading Facebook..."
        load_facebook_request = self.session.get('https://m.facebook.com')
        self.soup = BeautifulSoup(load_facebook_request.text, 'html.parser')
        print "Loaded Facebook!"

    def __check_session__(self):
        try:
            poke_url = 'https://m.facebook.com/pokes'
            self.__load_cookies__(self.cookies_filename)
            check_logged_in = self.session.get(poke_url)
            if '/login' in check_logged_in.url:
                print 'Session has expired. Please log in again.'
                __delete_cookies__(self.cookies_filename)
            return '/login' not in check_logged_in.url
        except IOError as e:
            if 'No such file or directory' not in e.strerror:
                raise

    def __save_cookies__(self, filename):
        with open(filename, 'w') as f:
            pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

    def __return_params__(self, login_form, email, password):
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

        return {'lsd': lsd, 'charset_test': charset_test, 'version': version, 'ajax': ajax, 'width': width,
                'pxr': pxr, 'gps': gps, 'dimensions': dimensions, 'm_ts': m_ts, 'li': li, 'login': login,
                'email': email, 'pass': password, 'login_url': login_url}

    def login(self):
        print "Login to Facebook"
        logged_in = self.__check_session__()
        login_response = {'cookies': self.session.cookies, 'session': self.session, 'logged_in': logged_in}
        if not logged_in:
            email = raw_input("Email: ")
            password = getpass.getpass("Password: ")
            cookies_save = ''
            while cookies_save is not 'y' or not 'n':
                cookies_save = raw_input('Stay logged in? (y/n) ')
            cookies_save = cookies_save == 'y'

            login_form = self.soup.findAll('div', {'class': 'g'})[0] \
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
            params = self.__return_params__(login_form, email, password)
            login_url = params['login_url']
            del params['login_url']

            print "Logging into Facebook..."
            login_request = self.session.post(login_url, data=params, headers=self.headers)
            if '/login' not in login_request.url:
                if cookies_save:
                    self.__save_cookies__(self.cookies_filename)
                    login_response['logged_in'] = True
            else:
                login_response['logged_in'] = False
        return login_response
