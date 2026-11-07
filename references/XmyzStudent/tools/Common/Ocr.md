# Ocr — 验证码识别（学社子树自包含）

与 CampusNet 子树 `Access/LoginSession.py` 的验证码预处理/变体投票同源同参
（591iq 实测参数）：`CAPTCHA_VARIANTS = [(170,3),(180,4),(200,4)]`，
数字→形近字母映射，必要长度 4~5 位。

- `preprocess(path, out, scale, threshold)` — 二值化反色 + 放大
- `ocrCaptcha(path)` — 多变体投票，返回 4~5 位小写字母或 `''`

学社 `HubSession.py --ocr` 兜底使用；优先 vision/token。
