# -*- coding: utf-8 -*-
"""Bo kiem thu hoi quy cua tuan 4.

Chay bang:  python -m unittest discover tests
Kiem thu hoi quy cho ban va HOTRO-3a: kiem tra vai tro phia may chu khi
truy cap trang quan tri (/admin).
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
sys.path.insert(0, BASE)

_TMP_DB = os.path.join(tempfile.gettempdir(), "minishop_tuan03.db")
if os.path.exists(_TMP_DB):
    os.remove(_TMP_DB)
os.environ["MINISHOP_DB"] = _TMP_DB

import app  # noqa: E402
import db  # noqa: E402
import seed  # noqa: E402

CONG = 8041
GOC = "http://127.0.0.1:" + str(CONG)


def _mo(path, cookie=None, data=None):
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


class NenKiemThu(unittest.TestCase):
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

    def _dang_nhap(self, ten, mat_khau):
        """Dang nhap roi tra ve chuoi cookie phien."""
        body = urlencode({"username": ten, "password": mat_khau}).encode("utf-8")
        resp = _KhongTheoChuyenHuong().open(Request(GOC + "/login", data=body))
        dat_cookie = resp.headers.get("Set-Cookie")
        self.assertIsNotNone(dat_cookie, "dang nhap that bai, khong nhan duoc cookie")
        return dat_cookie.split(";")[0]


class KiemThuHoTro3a(NenKiemThu):
    """HOTRO-3a: kiem tra vai tro quan tri vien phia may chu."""

    def test_nguoi_vai_tro_thuong_nhan_ma_403(self):
        """Phep kiem 1: nguoi vai tro thuong goi trang quan tri thi nhan ma 403."""
        cookie = self._dang_nhap("lan", "matkhau1")
        ma, than = _mo("/admin", cookie=cookie)
        self.assertEqual(ma, 403)
        self.assertIn("Tu choi", than)

    def test_than_phan_hoi_khong_chua_email(self):
        """Phep kiem 2: than phan hoi khong chua dia chi email cua nguoi dung nao."""
        cookie = self._dang_nhap("lan", "matkhau1")
        ma, than = _mo("/admin", cookie=cookie)
        self.assertEqual(ma, 403)
        self.assertNotIn("@", than)

    def test_quan_tri_vien_van_nhan_ma_200(self):
        """Phep kiem 3: quan tri vien van nhan ma 200 va xem duoc danh sach nguoi dung."""
        cookie = self._dang_nhap("quantri", "admin123")
        ma, than = _mo("/admin", cookie=cookie)
        self.assertEqual(ma, 200)
        self.assertIn("Quan tri nguoi dung", than)


if __name__ == "__main__":
    unittest.main()
