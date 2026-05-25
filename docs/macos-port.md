# macOS 移植技术说明

本文记录把 SPSS-MCP 从 Windows 原生移植到 macOS 的关键技术决策。

## 背景

上游的 [SPSS-MCP](https://github.com/Exekiel179/SPSS-MCP) 把 IBM SPSS Statistics 的 Python Integration Plug-in 通过 MCP 协议暴露给 LLM。但代码里有大量 Windows 特异性假设：

- 用 `winreg` 读注册表找 SPSS 安装路径
- 硬编码 `stats.exe` 文件名
- 假定 `Python3\Lib\site-packages`（Windows 风格）
- 用 `PATH` 加载动态库

## macOS 上的 SPSS 安装布局

```
/Applications/IBM SPSS Statistics 27/
├── SPSS Statistics.app/
│   └── Contents/
│       ├── MacOS/
│       │   └── stats              ← 主程序（无 .exe 后缀）
│       └── bin/pythonenv.sh       ← 官方启动脚本（依赖 Java）
└── Resources/
    └── Python3/
        ├── bin/python3.8           ← 真实 Python 二进制
        └── lib/python3.8/
            └── site-packages/
                └── spss/           ← IBM 官方 Python 接口模块
```

## 移植的 5 个关键点

### 1. SPSS 探测：`config.py`

新增 `_find_spss_via_macos()`，按版本号倒序扫描 `/Applications/IBM SPSS Statistics XX`，定位 `stats` 可执行文件。

### 2. SPSS Python 定位：`config.py`

macOS 下 `python3` 在 SPSS 安装根目录的 `Resources/Python3/bin/`，且优先使用真实二进制 `python3.8`，不用 shell wrapper（wrapper 在隔离环境下找不到 `python3.8` 命令）。

### 3. 动态库加载：`spss_engine.py`

**核心难点**：SPSS 27 的 `python3.8` 二进制把 `libpython3.8.dylib` 硬编码到 `/Applications/Python3/lib/libpython3.8.dylib`（一个非默认安装路径，IBM 历史遗留）。直接运行会报 `dyld[xxx]: Library not loaded`。

**已尝试方案**：
- ❌ `DYLD_LIBRARY_PATH`：macOS SIP（System Integrity Protection）在 Catalina 之后会剥掉子进程的此环境变量
- ❌ 创建 `/Applications/Python3` 符号链接：需要 sudo，破坏性
- ❌ `install_name_tool` 改二进制：修改 IBM 闭源软件，不优雅
- ✅ **`DYLD_FALLBACK_LIBRARY_PATH`**：SIP 不剥这个，且优先级低于 `@rpath`，安全。指向 `$SPSS_HOME/Resources/Python3/lib`。

完整环境变量配置：

```python
env["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join([
    f"{spss_home}/Resources/Python3/lib",
    f"{spss_home}/lib",
    f"{spss_home}/SPSS Statistics.app/Contents/Frameworks",
    f"{spss_home}/SPSS Statistics.app/Contents/MacOS",
])
env["SPSS_HOME"] = spss_home
env["STATSHOME"] = spss_home
env["PYTHONHOME"] = f"{spss_home}/Resources/Python3"
env["PYTHONPATH"] = f"{spss_home}/Resources/Python3/lib/python3.8/site-packages"
```

### 4. site-packages 路径风格：`spss_engine.py`

引擎子进程脚本生成时，macOS 用：

```python
os.path.join(SPSS_HOME, "Resources", "Python3", "lib",
             "python%d.%d" % sys.version_info[:2], "site-packages")
```

Windows 用原来的 `Python3/Lib/site-packages`。

### 5. SPV 输出：OMS 而非 OUTPUT 命令

XD 模式（Python `spss.StartSPSS()`）下没有 Designated Viewer，所有 `OUTPUT SAVE` / `OUTPUT EXPORT` 都失败（err_level=3）。

**解决方案**：直接用 OMS 三联输出：

```spss
OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='analysis.xml' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV  OUTFILE='analysis.spv' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='analysis.html' VIEWER=NO.

... your analysis syntax ...

OMSEND.
```

OMS 是底层捕获，独立于 Viewer，在 XD 模式下完全可用。

## 验证

23 项主流分析方法，6 个数据集，三种输出格式，全部通过。详见 [examples/full_validation/](../examples/full_validation/)。

## 致谢

上游 [SPSS-MCP](https://github.com/Exekiel179/SPSS-MCP) 的持久引擎 + OMS 捕获架构是这次移植的基础。本项目专注于 macOS 适配与全功能验证。
