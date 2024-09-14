---
hide:
  - navigation
  - toc
icon: material/home
---

# :material-home: 欢迎

用于存储各类感兴趣的、  以及日常开发的技术文档。

旨在妥善管理平日所积累的各类技术相关笔记、参考文档等需要反复查阅的内容。

??? note "MKDocs速查"
    - `mkdocs new [dir-name]` - 创建一个新项目
    - `mkdocs serve` - 本地调试web界面
    - `mkdocs build` - 构建项目
    - `mkdocs -h` - 帮助


<div id="grid-cards-container" class="grid cards" markdown>
    <!-- JavaScript will insert cards here -->
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById('grid-cards-container');

    // 假设你有一个API可以返回目录结构
    fetch('/api/get-directory-structure')
        .then(response => response.json())
        .then(data => {
            data.forEach(category => {
                const card = `
- :octicons-dot-16:{ .lg .middle } [__${category.name}__](${category.link})
    ---

    偏向实际开发的分类

    > “${category.name}”：描述...
`;
                container.innerHTML += card;
            });
        })
        .catch(error => console.error('Error fetching directory structure:', error));
});
</script>

<!-- 

<div class="grid cards" markdown>

-   :simple-formspree:{ .lg .middle } [__平台__](平台/index.md)

    ---


    偏向实际开发的分类

    > “平台”：ARM/MCU/x86平台…

-   :simple-opensourcehardware:{ .lg .middle } [__硬件__](硬件/index.md)

    ---

    偏向理论知识、硬件模块参考的分类
    
    > “硬件”：基础理论/电路模块/机械/材料…

-   :simple-gnubash:{ .lg .middle } [__软件__](软件/index.md)

    ---

    偏向软件知识的分类

    > “软件”：数据结构/嵌软/Linux/WEB/AI/语言…
<!-- 
-   :simple-gnubash:{ .lg .middle } [__个人主页__](https://sagi-rastar.github.io/about/)

    ---

    个人主页主要用来存放碎碎念

    > “个人主页”：Blog/图集/关于… -->

