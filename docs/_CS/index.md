---
changelog: true
render_macros: true
---

测试单独推送修改.md文件能否触发CI/CD流程，以完成自动化编译网站静态资源以及部署。

{{m generate_changelog_yaml_for_subfolder('_CS') m}}

{{ _CS }}
