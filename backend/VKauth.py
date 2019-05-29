import requests
import getpass

class VKAuth(object):

    def __init__(self, permissions, app_id, api_v, email=None, pswd=None, two_factor_auth=False, security_code=None, auto_access=True):
        """
        Args:
            permissions: list of Strings with permissions to get from API
            app_id: (String) vk app id that one can get from vk.com
            api_v: (String) vk API version
        """

        self.session        = requests.Session()
        self.form_parser    = FormParser()
        self.user_id        = None
        self.access_token   = None
        self.response       = None

        self.permissions    = permissions
        self.api_v          = api_v
        self.app_id         = app_id
        self.two_factor_auth= two_factor_auth
        self.security_code  = security_code
        self.email          = email
        self.pswd           = pswd
        self.auto_access    = auto_access

        if security_code != None and two_factor_auth == False:
            raise RuntimeError('Security code provided for non-two-factor authorization')

        def authorize(self):
            api_auth_url = 'https://oauth.vk.com/authorize'
            app_id = self.app_id
            permissions = self.permissions
            redirect_uri = 'https://oauth.vk.com/blank.html'
            display = 'wap'
            api_version = self.api_v

            auth_url_template = '{0}?client_id={1}&scope={2}&redirect_uri={3}&display={4}&v={5}&response_type=token'
            auth_url = auth_url_template.format(api_auth_url, app_id, ','.join(permissions), redirect_uri, display, api_version)

            self.response = self.session.get(auth_url)

            # look for <form> element in response html and parse it
            if not self._parse_form():
                raise RuntimeError('No <form> element found. Please, check url address')
                # look for <form> element in response html and parse it
                if not self._parse_form():
                    raise RuntimeError('No <form> element found. Please, check url address')
                else:
                    # try to log in with email and password (stored or expected to be entered)
                    while not self._log_in():
                        pass;

                    # handling two-factor authentication
                    # expecting a security code to enter here
                    if self.two_factor_auth:
                        self._two_fact_auth()

        def _log_in(self):

            if self.email == None:
                self.email = ''
                while self.email.strip() == '':
                    self.email = input('Enter an email to log in: ')

            if self.pswd == None:
                self.pswd = ''
                while self.pswd.strip() == '':
                    self.pswd = getpass.getpass('Enter the password: ')

            self._submit_form({'email': self.email, 'pass': self.pswd})
            if not self._parse_form():
                raise RuntimeError('No <form> element found. Please, check url address')

            # if wrong email or password
            if 'pass' in self.form_parser.params:
                print('Wrong email or password')
                self.email = None
                self.pswd = None
                return False
            elif 'code' in self.form_parser.params and not self.two_factor_auth:
                raise RuntimeError(
                    'Two-factor authentication expected from VK.\nChange `two_factor_auth` to `True` and provide a security code.')
            else:
                return True

        def _two_fact_auth(self):

            prefix = 'https://m.vk.com'
            if prefix not in self.form_parser.url:
                self.form_parser.url = prefix + self.form_parser.url

            if self.security_code == None:
                self.security_code = input('Enter security code for two-factor authentication: ')

            self._submit_form({'code': self.security_code})

            if not self._parse_form():
                raise RuntimeError('No <form> element found. Please, check url address')

        # allow vk to use this app and access self.permissions
        self._allow_access()

        # now get access_token and user_id
        self._get_params()

        def _allow_access(self):
            parser = self.form_parser

            if 'submit_allow_access' in parser.params and 'grant_access' in parser.url:
                if not self.auto_access:
                    answer = ''
                    msg = 'Application needs access to the following details in your profile:\n' + \
                          str(self.permissions) + '\n' + \
                          'Allow it to use them? (yes or no)'

                    attempts = 5
                    while answer not in ['yes', 'no'] and attempts > 0:
                        answer = input(msg).lower().strip()
                        attempts -= 1

                    if answer == 'no' or attempts == 0:
                        self.form_parser.url = self.form_parser.denial_url
                        print('Access denied')

                self._submit_form({})

        def _get_params(self):
            try:
                params = self.response.url.split('#')[1].split('&')
                self.access_token = params[0].split('=')[1]
                self.user_id = params[2].split('=')[1]
            except IndexError(e):
                print(e)
                print('Coudln\'t fetch token')