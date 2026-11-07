"""验证码 OCR（学社子树自包含版）。

来源：与 CampusNet 子树 `Access/LoginSession.py` 的验证码预处理/投票逻辑同源
（591iq 同参数，实测有效）。学社子树不依赖 CampusNet 的 `Access/` 包名，
故抽出这一份最小实现；两处参数若需同步，改这边即可（视觉优先，OCR 仅兜底）。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 变体池：`(阈值, 放大倍数)`，与 CampusNet/591iq 同源同参
CAPTCHA_VARIANTS = [(170, 3), (180, 4), (200, 4)]
DIGIT2LETTER = str.maketrans("0123456789", "olzeasgbgg")


def preprocess(path, out=None, scale=3, threshold=160):
    """红字白底验证码 → 黑字白底 → 放大。"""
    from PIL import Image
    import numpy as np
    im = Image.open(path).convert("L")
    a = np.array(im)
    im2 = Image.fromarray(255 - (a < threshold).astype("uint8") * 255)
    im3 = im2.resize((im2.width * scale, im2.height * scale), Image.LANCZOS)
    out = out or (str(path) + ".prep.png")
    im3.save(out)
    return out


def cleanCode(text: str) -> str:
    t = text.strip().lower().translate(DIGIT2LETTER)
    return "".join(ch for ch in t if "a" <= ch <= "z")


def _ocrOnce(ocr, path):
    res, _ = ocr(path)
    if not res:
        return "", 0.0
    res = sorted(res, key=lambda r: min(p[0] for p in r[0]))
    joined = cleanCode("".join(r[1] for r in res))
    return joined, sum(float(r[2]) for r in res) / len(res)


def ocrCaptcha(path: str) -> str:
    """多预处理变体投票。返回 4~5 位小写字母串，无合法长度候选则返回 ''。"""
    made = []
    for t, s in CAPTCHA_VARIANTS:
        o = "%s.t%d_s%d.png" % (path, t, s)
        made.append(((t, s), preprocess(path, out=o, threshold=t, scale=s)))
    try:
        from rapidocr_onnxruntime import RapidOCR
        ocr = RapidOCR()
    except Exception:
        return ""
    cands = []
    for (t, s), f in made:
        code, conf = _ocrOnce(ocr, f)
        if len(code) in (4, 5):
            cands.append((code, conf))
    if not cands:
        return ""
    votes = {}
    for code, conf in cands:
        slot = votes.setdefault(code, [0, 0.0])
        slot[0] += 1
        slot[1] = max(slot[1], conf)
    return max(votes, key=lambda k: (votes[k][0], votes[k][1]))
