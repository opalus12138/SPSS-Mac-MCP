# SPSS-Mac-MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)]()
[![MCP](https://img.shields.io/badge/protocol-MCP-green.svg)](https://modelcontextprotocol.io)
[![SPSS 20-31](https://img.shields.io/badge/SPSS-20--31-orange.svg)]()

> Let AI assistants drive IBM SPSS Statistics on macOS through the **Model Context Protocol**.
> Describe your analysis in plain language — SPSS-Mac-MCP translates it into SPSS syntax, runs it on the real SPSS engine, and returns clean Markdown/SPV/HTML output.

让 AI 助手在 **macOS** 上直接驱动 IBM SPSS Statistics 跑统计分析。
用自然语言描述需求 —— SPSS-Mac-MCP 自动生成 SPSS 语法、调用真实 SPSS 引擎、返回 Markdown / SPV / HTML 三种格式的结果。

---

## ✨ Why SPSS-Mac-MCP

| | Windows 版 SPSS-MCP | **SPSS-Mac-MCP（本项目）** |
|---|---|---|
| 平台支持 | 仅 Windows | **macOS** + Windows + Linux |
| 安装 | `install.bat` | `pip install -e .` |
| SPSS 检测 | Windows 注册表 | macOS `/Applications` 自动探测 |
| 动态库处理 | `PATH` | **`DYLD_FALLBACK_LIBRARY_PATH`**（绕过 macOS SIP）|
| 输出格式 | OXML | **OXML + SPV + HTML**（三联输出）|
| 端到端验证 | 部分 | **23 项主流分析 100% 通过** |

---

## 🎯 Features

- **Native macOS support**：自动识别 `/Applications/IBM SPSS Statistics XX/`，无需手工配置
- **Persistent SPSS engine**：一次启动复用，避免每次冷启动 30-60 秒
- **Triple-format output**：同步生成机器解析的 OXML、SPSS 原生的 SPV、浏览器友好的 HTML
- **22+ SPSS methods**：覆盖描述、相关、t/ANOVA/重测、线性/Logistic/多分类回归、信度/EFA、非参数、聚类、判别、生存分析
- **Cross-platform compatible**：同一份代码兼容 macOS、Windows、Linux

---

## 📦 Requirements

- macOS 11+（也兼容 Windows 10/11 与 Linux）
- Python **3.10+**
- IBM SPSS Statistics **20–31**（带 Python Essentials / Python Integration Plug-in）
- MCP 客户端：Claude Code、Claude Desktop、Cline 等

---

## 🚀 Quick Install

```bash
# 1. 用 uv 装隔离环境（推荐）
git clone https://github.com/opalus12138/SPSS-Mac-MCP.git
cd SPSS-Mac-MCP
uv venv .venv --python python3.12
uv pip install -e .

# 2. 一键写入 Claude Code 配置（自动备份原配置）
.venv/bin/spss-mac-mcp configure-claude

# 3. 重启 Claude Code
```

完成。Claude Code 里 `/mcp` 命令会列出 `spss-mac-mcp`。

### 验证安装

```bash
.venv/bin/spss-mac-mcp status
```

应输出：

```
=== SPSS MCP Capability Status ===
pyreadstat : OK v1.3.5
pandas     : OK v3.0.3
SPSS batch : OK — /Applications/IBM SPSS Statistics 27/SPSS Statistics.app/Contents/MacOS/stats
```

---

## 💬 Usage

只需在 Claude Code 里用自然语言描述：

```
请对 data.sav 做描述性统计
```

```
用 SPSS 的 EFA 对 Q1-Q12 做探索性因子分析，VARIMAX 旋转，提取 2 个因子
```

```
对 firm_panel.sav 做层级回归：
  Step 1: 控制变量 (Lev, ROA, Size)
  Step 2: 加入 DTI
  Step 3: 加入 IP
报告 R² 变化和系数表
```

Claude 会自动：
1. 读取你的 `.sav` 文件
2. 生成 SPSS 语法
3. 调用真实 SPSS 引擎执行
4. 把结果整理成 Markdown 三线表（同时把 `.spv` 留给 SPSS GUI、`.html` 给浏览器）

---

## 🧪 Validated Analyses

本项目对 **23 项主流 SPSS 分析方法**做了端到端验证，全部在 macOS 上跑通：

<details>
<summary>展开查看完整列表（23/23 PASS）</summary>

| 类别 | 分析 | SPSS 命令 | 状态 |
|---|---|---|---|
| 描述 / 相关 / 频数 | 描述统计 | `DESCRIPTIVES` | ✅ |
| | 频数分布 | `FREQUENCIES` | ✅ |
| | 交叉表 + 卡方 | `CROSSTABS` | ✅ |
| | Pearson 相关 | `CORRELATIONS` | ✅ |
| | Spearman 等级相关 | `NONPAR CORR` | ✅ |
| 均值比较 | 独立样本 t | `T-TEST GROUPS` | ✅ |
| | 配对 t | `T-TEST PAIRS` | ✅ |
| | 单因素 ANOVA | `ONEWAY` | ✅ |
| | 双因素 ANOVA | `UNIANOVA` | ✅ |
| | 重复测量 ANOVA | `GLM` w/ `WSFACTOR` | ✅ |
| 回归 | 线性回归 | `REGRESSION` | ✅ |
| | 层级回归 | `REGRESSION` 多步 | ✅ |
| | 二元 Logistic | `LOGISTIC REGRESSION` | ✅ |
| | 多分类 Logistic | `NOMREG` | ✅ |
| 量表方法 | Cronbach's α | `RELIABILITY` | ✅ |
| | EFA 因子分析 | `FACTOR` w/ VARIMAX | ✅ |
| 非参数检验 | Mann-Whitney U | `NPAR TESTS /M-W` | ✅ |
| | Kruskal-Wallis | `NPAR TESTS /K-W` | ✅ |
| | Wilcoxon 符号秩 | `NPAR TESTS /WILCOXON` | ✅ |
| 多元方法 | K-均值聚类 | `QUICK CLUSTER` | ✅ |
| | 层次聚类 | `CLUSTER` | ✅ |
| | 判别分析 | `DISCRIMINANT` | ✅ |
| 生存分析 | Kaplan-Meier | `KM` | ✅ |

</details>

完整演示见 [`examples/full_validation/`](examples/full_validation/)。

---

## 🔧 Technical Highlights

### macOS 适配的几个关键决策

1. **`DYLD_FALLBACK_LIBRARY_PATH` 而非 `DYLD_LIBRARY_PATH`**：macOS SIP 在 Catalina+ 之后会剥掉子进程的 `DYLD_LIBRARY_PATH`，但 `DYLD_FALLBACK_LIBRARY_PATH` 不受影响。
2. **绕过 IBM 硬编码的 `/Applications/Python3/lib/`**：SPSS 自带的 `python3.8` 二进制把 `libpython3.8.dylib` 路径硬编码到 `/Applications/Python3/`（一个非默认位置）。通过 `DYLD_FALLBACK_LIBRARY_PATH=$SPSS_HOME/Resources/Python3/lib` 让它能找到真实的库。
3. **OMS 直接输出 SPV**：XD 模式（Python 启动的外部 SPSS 引擎）下 `OUTPUT SAVE` / `OUTPUT EXPORT` 不可用，但 `OMS /DESTINATION FORMAT=SPV` 可以。

详细技术报告见 [`docs/macos-port.md`](docs/macos-port.md)。

---

## 📊 Output Formats

每次分析自动生成三种格式：

| 格式 | 用途 | 推荐场景 |
|---|---|---|
| **OXML** (`.xml`) | 机器解析 | 写脚本提取系数/p 值/R² |
| **SPV** (`.spv`) | SPSS Viewer 原生 | 在 SPSS GUI 打开、改透视表样式、复制到 Word |
| **HTML** (`.html`) | 浏览器 | 直接看、分享给同事、贴到邮件 |

---

## 🧠 PROCESS Macro Integration

集成 Andrew Hayes 的 **PROCESS v4.1**，覆盖 6 大常用模型（已端到端验证，见 [`examples/process_models/`](examples/process_models/)）。

### 用法

```python
# 通过 MCP 工具
spss_run_process(
    file_path="data.sav",
    y="TQ", x="DTI", m=["IP"],           # 注意：m 必须是列表
    model=4, bootstrap=5000, seed=20260525,
)
```

或者用自然语言：

```
"用 PROCESS Model 4 跑 firm_panel.sav 的 DTI → IP → TQ 中介，
 bootstrap 5000 次，标准化系数"
```

### ⚠️ FAQ: 常见错误

#### 错误 1：`MATRIX Error #12302` 或 PROCESS 解析失败

**症状**：直接用 `spss_run_syntax` 自己写 PROCESS 调用语法时报错。

**根因**：用了错误的 SPSS 命令 `INCLUDE FILE='...'.`

**正确做法**：

```spss
INSERT FILE='/path/to/process.sps'.        ← ✅ 用 INSERT
PROCESS y=Y /x=X /m=M /model=4 /boot=5000.

# 而不是：
INCLUDE FILE='/path/to/process.sps'.       ← ❌ 不能用 INCLUDE
```

为什么？`INCLUDE` 是 SPSS 老命令，对长行有 80 字符截断，会破坏 PROCESS 内部的 `MATRIX ... END MATRIX` 块。Andrew Hayes 官方文档明确要求用 `INSERT`。

如果你用本项目的 `spss_run_process` 工具，**已经自动用 INSERT**，不用操心这个。

#### 错误 2：调用 `spss_run_process` 报 "Missing required argument"

**症状**：参数明明传了，但报缺 `file_path / y / x`。

**根因**：早期版本（≤ v0.1.x）的 schema 用了过于宽松的类型（`object`、空 `list/dict`），客户端 XML 序列化器会把整个 dict 渲染成空。

**修复**：v0.2.0+ 已经把 `m` 改成明确的 `List[str]`，`covariates` 为 `List[str]`，`extra_options` 为 `Dict[str, str]`。升级即可。

#### 错误 3：输出超大（900KB+）超过 LLM 上下文

**症状**：PROCESS 跑完后输出几百 KB 的源码 echo，把 LLM 上下文塞爆。

**根因**：PROCESS 用 `MATRIX` 引擎，源码会被完整 echo。`SET PRINTBACK=OFF` 在 XD 模式下无效。

**修复**：v0.2.0+ 内置 `extract_process_results()` 后处理，自动定位最后一次"PROCESS Procedure"banner，把输出从 ~937 KB 压到 ~3 KB（99.7% 压缩）。

---

## 🙏 Acknowledgments

This project is derived from [SPSS-MCP](https://github.com/Exekiel179/SPSS-MCP) by Exekiel179 (MIT licensed).

The original project pioneered the persistent SPSS engine + OMS capture architecture, which made the macOS port feasible. SPSS-Mac-MCP focuses specifically on:

- Native macOS adaptation (path detection, DYLD handling)
- Triple-format output (OXML + SPV + HTML)
- Comprehensive validation of 23 analysis methods
- Cross-platform unification (one codebase, three OSes)

IBM® and SPSS® are trademarks of International Business Machines Corporation. This project is not affiliated with, endorsed by, or sponsored by IBM.

---

## 📜 License

MIT — see [`LICENSE`](LICENSE).

Acknowledgment notice in [`NOTICE`](NOTICE).

---

## 🛠️ Contributing

Issues 与 PR 欢迎。重点方向：

- 接入更多 SPSS 命令（PROCESS、SEM AMOS 桥接）
- Windows 同步验证（保持跨平台兼容）
- 性能优化（多分析并行）

---

**Author**: [opalus12138](https://github.com/opalus12138)
