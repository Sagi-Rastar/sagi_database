---
tags:
  - c语言
  - cmakelist
  - vscode
---

# 250102-vscode&cmakelist配置记录

## 介绍

CMake在配置的时候会在输出目录下（`build`）生成一个`compile_commands.json`文件，这个文件中包含了完整的编译命令。`intelliSense`会根据这个文件来提供代码补全、跳转等功能。

