"""彩色分等级日志（内部诊断用；默认 stderr+WARNING，单例 `Log`）。

与 591iqAutomatic 的 Common/Logcat.py 同契约：结论一律 print 走 stdout，
内部诊断一律走这里走 stderr，二者不得混用。
"""
import os
import sys

_LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}
_VERBOSE = os.environ.get("XMYZ_VERBOSE") == "1"


def setVerbose(on: bool) -> None:
    global _VERBOSE
    _VERBOSE = bool(on)


def _color(text: str, code: str) -> str:
    if not sys.stderr.isatty():
        return text
    return "\033[%sm%s\033[0m" % (code, text)


class _Log:
    def __init__(self):
        self.enabled = True

    def _emit(self, level: str, tag: str, msg: str) -> None:
        if not self.enabled or _LEVELS[level] < _LEVELS["DEBUG"] and not _VERBOSE:
            return
        color = {"DEBUG": "36", "INFO": "32", "WARN": "33", "ERROR": "31"}[level]
        sys.stderr.write(_color("[%s][%s] %s" % (level, tag, msg), color) + "\n")

    def d(self, tag: str, msg: str) -> None:
        self._emit("DEBUG", tag, msg)

    def i(self, tag: str, msg: str) -> None:
        self._emit("INFO", tag, msg)

    def w(self, tag: str, msg: str) -> None:
        self._emit("WARN", tag, msg)

    def e(self, tag: str, msg: str) -> None:
        self._emit("ERROR", tag, msg)


Log = _Log()