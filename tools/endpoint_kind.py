#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""端点读写分类 —— 唯一权威判定, 被 merge 与 probe 共用。

旧 bug: 正则每个分支后硬接 `\\.action$`, `approve` 只能匹配 `approvedComplete`
的前 7 字母, 后面接不上 `.action` 而漏判, 审批写端点被当成只读探测。
新实现按「先取 action 名, 再做词元判定」, 不再用正则硬拼。
"""
import re

EP_RE = re.compile(r"^/?(?P<ns>[A-Za-z0-9_\-/]+?)!(?P<act>[A-Za-z0-9_]+)\.action$")

# 精确只读动作（优先于所有规则）
READ_EXACT = {
    "read", "list", "load", "detail", "detailJosn", "query", "search", "get",
    "find", "findRead", "count", "stat", "statInfo", "statByClassTeacher",
    "statByGradeTeacher", "exists", "check", "preview", "html", "report",
    "reportByTeacher", "detailJosn", "history", "pending", "readPending",
    "getComboStore", "getTree", "getComboStoreCacheable", "getComboStoreBySubjectTeacher",
    "getComboStoreByGradeTeacher", "getSubCategory", "getMainMenu",
    "getGroupTwoMenu", "getGroupTree", "getArchive", "getAllPrincipals",
    "getCustomUser", "getParameterValue", "getWeather", "getFolders", "getFiles",
    "getTreeByUser", "getTreeByGradeTeacher", "getTreeByManager", "getTreeBySubjectTeacher",
    "getGrantedMenuTree", "readClassByStudent", "readByClass", "readByClassTeacher",
    "readByGradeTeacher", "readByStudent", "readByUser", "readByParticipate",
    "readByTarget", "readByCategory", "readByParent", "readByView", "readByIds",
    "readByUser", "readBaseByClassTeacher", "readExcellentWork", "readClassByStudent",
    "readDialog", "readEvaluationStudentByClassTeacher",
    "readEvaluationStudentByGradeTeacher", "readNotReply", "readByShortMessage",
    "readHasReturned", "readAttachment", "readSimple", "readSimpleUser",
    "readStudentAndTeacherByParent", "readTeacherByParent", "readMobilePhoneUser",
    "readAllClass", "readMine", "classCurriculum", "myOpen", "toPdf",
    "export", "exportByUser", "exportByClassTeacher", "exportByGradeTeacher",
    "exportOutbox", "exportHasReturned", "exportTargetRead",
    "download", "compressDownload", "compressDownloadHasReturned",
    "send",            # attachment!send / short-message read 系, 见 SPECIAL_READ
    "inbox", "outbox", "status", "calculateTotal", "currentTime",
    "loadUserTree", "loadTreeByClassTeacher", "loadTree",
    "loadClassParent", "loadClassStudent", "loadDormitoryStudent",
    "loadStudentTree", "loadParentTree", "getMonthCombo", "myOpen",
}

# 会改状态的动词（action 名以这些词开头即判写）
WRITE_PREFIX = (
    "create", "update", "save", "delete", "destroy", "remove", "add", "insert",
    "modify", "edit", "submit", "approve", "approved", "notApproved", "completed",
    "complete", "imp", "import", "upload", "reset", "change", "resend", "input",
    "copy", "move", "transfer", "bind", "unbind", "enable", "disable", "publish",
    "release", "withdraw", "revoke", "revert", "cancel", "confirm", "accept",
    "refuse", "reject", "return", "releaseRecord", "toDraft", "sort", "set",
    "batch", "mark", "toAttachment", "generatePdfAndHtml", "delRecord",
    "start", "finish", "sign", "apply", "assign", "reply", "readDialogSubmit",
    "updateSound", "updateTheme", "sendSms", "changeSms", "forgot",
)

# 明确写但不在前缀表里的补充
WRITE_EXACT = {
    "setRead", "markAsUnread", "batchUpdateRead", "batchUpdateSign", "updateSound",
    "updateTheme", "notifyOfficeComplete", "principalApprovalComplete",
    "schoolLeaderApprovalComplete", "secretaryApprovalComplete",
    "deptLeaderApprovalComplete", "generalAffairsApprovalComplete",
    "legalApprovalComplete", "notifyOfficeComplete", "copy", "deleteDraft",
    "toAttachment", "move",
}

# 特例：namespace 决定语义的
# ⚠️ `send` 同名两义，必须按 namespace 分流：
#   attachment!send  = 把附件推给浏览器（读）
#   short-message-detail!send = 真的发出短信（写）
SPECIAL_READ = {
    ("system/attachment", "send"): True,
    ("system/attachment", "upload"): False,
}
SPECIAL_WRITE = {
    ("message/short-message-detail", "send"): True,
}


def split_ep(ep):
    m = EP_RE.match(ep.strip())
    if not m:
        return None, None
    return m.group("ns"), m.group("act")


def is_write(ep):
    ns, act = split_ep(ep)
    if act is None:
        return False
    key = (ns or "", act)
    if key in SPECIAL_WRITE:
        return True
    if key in SPECIAL_READ:
        return not SPECIAL_READ[key]
    if act in WRITE_EXACT:
        return True
    for p in WRITE_PREFIX:
        if act == p or act.startswith(p):
            return True
    if act in READ_EXACT:
        return False
    # 兜底：未知动作默认只读（保守，不去碰）
    return False


def kind(ep):
    return "write" if is_write(ep) else "read"