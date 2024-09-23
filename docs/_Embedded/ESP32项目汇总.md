# ESP32项目汇总

## 1 蓝牙WIFI双模门禁控制器

使用 ESP32-S3作为主控，旨在实现断网情况下也可以利用蓝牙功能进行门禁控制。

> 项目链接： https://gitee.com/chenym_simpler/git_lock_electromagnet

硬件资源如下：

- 使用模组 `ESP32-S3-WROOM-1U-N8R2`
	- `ESP32-S3` 主控，主频高达 240MHz，双核 Xtensa® dual-core 32-bit LX7 CPU
	- 8MB Flash
	- 2MB PSRAM

ESP32-S3-WROOM-1 采用 PCB 板载天线;

ESP32-S3-WROOM-1U 采用 U.FL 座子连接外部 IPEX 天线

可选 4/8/16 MB flash；0/2/8 PSRAM

- [240615-smartconfig配网](240615-smartconfig配网.md)
- [240617-IDF 的事件循环，及 wifi 运行流程](240617-IDF%20的事件循环，及%20wifi%20运行流程.md)
- [240618-SNTP 获取时间、AES 加密](240618-SNTP%20获取时间、AES%20加密.md)
- [240619-蓝牙开发](240619-蓝牙开发.md)
- [240625-卡关系存储设计](240625-卡关系存储设计.md)
- [240626-BM8563 驱动移植，IDF-I2C 笔记](240626-BM8563%20驱动移植，IDF-I2C%20笔记.md)
- [240719-LEDPWM及常用指示函数封装](240719-LEDPWM及常用指示函数封装.md)
- [240818-蓝牙配网以及softAP方式配网探索](240818-蓝牙配网以及softAP方式配网探索.md)
- [240822-ESP32分区表及OTA](240822-ESP32分区表及OTA.md)
- [240905-更新storage以及mqtt模块部分，逐步实现私有json协议](240905-更新storage以及mqtt模块部分，逐步实现私有json协议.md)


## 2 参考文档以及链接：

- [IDF 官方文档](https://docs.espressif.com/projects/esp-idf/zh_CN/v5.2.1/esp32/get-started/index.html)
- [IDF 官方注册表仓库](https://components.espressif.com/)
- [ESP32-S3 技术参考手册](https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_cn.pdf)
> 较为详细，包括概述、功能列表、硬件架构、编程指南、寄存器列表等信息
- [ESP32-S3 技术规格书](https://espressif.com/sites/default/files/documentation/esp32-s3_datasheet_cn.pdf)
> 概述类型，包括各外设重要参数
- [ESP32 选型在线工具]( https://products.espressif.com/#/product-selector?language=zh&names= )
