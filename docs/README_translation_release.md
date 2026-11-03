# 翻译增强版下载、升级与打包

当前社区版本：**v2.1.6-translation.1**，基于上游 v2.1.5。此版本由 tssj520 发布，保留 hiroi-sora 及其他原贡献者的版权和许可证。

[前往 GitHub Release 下载](https://github.com/tssj520/Umi-OCR/releases/tag/v2.1.6-translation.1)。

## 首次使用

下载 `Umi-OCR_Translation_Rapid_v2.1.6-translation.1_Windows_x64.zip`，完整解压到可写目录后运行其中的 `Umi-OCR.exe`。内含 Python 运行环境和 RapidOCR 插件，无需安装 Python。此次提供 Windows x64 包；其他平台可参考上游运行环境说明使用源码。

截图 OCR 工具栏的“翻译”默认不勾选，点击开启；旁边的下拉箭头可选择语言和服务。默认英语译为简体中文，支持自动检测。OCR 离线运行；翻译需要联网，免费服务可能出现网络限制、限流或额度不足，详见[翻译使用说明](README_translation.md)。

## 从上游 Windows v2.1.5 升级

1. 备份原软件目录，并从系统托盘完全退出 Umi-OCR。
2. 下载 `Umi-OCR_Translation_v2.1.6-translation.1_Update_from_v2.1.5.zip`。
3. 将更新包内的 `UmiOCR-data` 等文件合并到原软件根目录，与 `Umi-OCR.exe` 同级，允许覆盖同名文件。
4. 重新启动软件，在关于页确认版本号，然后开启截图 OCR 的翻译功能。

更新包只适用于上游 Windows v2.1.5 运行环境。它不包含 OCR 引擎和 Python 库，不单独运行。个人 `.settings`、`.pre_settings`、日志、临时图片和其他缓存均不包含在发布包中，也不由更新包覆盖。原有个性化主题可以继续保留。

## 校验下载

Release 附带 `SHA256SUMS.txt`。可在 PowerShell 中计算文件校验值，与其对照：

```powershell
Get-FileHash .\Umi-OCR_Translation_Rapid_v2.1.6-translation.1_Windows_x64.zip -Algorithm SHA256
```

## 从源码重新打包

使用上游 Windows v2.1.5 运行环境和 RapidOCR 插件，确保本地已有 `Umi-OCR.exe`、`UmiOCR-data/runtime`、`UmiOCR-data/site-packages`、`UmiOCR-data/plugins/win7_x64_RapidOCR-json`。

```powershell
python tools/package_translation.py
```

脚本以 Git 跟踪的源码为输入，从本地运行环境复制依赖，生成完整便携包、仅含代码及文档的增量更新包、校验文件和构建清单。它不会打包用户配置、日志、Python 缓存或截图。输出目录默认为 `release`；如目录已存在，使用 `--output release/new-build` 选择一个新目录。`--base` 可指定生成增量包时的上游基线提交。

源码的 `feature/screenshot-translation` 分支仅包含翻译功能、文档和测试，供上游审阅；`main` 还包含此社区版本的发行元数据和打包工具。
