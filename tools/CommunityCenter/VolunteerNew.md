# VolunteerNew — 志愿者(新)：活动报名/签到/调查/AIMUNC/美辩

骨架由构建脚本生成后人工校对；参数 **kw 透传（GET query / POST form）。

| 方法 | 端点 | HTTP |
|---|---|---|
| `readVolunteerActivityBySign` | `volunteer/activity!readBySign.action` | GET |
| `createActivityRegistration` | `volunteer/activity-registration!create.action` | POST |
| `destroyActivityRegistration` | `volunteer/activity-registration!destroy.action` | POST |
| `exportActivityRegistration` | `volunteer/activity-registration!exportByStudent.action` | GET |
| `importActivityRegistration` | `volunteer/activity-registration!imp.action` | POST |
| `readActivityRegistration` | `volunteer/activity-registration!readByStudent.action` | GET |
| `registrationActivityRegistration` | `volunteer/activity-registration!registration.action` | POST |
| `unregistrationActivityRegistration` | `volunteer/activity-registration!unregistration.action` | POST |
| `updateActivityRegistration` | `volunteer/activity-registration!update.action` | POST |
| `readVolunteerActivity2ByRegistration` | `volunteer/activity2!readByRegistration.action` | GET |
| `loadAimuncDetail` | `volunteer/aimunc-detail!load.action` | GET |
| `saveAimuncDetail` | `volunteer/aimunc-detail!save.action` | POST |
| `loadNhsdlcDetail` | `volunteer/nhsdlc-detail!load.action` | GET |
| `saveNhsdlcDetail` | `volunteer/nhsdlc-detail!save.action` | POST |
| `loadSurveyDetail` | `volunteer/survey-detail!load.action` | GET |
| `saveSurveyDetail` | `volunteer/survey-detail!save.action` | POST |
| `signVolunteer` | `volunteer/volunteer!sign.action` | POST |
| `loadVolunteerRegistrationDetail` | `volunteer/volunteer-registration-detail!load.action` | GET |
| `saveVolunteerRegistrationDetail` | `volunteer/volunteer-registration-detail!save.action` | POST |
