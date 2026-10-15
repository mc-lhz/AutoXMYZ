"""学生端基础数据：本人档案、字典、学期、校区。

对应端点前缀：`account/`、`system/`、`edu/`、`transcript/`
"""


class ProfileMixin(object):

    def status(self):
        """本人账号与学籍摘要。GET /account/user!status.action"""
        return self.get("/account/user!status.action")

    def profile(self):
        """status 的语义别名，调用方读起来更顺。"""
        return self.status()

    def menuTree(self):
        """当前账号有权访问的菜单树（130 节点量级）。
        POST /account/user!getGrantedMenuTree.action
        返回节点含 action.jsFile / className / config，是端点清单的权威来源。
        """
        return self.post("/account/user!getGrantedMenuTree.action", {})

    def readSimpleUser(self, userId=None):
        """按 id 读用户简要信息。GET /account/user!readSimpleUser.action"""
        p = {"id": userId or self.userId}
        return self.get("/account/user!readSimpleUser.action", p)

    def readTeacherByParent(self, studentId=None):
        """读家长可见的教师信息。GET /account/user!readTeacherByParent.action"""
        return self.get("/account/user!readTeacherByParent.action",
                        {"studentId": studentId or self.userId})

    def readStudentAndTeacherByParent(self, studentId=None):
        """读家长绑定的学生与教师。GET /account/user!readStudentAndTeacherByParent.action"""
        return self.get("/account/user!readStudentAndTeacherByParent.action",
                        {"studentId": studentId or self.userId})

    def readBaseByClassTeacher(self, studentId=None, classId=None):
        """班主任读学生基础信息。GET /edu/student!readBaseByClassTeacher.action"""
        p = {"studentId": studentId, "classId": classId}
        return self.get("/edu/student!readBaseByClassTeacher.action", p)


class DictMixin(object):

    def comboStore(self, dictCode, **kw):
        """按字典码读下拉项。GET /system/dict!getComboStore.action?dictCode=..."""
        p = {"dictCode": dictCode}
        p.update(kw)
        return self.get("/system/dict!getComboStore.action", p)

    def comboStoreCacheable(self, dictCode, **kw):
        """缓存版字典。GET /system/dict!getComboStoreCacheable.action"""
        p = {"dictCode": dictCode}
        p.update(kw)
        return self.get("/system/dict!getComboStoreCacheable.action", p)

    def dictTree(self, dictCode):
        """树状字典。GET /system/dict!getTree.action?dictCode=..."""
        return self.get("/system/dict!getTree.action", {"dictCode": dictCode})

    def schoolTermCombo(self):
        """学期下拉。GET /edu/school-term!getComboStore.action"""
        return self.get("/edu/school-term!getComboStore.action", {})

    def classCombo(self):
        """班级下拉。GET /edu/class!getComboStore.action"""
        return self.get("/edu/class!getComboStore.action", {})

    def gradeCombo(self):
        """年段下拉。GET /edu/grade!getComboStore.action"""
        return self.get("/edu/grade!getComboStore.action", {})

    def subjectCombo(self):
        """科目下拉。GET /edu/subject!getComboStore.action"""
        return self.get("/edu/subject!getComboStore.action", {})

    def gradeTree(self):
        """年级树。GET /edu/grade!loadTree.action"""
        return self.get("/edu/grade!loadTree.action", {})

    def classTreeByClassTeacher(self):
        """班主任可见班级树。GET /edu/class!loadTreeByClassTeacher.action"""
        return self.get("/edu/class!loadTreeByClassTeacher.action", {})

    def parentCombo(self, **kw):
        """家长下拉。GET /edu/parent!loadClassParent.action"""
        return self.get("/edu/parent!loadClassParent.action", dict(kw))

    def classStudent(self, **kw):
        """班级学生列表（分页）。GET /edu/student!loadClassStudent.action"""
        return self.paged("/edu/student!loadClassStudent.action", dict(kw))

    def dormitoryStudent(self, **kw):
        """宿舍学生列表。GET /edu/student!loadDormitoryStudent.action"""
        return self.get("/edu/student!loadDormitoryStudent.action", dict(kw))

    def teacherSimple(self, **kw):
        """教师简要信息。GET /edu/teacher!readSimple.action"""
        return self.get("/edu/teacher!readSimple.action", dict(kw))

    def weather(self):
        """校园天气。GET /system/weather!getWeather.action"""
        return self.get("/system/weather!getWeather.action", {})

    def networkFolders(self, path=""):
        """网络磁盘目录。GET /system/network-disk!getFolders.action"""
        return self.get("/system/network-disk!getFolders.action", {"path": path})

    def networkFiles(self, path="", **kw):
        """网络磁盘文件。GET /system/network-disk!getFiles.action"""
        p = {"path": path}
        p.update(kw)
        return self.get("/system/network-disk!getFiles.action", p)