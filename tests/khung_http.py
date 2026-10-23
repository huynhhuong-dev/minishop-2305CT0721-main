# -*- coding: utf-8 -*-
"""Khung kiem thu HTTP cho MiniShop.

Phat san cho sinh vien tu tuan 5 de thuc hien cac bai kiem thu hoi quy
can may chu HTTP hoat dong va dang nhap nguoi dung.
"""

import os
import sys
import tempfile
import threading
import time
import unittest
from http.server import ThreadingHTTPServer
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

_TMP_DB = os.path.join(tempfile.gettempdir(), "minishop_tuan05.db")
if os.path.exists(_TMP_DB):
    try:
        os.remove(_TMP_DB)
    except OSError:
        pass
os.environ["MINISHOP_DB"] = _TMP_DB

import app  # noqa: E402
import db  # noqa: E402
import seed  # noqa: E402

CONG = 8051
GOC = "http://127.0.0.1:" + str(CONG)


def goi(path, cookie=None, data=None):
    """Goi mot duong dan, tra ve (ma trang thai, than phan hoi)."""
    headers = {}
    if cookie:
        headers["Cookie"] = cookie
    body = urlencode(data).encode("utf-8") if data is not None else None
    req = Request(GOC + path, data=body, headers=headers)
    try:
        resp = urlopen(req)
        return resp.status, resp.read().decode("utf-8")
    except HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")


class _KhongTheoChuyenHuong:
    """Mo mot duong dan nhung khong di theo chuyen huong, de doc duoc cookie."""

    def open(self, req):
        import urllib.request

        class _H(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args):
                return None

        opener = urllib.request.build_opener(_H)
        try:
            return opener.open(req)
        except HTTPError as exc:
            return exc


def dang_nhap(ten, mat_khau):
    """Dang nhap roi tra ve chuoi cookie phien."""
    body = urlencode({"username": ten, "password": mat_khau}).encode("utf-8")
    resp = _KhongTheoChuyenHuong().open(Request(GOC + "/login", data=body))
    dat_cookie = resp.headers.get("Set-Cookie")
    if not dat_cookie:
        return None
    return dat_cookie.split(";")[0]


class MayChuThu(unittest.TestCase):
    """Lop nen: tao co so du lieu tam va khoi dong may chu mot lan."""

    @classmethod
    def setUpClass(cls):
        db.DB_PATH = _TMP_DB
        conn = db.connect()
        seed.ensure_db(conn)
        conn.close()
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", CONG), app.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def dang_nhap(self, ten, mat_khau):
        """Phuong thuc tien ich goi ham dang_nhap cap module."""
        return dang_nhap(ten, mat_khau)

    def goi(self, path, cookie=None, data=None):
        """Phuong thuc tien ich goi ham goi cap module."""
        return goi(path, cookie=cookie, data=data)
