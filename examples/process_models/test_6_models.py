"""跑 6 个常用 PROCESS 模型，验证每个模型都能生成、执行、抽取干净结果。

测试矩阵（以 firm_panel.sav 为数据）：
  Model 1   调节（DTI × SOE → TQ）
  Model 4   简单中介（DTI → IP → TQ）
  Model 6   链式中介（DTI → IP → Size → TQ）
  Model 7   第一阶段被调节中介（DTI ×SOE → IP → TQ）
  Model 14  第二阶段被调节中介（DTI → IP × SOE → TQ）
  Model 58  双阶段被调节中介（DTI ×SOE → IP ×SOE → TQ）
"""
import asyncio
import sys
from pathlib import Path

# Run with: ~/Tools/spss-mac-mcp/.venv/bin/python test_6_models.py (package installed)

from spss_mac_mcp.config import get_process_macro_path
from spss_mac_mcp.spss_runner import (
    build_process_syntax,
    extract_process_results,
    run_syntax,
)

DATA = "Path(__file__).resolve().parents[1] / "full_validation" / "datasets" / "firm_panel.sav""
OUT = Path(__file__).parent / "process_outputs"
OUT.mkdir(exist_ok=True)

MACRO = get_process_macro_path()
BOOT = 1000   # 加快测试，正式用 5000
SEED = 20260525

TESTS = [
    # name, kwargs, 说明
    ("M01_moderation",
        dict(y="TQ", x="DTI", w="SOE", model=1),
        "Model 1: DTI × SOE → TQ（调节）"),
    ("M04_simple_mediation",
        dict(y="TQ", x="DTI", m="IP", model=4),
        "Model 4: DTI → IP → TQ（简单中介）"),
    ("M06_serial_mediation",
        dict(y="TQ", x="DTI", m=["IP", "Size"], model=6),
        "Model 6: DTI → IP → Size → TQ（链式中介）"),
    ("M07_first_stage_modmed",
        dict(y="TQ", x="DTI", m="IP", w="SOE", model=7),
        "Model 7: DTI ×SOE → IP → TQ（前调节中介）"),
    ("M14_second_stage_modmed",
        dict(y="TQ", x="DTI", m="IP", w="SOE", model=14),
        "Model 14: DTI → IP ×SOE → TQ（后调节中介）"),
    ("M58_both_stages_modmed",
        dict(y="TQ", x="DTI", m="IP", w="SOE", model=58),
        "Model 58: DTI ×SOE → IP ×SOE → TQ（双调节中介）"),
]


async def main():
    print(f"PROCESS macro: {MACRO}")
    print(f"数据: {DATA}")
    print(f"Bootstrap: {BOOT} 次, seed={SEED}")
    print(f"输出目录: {OUT}\n")
    print("=" * 72)

    summary = []
    for name, kwargs, desc in TESTS:
        print(f"\n[{name}] {desc}")
        syntax = build_process_syntax(
            file_path=DATA, process_macro_path=MACRO,
            bootstrap=BOOT, seed=SEED, total=True, **kwargs,
        )
        result = await run_syntax(syntax, data_file=None)

        raw = result.get("output_raw", "")
        clean = extract_process_results(raw)
        success = result.get("success", False)
        err = result.get("last_error_level", "?")

        # 保存干净结果
        out_file = OUT / f"{name}.txt"
        out_file.write_text(clean, encoding="utf-8")

        # 抽几个关键指标确认
        has_outcome = "OUTCOME VARIABLE" in clean
        has_indirect = "Indirect effect" in clean or "Conditional indirect" in clean
        has_index_modmed = "Index of moderated mediation" in clean
        has_total = "Total effect of X on Y" in clean

        markers = []
        if has_outcome: markers.append("OUTCOME ✓")
        if has_total: markers.append("TotalEff ✓")
        if has_indirect: markers.append("Indirect ✓")
        if has_index_modmed: markers.append("ModMedIdx ✓")

        status = "✅ PASS" if (success and len(clean) > 500 and len(clean) < 50000) else "⚠ CHECK"
        print(f"  {status}  raw={len(raw):>7}B  clean={len(clean):>5}B  err={err}")
        print(f"  markers: {' | '.join(markers) or '(none)'}")
        print(f"  → 保存到: {out_file.name}")

        summary.append({
            "name": name, "desc": desc, "success": success,
            "raw_size": len(raw), "clean_size": len(clean),
            "compression": (1 - len(clean)/max(len(raw), 1)) * 100,
            "markers": markers,
        })

    # 汇总
    print("\n" + "=" * 72)
    print("\n══════════ 汇总 ══════════\n")
    print(f"{'模型':<28} {'状态':<6} {'raw':>8} {'clean':>6} {'压缩率':>7}")
    print("-" * 72)
    for s in summary:
        flag = "✅" if s["success"] else "⚠"
        print(f"{s['name']:<28} {flag:<6} {s['raw_size']:>7}B {s['clean_size']:>5}B "
              f"{s['compression']:>6.1f}%")

    passed = sum(1 for s in summary if s["success"])
    print(f"\n通过率: {passed}/{len(summary)}")


asyncio.run(main())
