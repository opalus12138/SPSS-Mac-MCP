"""
Configuration loading and SPSS installation detection for SPSS MCP.
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load .env from project root first and let repo-local settings override inherited shell values.
load_dotenv(_PROJECT_ROOT / ".env", override=True)
load_dotenv()


def _find_spss_via_registry() -> str | None:
    """Search Windows registry for IBM SPSS Statistics installation path."""
    if sys.platform != "win32":
        return None
    try:
        import winreg
        base_key = r"SOFTWARE\IBM\SPSS Statistics"
        for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                with winreg.OpenKey(hive, base_key) as key:
                    i = 0
                    while True:
                        try:
                            version = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, version) as ver_key:
                                try:
                                    install_dir, _ = winreg.QueryValueEx(
                                        ver_key, "InstallationDirectory"
                                    )
                                    candidate = Path(install_dir) / "stats.exe"
                                    if candidate.exists():
                                        return str(candidate)
                                except FileNotFoundError:
                                    pass
                            i += 1
                        except OSError:
                            break
            except FileNotFoundError:
                continue
    except ImportError:
        pass
    return None


def _find_spss_via_filesystem() -> str | None:
    """Check common SPSS installation paths on Windows."""
    common_roots = [
        r"C:\Program Files\IBM\SPSS Statistics",
        r"C:\Program Files (x86)\IBM\SPSS Statistics",
        r"C:\spss",
        r"D:\spss",
        r"E:\spss",
    ]
    versions = list(range(20, 32))  # SPSS 20 through 31
    for root in common_roots:
        # Check versioned subdirectories (newest first)
        for v in reversed(versions):
            candidate = Path(root) / str(v) / "stats.exe"
            if candidate.exists():
                return str(candidate)
        # Check root directly
        candidate = Path(root) / "stats.exe"
        if candidate.exists():
            return str(candidate)
    return None


def _find_spss_via_macos() -> str | None:
    """检测 macOS 上的 SPSS Statistics 安装。"""
    if sys.platform != "darwin":
        return None
    versions = list(range(20, 32))  # SPSS 20–31
    candidates: list[Path] = []
    for v in reversed(versions):
        candidates.extend([
            Path(f"/Applications/IBM SPSS Statistics {v}/SPSS Statistics.app/Contents/MacOS/stats"),
            Path(f"/Applications/IBM SPSS Statistics {v}/SPSSStatistics.app/Contents/MacOS/stats"),
        ])
    # 无版本号的通用路径
    candidates.extend([
        Path("/Applications/IBM SPSS Statistics/SPSSStatistics.app/Contents/MacOS/stats"),
        Path("/Applications/IBM SPSS Statistics.app/Contents/MacOS/stats"),
    ])
    for c in candidates:
        if c.exists():
            return str(c)
    return None


def get_spss_home(stats_exe: str) -> Path:
    """从 stats 可执行文件路径推断 SPSS_HOME。

    Windows: stats.exe 直接在 SPSS_HOME 下
    macOS:   stats 在 SPSS_HOME/SPSS Statistics.app/Contents/MacOS/ 下
    """
    stats_path = Path(stats_exe)
    if sys.platform == "darwin":
        # MacOS → Contents → SPSS Statistics.app → SPSS_HOME
        return stats_path.parent.parent.parent.parent
    return stats_path.parent


def get_spss_executable() -> str | None:
    """
    Return path to stats.exe, or None if SPSS is not installed / disabled.

    Detection order:
    1. SPSS_NO_SPSS env var (forces file-only mode)
    2. SPSS_INSTALL_PATH env var (explicit path to install dir)
    3. Windows registry
    4. Common filesystem paths
    5. PATH scan
    """
    if os.environ.get("SPSS_NO_SPSS", "0").strip() in ("1", "true", "yes"):
        return None

    # Explicit install path from env
    install_path = os.environ.get("SPSS_INSTALL_PATH", "").strip()
    if install_path:
        # macOS：环境变量可指向 SPSS_HOME 或 .app 内的 stats
        if sys.platform == "darwin":
            mac_stats = Path(install_path) / "SPSS Statistics.app" / "Contents" / "MacOS" / "stats"
            if mac_stats.exists():
                return str(mac_stats)
            mac_stats2 = Path(install_path) / "SPSSStatistics.app" / "Contents" / "MacOS" / "stats"
            if mac_stats2.exists():
                return str(mac_stats2)
            if Path(install_path).name == "stats" and Path(install_path).exists():
                return install_path
        # Windows
        candidate = Path(install_path) / "stats.exe"
        if candidate.exists():
            return str(candidate)
        if Path(install_path).name.lower() == "stats.exe" and Path(install_path).exists():
            return install_path

    # macOS filesystem
    found = _find_spss_via_macos()
    if found:
        return found

    # Windows registry
    found = _find_spss_via_registry()
    if found:
        return found

    # Windows filesystem
    found = _find_spss_via_filesystem()
    if found:
        return found

    # PATH
    found = shutil.which("stats")
    if found:
        return found

    return None


def get_spss_python() -> str | None:
    """Return path to the SPSS Python3 executable bundled with SPSS."""
    stats_exe = get_spss_executable()
    if not stats_exe:
        return None
    if sys.platform == "darwin":
        # /Applications/IBM SPSS Statistics 27/Resources/Python3/bin/python3.8
        spss_home = get_spss_home(stats_exe)
        # 优先用 python3.8 这个真实二进制（而不是 python3 这个会丢 PATH 的 shell wrapper）
        for name in ("python3.8", "python3.9", "python3.10", "python3.7", "python3"):
            py = spss_home / "Resources" / "Python3" / "bin" / name
            if py.exists():
                return str(py)
        return None
    # Windows
    python_exe = Path(stats_exe).parent / "Python3" / "python.exe"
    if python_exe.exists():
        return str(python_exe)
    return None


def _get_positive_int_env(name: str, default: int) -> int:
    """Return a positive integer env var value or a default."""
    try:
        value = int(os.environ.get(name, str(default)))
    except ValueError:
        return default
    return value if value > 0 else default


def get_timeout() -> int:
    """Return SPSS analysis timeout in seconds (default 120)."""
    return _get_positive_int_env("SPSS_TIMEOUT", 120)


def get_startup_timeout() -> int:
    """
    Return SPSS engine startup timeout in seconds.

    Startup is often slower than a normal analysis request because SPSS may need
    to initialize licensing, Python integration, and the persistent XD engine.
    Default to 300 seconds unless explicitly overridden.
    """
    return _get_positive_int_env("SPSS_STARTUP_TIMEOUT", 300)


def get_runtime_config() -> dict:
    """Return the effective runtime configuration used for SPSS execution."""
    return {
        "timeout": get_timeout(),
        "startup_timeout": get_startup_timeout(),
        "temp_dir": str(get_temp_dir()),
        "results_dir": str(get_results_dir()),
        "spss_path": get_spss_executable(),
    }


def get_temp_dir() -> Path:
    """Return the directory for temporary SPSS files, creating it if needed."""
    default = Path(tempfile.gettempdir()) / "spss-mcp"
    temp_dir = Path(os.environ.get("SPSS_TEMP_DIR", str(default)))
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def get_results_dir() -> Path:
    """Return directory where persistent SPSS viewer output files (.spv) are saved."""
    default = get_temp_dir() / "results"
    out_dir = Path(os.environ.get("SPSS_RESULTS_DIR", str(default)))
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def get_process_macro_path() -> str | None:
    """检测 Andrew Hayes PROCESS macro 的 process.sps 文件路径。

    优先顺序：
      1. PROCESS_MACRO_PATH 环境变量（显式指定）
      2. 常见安装位置（用户 Downloads、Documents）
      3. SPSS Extensions 目录（极少有人放这里，但顺便扫一下）
    """
    # 1) 显式环境变量
    explicit = os.environ.get("PROCESS_MACRO_PATH", "").strip()
    if explicit:
        p = Path(explicit)
        if p.is_file() and p.suffix.lower() == ".sps":
            return str(p)
        if p.is_dir():
            candidate = p / "process.sps"
            if candidate.exists():
                return str(candidate)

    # 2) 常见用户目录扫描（向下找两层，避免太深）
    search_roots = [
        Path.home() / "Downloads",
        Path.home() / "Documents",
        Path.home() / "Desktop",
        Path("/Applications"),
    ]
    for root in search_roots:
        if not root.exists():
            continue
        for candidate in root.glob("**/PROCESS*/process.sps"):
            return str(candidate)
        for candidate in root.glob("**/process.sps"):
            # 必须确实在 PROCESS 包内
            if "PROCESS" in str(candidate).upper() or "Hayes" in str(candidate):
                return str(candidate)

    return None


def detect_capabilities() -> dict:
    """
    Detect what capabilities are available on this machine.

    Returns a dict with:
        pyreadstat: bool
        spss: bool
        spss_path: str | None
        pyreadstat_version: str | None
        pandas_version: str | None
        process_macro_path: str | None
    """
    caps: dict = {
        "pyreadstat": False,
        "pyreadstat_version": None,
        "pandas_version": None,
        "spss": False,
        "spss_path": None,
        "process_macro_path": get_process_macro_path(),
    }

    try:
        import pyreadstat
        caps["pyreadstat"] = True
        caps["pyreadstat_version"] = getattr(pyreadstat, "__version__", "unknown")
    except ImportError:
        pass

    try:
        import pandas as pd
        caps["pandas_version"] = pd.__version__
    except ImportError:
        pass

    spss_exe = get_spss_executable()
    if spss_exe:
        caps["spss"] = True
        caps["spss_path"] = spss_exe
        # Check for SPSS Python3 (XD API) — preferred execution method
        from pathlib import Path
        spss_py = Path(spss_exe).parent / "Python3" / "python.exe"
        caps["spss_python"] = str(spss_py) if spss_py.exists() else None
    else:
        caps["spss_python"] = None

    return caps
