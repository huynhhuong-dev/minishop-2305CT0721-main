# -*- coding: utf-8 -*-
"""Bo kiem thu hoi quy cua tuan 3.

Chay bang:  python -m unittest discover tests
Sinh vien them MOT lop kiem thu cua minh vao cuoi tep nay, cho HOTRO-5
hoac cho HOTRO-8.
"""

import hashlib
import os
import re
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

CONG = 8031
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


class KiemThuHoTro4(NenKiemThu):
    """HOTRO-4: bam mat khau phai cham va phai co muoi."""

    def test_gia_tri_bam_khong_con_la_md5_tran(self):
        gia_tri = db.hash_password("admin123")
        self.assertIsNone(
            re.fullmatch(r"[0-9a-f]{32}", gia_tri),
            "gia tri bam van la 32 ky tu thap luc phan, tuc van la MD5 tran",
        )

    def test_hai_lan_bam_cung_mat_khau_cho_hai_ket_qua(self):
        self.assertNotEqual(
            db.hash_password("admin123"),
            db.hash_password("admin123"),
            "hai lan bam cho cung ket qua, tuc chua co muoi",
        )

    def test_van_dang_nhap_duoc_sau_khi_doi_luoc_do(self):
        cookie = self._dang_nhap("lan", "matkhau1")
        ma, than = _mo("/hoso", cookie=cookie)
        self.assertEqual(ma, 200)
        self.assertIn("Nguyễn Thị Lan", than)

    def test_khong_dang_nhap_duoc_bang_mat_khau_sai(self):
        ma, than = _mo("/login", data={"username": "lan", "password": "sai"})
        self.assertIn("Sai ten dang nhap hoac mat khau", than)


class KiemThuHoTro8(NenKiemThu):
    """HOTRO-8: ma phien ngau nhien, khong the doan duoc."""

    def test_ma_phien_khong_phai_so_tu_tang(self):
        sid1 = app._new_session_id()
        sid2 = app._new_session_id()
        # Ma phien phai co do dai an toan (it nhat 16 ky tu hex tro len)
        self.assertGreaterEqual(len(sid1), 16)
        # Ma phien khong duoc la so tu tang de doan (nhu '1', '2')
        self.assertFalse(sid1.isdigit(), "ma phien van la so tu tang, rat de doan")


if __name__ == "__main__":
    unittest.main()
