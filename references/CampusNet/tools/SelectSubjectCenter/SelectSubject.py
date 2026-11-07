"""选科（3+1+2）mixin：状态、提交、确认、PDF 确认表、签名。

学生流（m2 前端实测）：
  getComboStoreByStudentOrParent（状态 + 我的 selectSubjectResult）
  → getComboStore(params.selectSubjectPart1/2)（科目下拉：物理类/历史类 + 再选科目）
  → save（subject1Id 物理/历史类、subject2Id 选科1、subject3Id 选科2、
        studentSignatureData / parentSignatureData 为**签名 dataURL**）
  → confirm（{confirm: true, ...}）
  → report.action?id=<结果id>（PDF 确认表，pdfjs 查看）

签名照片读取：结果明细里 studentSignatureId / parentSignatureId 是附件 id，
图片走 `system/attachment!send.action?id=<签名id>`（前端同款，`signatureImageUrl()` 已封）。

⚠️ select-subject-result!read 是**全量列表**（含他人记录，实测 2 万+ 条）——
本人数据一律走 `mySelectSubject()` / `getSelectSubjectDetail(loadId)`。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SelectSubjectMixin(object):
    """选科 mixin（由 XMYZClient 组合）。"""

    def getSelectSubjectState(self, **kw):
        """我的选科状态（含时间窗与 selectSubjectResult）。
        GET /select-subject/select-subject!getComboStoreByStudentOrParent.action"""
        return self.get("/select-subject/select-subject!getComboStoreByStudentOrParent.action", dict(kw))

    def getSubjectCombo(self, part1=None, part2=None, **kw):
        """科目下拉。GET /select-subject/select-subject!getComboStore.action
        part1=True → 物理类/历史类；part2=True → 再选科目（2 门）。"""
        p = {}
        if part1 is not None:
            p["selectSubjectPart1"] = part1
        if part2 is not None:
            p["selectSubjectPart2"] = part2
        p.update(kw)
        return self.get("/select-subject/select-subject!getComboStore.action", p)

    def getCombinationCombo(self, **kw):
        """选科组合下拉。GET /select-subject/select-subject!getCombinationComboStore.action"""
        return self.get("/select-subject/select-subject!getCombinationComboStore.action", dict(kw))

    def getSelectSubjectDetail(self, id, **kw):
        """我的选科明细（含科目名、签名 id/文件名、提交时间）。
        GET /select-subject/select-subject-result-detail!loadId.action"""
        p = {"id": id}
        p.update(kw)
        return self.get("/select-subject/select-subject-result-detail!loadId.action", p)

    def mySelectSubject(self):
        """便捷汇总：我的选科（状态→明细）。

        返回 dict：{activity, result, subjectNames, studentSignatureId,
        parentSignatureId, confirm, submitTime, raw}；未选科时 result=None。
        """
        st = self.getSelectSubjectState()
        acts = st.get("data") or []
        out = {"activity": None, "result": None, "subjectNames": None,
               "studentSignatureId": None, "parentSignatureId": None,
               "confirm": None, "submitTime": None, "activities": acts}
        if not acts:
            return out
        a = acts[0]
        out["activity"] = a.get("name")
        res = a.get("selectSubjectResult") or {}
        if not res.get("id"):
            return out
        out["result"] = res.get("id")
        det = self.getSelectSubjectDetail(res["id"]).get("data") or {}
        out["subjectNames"] = det.get("subjectNames") or det.get("combination")
        out["studentSignatureId"] = det.get("studentSignatureId")
        out["parentSignatureId"] = det.get("parentSignatureId")
        out["confirm"] = det.get("confirm")
        out["submitTime"] = det.get("submitTime")
        return out

    @staticmethod
    def signatureImageUrl(signatureId):
        """签名图片直链（前端同款路由）。"""
        return "https://xmyz.xmedu.cn/system/attachment!send.action?id=%s" % signatureId

    def selectSubjectReportUrl(self, resultId, host="https://xmyz.xmedu.cn"):
        """选科确认表 PDF 的 URL（生成式端点，建议配合浏览器/pdfjs 打开）。
        GET /select-subject/select-subject-result-detail!report.action?id=<结果id>"""
        return "%s/select-subject/select-subject-result-detail!report.action?id=%s" % (host, resultId)

    def getNotSelectedList(self, **kw):
        """未选科学生列表（管理向）。GET /select-subject/not-select-subject!read.action"""
        return self.get("/select-subject/not-select-subject!read.action", dict(kw))

    def getNotSelectedListByClassTeacher(self, **kw):
        """未选科（班主任向）。GET /select-subject/not-select-subject!readByClassTeacher.action"""
        return self.get("/select-subject/not-select-subject!readByClassTeacher.action", dict(kw))

    def getSelectSubjectResults(self, **kw):
        """选科结果全量列表——⚠️ 含他人记录（2 万+ 条），本人数据勿用此接口。"""
        return self.get("/select-subject/select-subject-result!read.action", dict(kw))

    def getSelectSubjectResultsByClassTeacher(self, **kw):
        """选科结果（班主任向）。GET /select-subject/select-subject-result!readByClassTeacher.action"""
        return self.get("/select-subject/select-subject-result!readByClassTeacher.action", dict(kw))

    def saveSelectSubject(self, subject1Id=None, subject2Id=None, subject3Id=None,
                          studentSignatureData=None, parentSignatureData=None, **kw):
        """提交/修改选科（写）。
        POST /select-subject/select-subject-result-detail!save.action
        subject1Id = 物理类/历史类；subject2Id/3Id = 再选科目；两个签名参数为
        **dataURL**（canvas.toDataURL() 输出）。"""
        p = {}
        for k, v in (("subject1Id", subject1Id), ("subject2Id", subject2Id),
                     ("subject3Id", subject3Id),
                     ("studentSignatureData", studentSignatureData),
                     ("parentSignatureData", parentSignatureData)):
            if v is not None:
                p[k] = v
        p.update(kw)
        return self.post("/select-subject/select-subject-result-detail!save.action", p)

    def confirmSelectSubject(self, resultId=None, **kw):
        """确认选科（写，确认后一般不可修改）。
        POST /select-subject/select-subject-result-detail!confirm.action"""
        p = {"confirm": True}
        if resultId is not None:
            p["id"] = resultId
        p.update(kw)
        return self.post("/select-subject/select-subject-result-detail!confirm.action", p)

    def saveSelectSubjectById(self, id, **kw):
        """按 id 修改已提交的选科（写）。
        POST /select-subject/select-subject-result-detail!saveById.action"""
        p = {"id": id}
        p.update(kw)
        return self.post("/select-subject/select-subject-result-detail!saveById.action", p)