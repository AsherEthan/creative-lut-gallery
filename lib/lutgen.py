"""lutgen.py — 創意風格 LUT 圖鑑的參數模型（與網站使用同一套演算法）。

用法：
    from lutgen import make_transform, generate_cube
    look = json.load(open("api/looks/kodak_2383.json"))
    text = generate_cube(look, size=33, intensity=0.8)
"""

DEFAULTS = dict(exp=0, temp=0, tint=0, sat=1, con=1, piv=0.45, lift=[0, 0, 0], gam=[1, 1, 1],
                gain=[1, 1, 1], sh=[0, 0, 0], hi=[0, 0, 0], fade=0, roll=1, mix=None, bw=None)


def _cl(v):
    return 0.0 if v < 0 else 1.0 if v > 1 else v


def make_transform(params=None):
    """回傳 fn(r, g, b) -> (r, g, b)，輸入輸出皆為 0–1 的 Rec.709 顯示值。"""
    P = dict(DEFAULTS)
    P.update({k: v for k, v in (params or {}).items() if v is not None or k in ("mix", "bw")})
    em = 2 ** P["exp"]
    wr, wg, wb = em * (1 + 0.12 * P["temp"]), em * (1 - 0.08 * P["tint"]), em * (1 - 0.12 * P["temp"])
    ig = [1 / g for g in P["gam"]]
    m, bw, c, pv, s, fd = P["mix"], P["bw"], P["con"], P["piv"], P["sat"], P["fade"]
    rg = P["roll"] - fd
    LI, GA, SH, HI = P["lift"], P["gain"], P["sh"], P["hi"]

    def sc(v):
        return pv * (v / pv) ** c if v < pv else 1 - (1 - pv) * ((1 - v) / (1 - pv)) ** c

    def lg(v, i):
        v = _cl(GA[i] * (v + LI[i] * (1 - v)))
        return v if ig[i] == 1 else v ** ig[i]

    def fn(r, g, b):
        r, g, b = r * wr, g * wg, b * wb
        if m:
            r, g, b = (m[0] * r + m[1] * g + m[2] * b, m[3] * r + m[4] * g + m[5] * b, m[6] * r + m[7] * g + m[8] * b)
        if bw:
            r = g = b = bw[0] * r + bw[1] * g + bw[2] * b
        r, g, b = _cl(r), _cl(g), _cl(b)
        if c != 1:
            r, g, b = sc(r), sc(g), sc(b)
        l = 0.2126 * r + 0.7152 * g + 0.0722 * b
        r, g, b = _cl(l + (r - l) * s), _cl(l + (g - l) * s), _cl(l + (b - l) * s)
        r, g, b = lg(r, 0), lg(g, 1), lg(b, 2)
        l = 0.2126 * r + 0.7152 * g + 0.0722 * b
        ws, wh = (1 - l) * (1 - l), l * l
        r += SH[0] * ws + HI[0] * wh
        g += SH[1] * ws + HI[1] * wh
        b += SH[2] * ws + HI[2] * wh
        return _cl(fd + _cl(r) * rg), _cl(fd + _cl(g) * rg), _cl(fd + _cl(b) * rg)

    return fn


def generate_cube(look, size=33, intensity=1.0, decimals=6):
    """look 可以是 API 的風格 JSON（含 params），也可以直接是參數 dict。回傳 .cube 文字。"""
    params = look.get("params", look) if isinstance(look, dict) else {}
    fn = make_transform(params)
    k = float(intensity)
    raw = str(look.get("name_en") or look.get("id") or "Creative LUT") if isinstance(look, dict) else "Creative LUT"
    title = "".join(ch for ch in raw if 32 <= ord(ch) < 127).replace('"', "'").strip() or "Creative LUT"
    out = ['TITLE "%s"' % title,
           "# Creative LUT approximation - Creative LUT Gallery",
           "# Input: Rec.709 display-referred. Intensity: %d%%" % round(k * 100),
           "LUT_3D_SIZE %d" % size,
           "DOMAIN_MIN 0.0 0.0 0.0",
           "DOMAIN_MAX 1.0 1.0 1.0"]
    n = size - 1
    f = "%%.%df %%.%df %%.%df" % (decimals, decimals, decimals)
    for bi in range(size):
        B = bi / n
        for gi in range(size):
            G = gi / n
            for ri in range(size):
                R = ri / n
                o = fn(R, G, B)
                out.append(f % (R + (o[0] - R) * k, G + (o[1] - G) * k, B + (o[2] - B) * k))
    return "\n".join(out) + "\n"
