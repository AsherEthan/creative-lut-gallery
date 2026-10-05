#!/usr/bin/env python3
"""從 API 資料產生任意網格尺寸／強度的 .cube 檔。

  python tools/build_cubes.py --size 33 --out cubes                 # 用 repo 內的 api/looks/*.json
  python tools/build_cubes.py --size 65 --intensity 0.7 --ids kodak_2383 teal_orange
  python tools/build_cubes.py --remote --size 33 --out cubes        # 直接讀線上 API
"""
import argparse, glob, json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
from lutgen import generate_cube  # noqa: E402

API = "https://asherethan.github.io/creative-lut-gallery/api"


def get_json(url):
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read().decode("utf-8"))


def load_looks(remote, ids):
    if remote:
        lst = get_json(API + "/looks.json")["looks"]
        return [get_json(API + "/looks/%s.json" % l["id"]) for l in lst if not ids or l["id"] in ids]
    out = []
    for p in sorted(glob.glob(os.path.join(HERE, "..", "api", "looks", "*.json"))):
        look = json.load(open(p, encoding="utf-8"))
        if not ids or look["id"] in ids:
            out.append(look)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=33, help="網格尺寸，例如 17 / 33 / 65")
    ap.add_argument("--intensity", type=float, default=1.0, help="強度 0–1")
    ap.add_argument("--out", default="cubes", help="輸出資料夾")
    ap.add_argument("--ids", nargs="*", help="只產生指定的風格 id")
    ap.add_argument("--remote", action="store_true", help="從線上 API 讀取")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    looks = load_looks(a.remote, set(a.ids or []))
    for look in looks:
        with open(os.path.join(a.out, look["id"] + ".cube"), "w", encoding="utf-8") as f:
            f.write(generate_cube(look, size=a.size, intensity=a.intensity))
    print("已產生 %d 個 .cube（%d³，強度 %d%%）到 %s/" % (len(looks), a.size, round(a.intensity * 100), a.out))


if __name__ == "__main__":
    main()
