#!/usr/bin/python3

import re
import requests
from typing import Any
from bs4 import BeautifulSoup


class Payload:
    username: str = "ctl00$ContentPlaceHolder1$loginframe$UserName"
    password: str = "ctl00$ContentPlaceHolder1$loginframe$Password"
    captcha: str = "ctl00$ContentPlaceHolder1$capres"
    login_btn: str = "ctl00$ContentPlaceHolder1$loginframe$LoginButton"
    captcha_btn: str = "ctl00$ContentPlaceHolder1$submitCaptch"

    def __init__(self, 
                 username: str = None, 
                 password: str = None,
                 login_btn: str = "Sign+In"):

        self._data = {}
        self._data[Payload.username] = username
        self._data[Payload.password] = password
        self._data[Payload.login_btn] = login_btn

    def set_username(self, username: str) -> None:
        self._data[Payload.username] = username

    def set_password(self, password: str) -> None:
        self._data[Payload.password] = password
    
    def set_login_btn(self, login_btn: str = "Sign+In") -> None:
        self._data[Payload.login_btn] = login_btn

    def set_login(self, username: str, password: str, login_btn: str = "Sign+In") -> None:
        self.set_username(username)
        self.set_password(password)
        self.set_login_btn(login_btn)

    def set_captcha(self, captcha: str, captcha_btn: str = "Submit") -> None:
        self._data[Payload.captcha] = captcha
        self._data[Payload.captcha_btn] = captcha_btn

    def set_captcha_btn(self, captcha_btn: str = "Submit") -> None:
        self._data[Payload.captcha_btn] = captcha_btn

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    @property
    def data(self) -> dict:
        return self._data



class YADSL:
    '''
    Usage
    -----

    yadsl = YADSL(
        user: str = "xxxxxx",
        password: str = "...",
        lang: str = "en",
        cookies: dict = None,
    )

    yadsl.login() -> int
    yadsl.fetch_captcha() -> bytes
    yadsl.verify(captcha: str = "xxxx") -> int
    yadsl.fetch_data(cookies: dict = None) -> dict
    '''

    URL = "https://adsl.yemen.net.ye"

    def __init__(self, 
                 username: str, 
                 password: str, 
                 *,
                 lang: str = "en", 
                 cookies: dict = None):

        self._username = username
        self._password = password
        self._lang = lang
        self._cookies = cookies
        self._payload = Payload(username, password)

        self.init_session(cookies)

    def init_session(self, cookies: dict = None):
        self._session = requests.Session()
        if cookies is not None:
            self.set_cookies(cookies)

    def login(self, username: str = None, password: str = None) -> int:

        if username is not None:
            self._payload.set_username(username)

        if password is not None:
            self._payload.set_password(password)

        ## Login GET
        _login_get = self._session.get(self._login_url)
        _login_get_soup = BeautifulSoup(_login_get.content, "lxml")
        for _input in _login_get_soup.find("form", attrs={"name": "aspnetForm"}).find_all("input"):
            _name = _input.attrs.get("name")
            if _name.startswith("_"):
                self._payload.set(_name, _input.attrs.get("value"))

        ## Login POST
        _login_post = self._session.post(self._login_url, data=self._payload.data, allow_redirects=True)
        _login_post_soup = BeautifulSoup(_login_post.content, "lxml")
        for _input in _login_post_soup.find("form", attrs={"name": "aspnetForm"}).find_all("input"):
            _name = _input.attrs.get("name")
            if _name.startswith("_"):
                _value = _input.attrs.get("value")
                self._payload.set(_name, _value)

        return _login_post.status_code

    def verify(self, captcha: str) -> int:
        self._payload.set_captcha(captcha)
        _req = self._session.post(self._login_url, data=self._payload.data)
        return _req.status_code

    def fetch_data(self, cookies: dict = None) -> dict:
        if cookies is not None:
            self.set_cookies(cookies)

        _data = {}
        _request = self._session.get(self._user_url)
        _request_soup = BeautifulSoup(_request.content, "lxml")

        name = _request_soup.find("span", id="ctl00_labWelcome").text.strip()
        labels = _request_soup.find_all("td", class_="td_mc")
        values = _request_soup.find_all("span", attrs={"id": re.compile(r"ctl00_ContentPlaceHolder1_\d+")})

        _data[("الاسم" if self._lang.lower() == "ar" else "name")] = name.split(":")[-1].strip()
        _data.update({k.text.strip().lower(): v.text.strip().lower() for k, v in zip(labels, values)})

        return _data

    def fetch_captcha(self) -> bytes:
        return self._session.get(self._captcha_url).content

    def auto_login(self, 
                   captcha: str,
                   username: str = None,
                   password: str = None) -> tuple[int, int]:

        _login_status_code = self.login(username, password)
        _verify_status_code = self.verify(captcha)
        return (_login_status_code, _verify_status_code)

    def get_cookies(self) -> dict:
        return requests.utils.dict_from_cookiejar(self._session.cookies)

    def set_cookies(self, cookies: dict):
        return self._session.cookies.update(requests.utils.cookiejar_from_dict(cookies))

    def export_cookies(self) -> dict:
        return self.get_cookies()

    def import_cookies(self, cookies: dict):
        return self.set_cookies(cookies)

    def clear_cookies(self):
        self._session.cookies.clear()
        self._session.cookies.clear_expired_cookies()

    @property
    def _login_url(self) -> str:
        return f"{self.URL}/{self._lang}/login.aspx"

    @property
    def _user_url(self) -> str:
        return f"{self.URL}/{self._lang}/user_main.aspx"

    @property
    def _captcha_url(self) -> str:
        return f"{self.URL}/captcha/docap.aspx?new=1"
