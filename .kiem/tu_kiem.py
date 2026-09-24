# -*- coding: utf-8 -*-
"""Tu kiem kho bai lam hoc phan 04210 Bao mat phan mem, theo tung tuan.

Chay tren GitHub: the Actions, chon tu-kiem, bam Run workflow, chon tuan.
Chay tren may:    python .kiem/tu_kiem.py --tuan 5   (dung o thu muc goc cua kho)

Phep tu kiem xem ba viec: du tep cua tuan chua, co tep khong duoc dua len kho
khong, va (neu co git) du thong diep ghi nhan bat buoc chua; roi chay bo kiem
thu trong thu muc tests. No KHONG cham diem va KHONG kiem ban va dung hay sai.
Dat phep tu kiem chi co nghia bai du dieu kien de nguoi cham mo ra.
Khong sua tep nay. Chi dung thu vien chuan Python.
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUOI_ANH = (".png", ".jpg", ".jpeg")
TEP_CAM = re.compile(r"(^|/)([^/]+\.db|__pycache__/.*|\.env)$")


def danh_sach_tep():
    ra = []
    for g, ds, ts in os.walk(GOC):
        ds[:] = [d for d in ds if d != ".git"]
        for t in ts:
            ra.append(os.path.relpath(os.path.join(g, t), GOC).replace(os.sep, "/"))
    return set(ra)


def co_tep(p, tep):
    if p.endswith(".png"):
        return any(p[:-4] + d in tep for d in DUOI_ANH)
    return p in tep


def thong_diep_da_co():
    try:
        r = subprocess.run(["git", "log", "--format=%s"], cwd=GOC, capture_output=True,
                           text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0:
        return None
    return set(d.strip() for d in r.stdout.splitlines())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tuan", type=int, required=True)
    a = ap.parse_args()
    with open(os.path.join(GOC, ".kiem", "quy-uoc.json"), encoding="utf-8") as fh:
        qu = json.load(fh)
    q = qu.get(str(a.tuan))
    if q is None:
        print("Tuan phai tu 1 toi 10.")
        return 2
    tep = danh_sach_tep()
    loi = 0
    print("TU KIEM TUAN %d" % a.tuan)
    print("=" * 60)
    thieu = [p for p in q["bat_buoc"] if not co_tep(p, tep)]
    for p in q["bat_buoc"]:
        print("  [%s] %s" % ("CO  " if p not in thieu else "THIEU", p))
    for p in q["nen_co"]:
        print("  [%s] %s (nen co)" % ("CO  " if co_tep(p, tep) else "chua", p))
    loi += len(thieu)
    cam = sorted(p for p in tep if TEP_CAM.search(p))
    for p in cam:
        print("  [CAM ] %s: khong duoc dua len kho, xoa tep nay" % p)
    loi += len(cam)
    if q["thong_diep"]:
        da = thong_diep_da_co()
        if da is None:
            print("  (khong doc duoc lich su git, bo qua phan thong diep ghi nhan)")
        else:
            for t in q["thong_diep"]:
                ok = t in da
                print("  [%s] thong diep: %s" % ("CO  " if ok else "THIEU", t))
                loi += 0 if ok else 1
    if q.get("nhanh") and q["nhanh"] != "main":
        print("  Luu y: bai tuan nay nop tren nhanh %s." % q["nhanh"])
    print("-" * 60)
    if os.path.isdir(os.path.join(GOC, "tests")):
        print("Chay bo kiem thu: python -m unittest discover -s tests")
        env = dict(os.environ, MINISHOP_DB=os.path.join(GOC, ".kiem", "tu-kiem.db"), PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                           cwd=GOC, env=env, capture_output=True, text=True, timeout=300)
        dong = [d for d in r.stderr.strip().splitlines() if d.strip()]
        print("\n".join(dong[-12:]))
        if r.returncode != 0:
            loi += 1
        try:
            os.remove(env["MINISHOP_DB"])
        except OSError:
            pass
    print("=" * 60)
    if loi:
        print("CHUA DAT: %d muc can xu ly truoc khi nop." % loi)
        return 1
    print("DAT: du tep, khong co tep cam, bo kiem thu chay ra OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
