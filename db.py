# -*- coding: utf-8 -*-
"""Moi truy cap co so du lieu cua MiniShop nam trong module nay.

Moi ham tu mo mot ket noi rieng roi dong lai, nen an toan khi may chu
xu ly nhieu yeu cau tren nhieu luong khac nhau.
"""

import hashlib
import os
import secrets
import sqlite3
import time

# Duong dan co so du lieu. Bo kiem thu dat bien moi truong de dung tep tam.
DB_PATH = os.environ.get(
    "MINISHOP_DB",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "minishop.db"),
)


def connect():
    """Mo mot ket noi moi, tra ve moi hang duoi dang ban ghi truy cap theo ten cot."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password, salt=None):
    """Bam mat khau bang ham dan xuat khoa cham co muoi, tra ve chuoi muoi:bam."""
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), 600000
    ).hex()
    return salt + ":" + digest


def verify_password(password, stored):
    """So khop mat khau voi gia tri da luu, dung phep so sanh thoi gian co dinh."""
    if ":" not in stored:
        return False
    salt = stored.split(":", 1)[0]
    return secrets.compare_digest(hash_password(password, salt), stored)


def find_login(username, password):
    """Tim nguoi dung khop ten dang nhap va mat khau. Tra ve ban ghi hoac None."""
    conn = connect()
    try:
        sql = "SELECT * FROM users WHERE username = '" + username + "'"
        row = conn.execute(sql).fetchone()
        if row is None:
            return None
        if not verify_password(password, row["password_md5"]):
            return None
        return row
    finally:
        conn.close()


def search_products(keyword):
    """Tim san pham theo tu khoa trong ten. Tra ve danh sach ban ghi."""
    conn = connect()
    try:
        sql = "SELECT * FROM products WHERE name LIKE '%" + keyword + "%' ORDER BY id"
        return conn.execute(sql).fetchall()
    finally:
        conn.close()


def list_products():
    """Liet ke toan bo san pham theo thu tu ma."""
    conn = connect()
    try:
        return conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    finally:
        conn.close()


def get_product(product_id):
    """Lay mot san pham theo ma. Tra ve ban ghi hoac None."""
    conn = connect()
    try:
        return conn.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        ).fetchone()
    finally:
        conn.close()


def get_user(user_id):
    """Lay mot nguoi dung theo ma. Tra ve ban ghi hoac None."""
    conn = connect()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    finally:
        conn.close()


def list_users():
    """Liet ke toan bo nguoi dung, phuc vu trang quan tri."""
    conn = connect()
    try:
        return conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    finally:
        conn.close()


def list_orders_for_user(user_id):
    """Liet ke don hang cua mot nguoi dung, kem ten san pham."""
    conn = connect()
    try:
        return conn.execute(
            "SELECT o.*, p.name AS product_name FROM orders o "
            "JOIN products p ON p.id = o.product_id "
            "WHERE o.user_id = ? ORDER BY o.id",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()


def get_order(order_id):
    """Lay mot don hang theo ma, kem ten san pham. Tra ve ban ghi hoac None."""
    conn = connect()
    try:
        return conn.execute(
            "SELECT o.*, p.name AS product_name FROM orders o "
            "JOIN products p ON p.id = o.product_id WHERE o.id = ?",
            (order_id,),
        ).fetchone()
    finally:
        conn.close()


def buy_product(user_id, product_id, quantity):
    """Tru ton kho va tao don hang moi. Tra ve True neu mua duoc."""
    conn = connect()
    try:
        row = conn.execute(
            "SELECT price, stock FROM products WHERE id = ?", (product_id,)
        ).fetchone()
        if row is None:
            return False
        if row["stock"] >= quantity:
            time.sleep(0.05)
            conn.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (quantity, product_id),
            )
            conn.execute(
                "INSERT INTO orders (user_id, product_id, quantity, total, created_at) "
                "VALUES (?, ?, ?, ?, datetime('now'))",
                (user_id, product_id, quantity, row["price"] * quantity),
            )
            conn.commit()
            return True
        return False
    finally:
        conn.close()
