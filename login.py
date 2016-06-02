class Login:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.8.1.14) Gecko/20080609 Firefox/2.0.0.14",
            "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,"
                      "*/*;q=0.5",
            "Accept-Language": "en-us,en;q=0.5",
            "Accept-Charset": "ISO-8859-1",
            "Content-type": "application/poke_page-www-form-urlencoded",
            "Host": "m.facebook.com"
        }

    def login(self, soup, session):
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

        params = {'lsd': lsd, 'charset_test': charset_test, 'version': version, 'ajax': ajax, 'width': width,
                  'pxr': pxr,
                  'gps': gps, 'dimensions': dimensions, 'm_ts': m_ts, 'li': li, 'login': login, 'email': self.email,
                  'pass': self.password}

        print "Logging into Facebook..."
        login_request = session.post(login_url, data=params, headers=self.headers)
        return login_request
