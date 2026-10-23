# -*- coding: utf-8 -*-
"""Bo kiem thu hoi quy cua tuan 5.

Chay bang: python -m unittest discover tests
Bao gom bon bai kiem thu hoi quy cho:
1. HOTRO-1 tai find_login (SQL Injection)
2. HOTRO-1 tai search_products (SQL Injection)
3. HOTRO-2 tai search_page (Cross-Site Scripting - XSS)
4. HOTRO-3b tai _show_order (Insecure Direct Object Reference - IDOR)
"""

import os
import sys
import unittest

DIR_TESTS = os.path.dirname(os.path.abspath(__file__))
if DIR_TESTS not in sys.path:
    sys.path.insert(0, DIR_TESTS)

BASE = os.path.dirname(DIR_TESTS)
if BASE not in sys.path:
    sys.path.insert(0, BASE)

import db  # noqa: E402
import views  # noqa: E402
from khung_http import MayChuThu  # noqa: E402


class KiemThuTuan05(MayChuThu):
    """Bon bai kiem thu hoi quy cho cac ban va cua tuan 5."""

    def test_01_find_login_sql_injection(self):
        """Bai 1: db.find_login voi ten dang nhap chua cu phap SQL tra ve None."""
        ket_qua = db.find_login("lan' --", "matkhau1")
        self.assertIsNone(ket_qua)

    def test_02_search_products_sql_injection(self):
        """Bai 2: db.search_products voi chuoi tan cong tra ve danh sach rong."""
        ket_qua = db.search_products("' OR 1=1 --")
        self.assertEqual(ket_qua, [])

    def test_03_search_page_xss(self):
        """Bai 3: views.search_page voi tu khoa chua the kich ban khong tra ve the nay nguyen ven."""
        tu_khoa = "<script>alert(1)</script>"
        html_tra_ve = views.search_page(tu_khoa, [], None)
        self.assertNotIn("<script>alert(1)</script>", html_tra_ve)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html_tra_ve)

    def test_04_idor_order_detail(self):
        """Bai 4: Nguoi dung lan goi /don/4 nhan ma trang thai 404."""
        cookie_lan = self.dang_nhap("lan", "matkhau1")
        self.assertIsNotNone(cookie_lan, "Dang nhap tai khoan lan phai thanh cong")
        ma_trang_thai, _ = self.goi("/don/4", cookie=cookie_lan)
        self.assertEqual(ma_trang_thai, 404)


if __name__ == "__main__":
    unittest.main()
