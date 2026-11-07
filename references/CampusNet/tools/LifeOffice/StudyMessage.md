成绩、综评之外的学习与生活数据。
对应前缀 `edu/` `score/` `transcript/` `message/` `office/` `system/attachment`。

- 学业：`myScores` / `studentScoreTable` / `moduleScores` / `transcript` / `transcriptDetail` /
  `physicalExamination` / `classWork` / `homeworkCompleteTime` / `excellentWorks` /
  `matchAwards` / `attendanceByClass` / `speciality`
- 成长：`growthRecords` / `growthRecordDetail` / `classGrowthRecords`
- 消息：`inbox` / `outbox` / `messageDetail` / `unreadStat` / `recipientStat` /
  `categoryMessages` / `noticeFeedback` / `noticeByTarget` / `officeNotice`
- 附件：`attachmentsByIds` / `myAttachments` / `downloadUrl`

`downloadUrl` 只拼 URL 不下载内容——下载会落本地文件，超出只读查询范畴。
