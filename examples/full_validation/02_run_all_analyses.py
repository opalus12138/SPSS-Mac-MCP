"""逐一执行 23 项 SPSS 分析，统计成功/失败。

运行方式：
    ~/Tools/spss-mcp-mac/.venv/bin/python 02_run_all_analyses.py

SPSS-MCP 已通过 pip 安装到该 venv，直接 import 即可。
"""
import asyncio
from pathlib import Path
from typing import List, Tuple

from spss_mcp.spss_engine import SpssEngine  # type: ignore

DAY = Path(__file__).parent
DATASETS = DAY / "datasets"
OUTPUT = DAY / "output"           # OXML 机器解析
SYNTAX = DAY / "syntax"           # 留档的 .sps 文件
SPV_DIR = DAY / "spv"             # SPSS Viewer 原生格式（可在 SPSS GUI 打开）
HTML_DIR = DAY / "html"           # HTML，浏览器直接看
for d in (OUTPUT, SYNTAX, SPV_DIR, HTML_DIR):
    d.mkdir(exist_ok=True)


def D(name: str) -> str:
    """数据集路径。"""
    return str(DATASETS / f"{name}.sav")


ANALYSES: List[Tuple[str, str, str]] = [
    # ════ 描述 / 相关 / 频数 ════════════════════════════════════
    ("A1_descriptives", "描述统计 DESCRIPTIVES", f"""
GET FILE='{D("firm_panel")}'.
DESCRIPTIVES VARIABLES=TQ DTI IP Lev ROA Size
  /STATISTICS=MEAN STDDEV MIN MAX KURTOSIS SKEWNESS.
"""),

    ("A2_frequencies", "频数分布 FREQUENCIES", f"""
GET FILE='{D("survey_likert")}'.
FREQUENCIES VARIABLES=Q1 Q2 Q3 gender age_group
  /STATISTICS=MEAN MEDIAN MODE STDDEV
  /ORDER=ANALYSIS.
"""),

    ("A3_crosstabs_chi2", "交叉表+卡方 CROSSTABS", f"""
GET FILE='{D("categorical")}'.
CROSSTABS /TABLES=industry BY digital_level
  /STATISTICS=CHISQ PHI LAMBDA
  /CELLS=COUNT ROW COLUMN
  /COUNT ROUND CELL.
"""),

    ("B1_pearson", "Pearson 相关 CORRELATIONS", f"""
GET FILE='{D("firm_panel")}'.
CORRELATIONS /VARIABLES=TQ DTI IP Lev ROA Size
  /PRINT=TWOTAIL NOSIG /MISSING=PAIRWISE.
"""),

    ("B2_spearman", "Spearman 等级相关 NONPAR CORR", f"""
GET FILE='{D("nonparametric")}'.
NONPAR CORR /VARIABLES=income satisfaction rank_var
  /PRINT=SPEARMAN TWOTAIL NOSIG.
"""),

    # ════ 均值比较 ═════════════════════════════════════════════
    ("C1_indep_ttest", "独立样本 t 检验 T-TEST", f"""
GET FILE='{D("survey_likert")}'.
T-TEST GROUPS=gender(0 1) /VARIABLES=total Q1 Q2.
"""),

    ("C2_paired_ttest", "配对样本 t 检验 T-TEST PAIRS", f"""
GET FILE='{D("experiment")}'.
T-TEST PAIRS=pre_test WITH post_test (PAIRED).
"""),

    ("C3_oneway_anova", "单因素方差 ONEWAY", f"""
GET FILE='{D("survey_likert")}'.
ONEWAY total BY age_group
  /STATISTICS DESCRIPTIVES HOMOGENEITY
  /POSTHOC=BONFERRONI ALPHA(0.05).
"""),

    ("C4_factorial_anova", "双因素方差 UNIANOVA", f"""
GET FILE='{D("experiment")}'.
UNIANOVA t4_week8 BY treatment intensity
  /METHOD=SSTYPE(3) /INTERCEPT=INCLUDE
  /POSTHOC=treatment(BONFERRONI)
  /EMMEANS=TABLES(treatment*intensity)
  /PRINT=DESCRIPTIVE HOMOGENEITY ETASQ.
"""),

    ("C5_repeated_measures", "重复测量 GLM", f"""
GET FILE='{D("experiment")}'.
GLM t1_baseline t2_week2 t3_week4 t4_week8 BY treatment
  /WSFACTOR=time 4 Polynomial
  /MEASURE=score
  /METHOD=SSTYPE(3)
  /PRINT=DESCRIPTIVE ETASQ
  /WSDESIGN=time
  /DESIGN=treatment.
"""),

    # ════ 回归 ═══════════════════════════════════════════════════
    ("D1_linear_reg", "线性回归 REGRESSION", f"""
GET FILE='{D("firm_panel")}'.
REGRESSION /STATISTICS COEFF OUTS R ANOVA COLLIN TOL
  /DEPENDENT TQ
  /METHOD=ENTER DTI IP Lev ROA Size Dual.
"""),

    ("D2_hierarchical_reg", "层级回归（多步 ENTER）", f"""
GET FILE='{D("firm_panel")}'.
REGRESSION /STATISTICS COEFF OUTS R ANOVA CHANGE
  /DEPENDENT TQ
  /METHOD=ENTER Lev ROA Size
  /METHOD=ENTER DTI
  /METHOD=ENTER IP.
"""),

    ("D3_binary_logistic", "二元 Logistic LOGISTIC REGRESSION", f"""
GET FILE='{D("firm_panel")}'.
LOGISTIC REGRESSION VARIABLES HighTQ
  /METHOD=ENTER DTI IP Lev ROA Size
  /PRINT=GOODFIT CI(95)
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5).
"""),

    ("D4_multinomial", "多分类 Logistic NOMREG", f"""
GET FILE='{D("categorical")}'.
NOMREG digital_level (BASE=FIRST ORDER=ASCENDING) BY industry WITH profit firm_age
  /CRITERIA CIN(95) DELTA(0) MXITER(100) MXSTEP(5) CHKSEP(20) LCONVERGE(0) PCONVERGE(0.000001) SINGULAR(0.00000001)
  /MODEL
  /STEPWISE=PIN(.05) POUT(0.1) MINEFFECT(0) RULE(SINGLE) ENTRYMETHOD(LR) REMOVALMETHOD(LR)
  /INTERCEPT=INCLUDE
  /PRINT=PARAMETER SUMMARY LRT CPS STEP MFI.
"""),

    # ════ 量表与维度 ════════════════════════════════════════════
    ("E1_reliability", "信度分析 RELIABILITY", f"""
GET FILE='{D("survey_likert")}'.
RELIABILITY /VARIABLES=Q1 Q2 Q3 Q4 Q5 Q6
  /SCALE('数字化感知量表') ALL /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE
  /SUMMARY=TOTAL.
"""),

    ("E2_factor_analysis", "探索性因子分析 FACTOR", f"""
GET FILE='{D("survey_likert")}'.
FACTOR /VARIABLES Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 Q9 Q10 Q11 Q12
  /MISSING LISTWISE
  /ANALYSIS Q1 Q2 Q3 Q4 Q5 Q6 Q7 Q8 Q9 Q10 Q11 Q12
  /PRINT INITIAL KMO EXTRACTION ROTATION
  /CRITERIA MINEIGEN(1) ITERATE(25)
  /EXTRACTION PC
  /CRITERIA ITERATE(25)
  /ROTATION VARIMAX
  /METHOD=CORRELATION.
"""),

    # ════ 非参数检验 ════════════════════════════════════════════
    ("F1_mann_whitney", "Mann-Whitney U 检验", f"""
GET FILE='{D("nonparametric")}'.
SELECT IF region < 3.
NPAR TESTS /M-W= income BY region(1 2)
  /MISSING ANALYSIS.
EXECUTE.
"""),

    ("F2_kruskal_wallis", "Kruskal-Wallis 检验", f"""
GET FILE='{D("nonparametric")}'.
NPAR TESTS /K-W=income BY region(1 3)
  /MISSING ANALYSIS.
"""),

    ("F3_wilcoxon", "Wilcoxon 符号秩检验", f"""
GET FILE='{D("experiment")}'.
NPAR TESTS /WILCOXON=pre_test WITH post_test (PAIRED).
"""),

    # ════ 多元方法 ═══════════════════════════════════════════════
    ("G1_kmeans", "K-均值聚类 QUICK CLUSTER", f"""
GET FILE='{D("cluster_survival")}'.
QUICK CLUSTER x1_spend x2_freq x3_recency
  /MISSING=LISTWISE
  /CRITERIA=CLUSTER(3) MXITER(20) CONVERGE(0)
  /METHOD=KMEANS(NOUPDATE)
  /PRINT INITIAL ANOVA CLUSTER DISTAN.
"""),

    ("G2_hierarchical_cluster", "层次聚类 CLUSTER", f"""
GET FILE='{D("cluster_survival")}'.
SAMPLE 100 FROM 500.
CLUSTER x1_spend x2_freq x3_recency
  /METHOD WARD
  /MEASURE=SEUCLID
  /PRINT SCHEDULE
  /PRINT CLUSTER(3,3)
  /PLOT NONE.
"""),

    ("G3_discriminant", "判别分析 DISCRIMINANT", f"""
GET FILE='{D("cluster_survival")}'.
DISCRIMINANT /GROUPS=true_segment(0 2)
  /VARIABLES=x1_spend x2_freq x3_recency
  /ANALYSIS ALL
  /PRIORS EQUAL
  /STATISTICS=COEFF RAW BOXM TABLE
  /CLASSIFY=NONMISSING POOLED.
"""),

    # ════ 生存分析 ═══════════════════════════════════════════════
    ("H1_kaplan_meier", "Kaplan-Meier 生存分析 KM", f"""
GET FILE='{D("cluster_survival")}'.
KM time BY true_segment
  /STATUS=event(1)
  /PRINT TABLE MEAN
  /COMPARE OVERALL POOLED.
"""),
]


def wrap_oms(name: str, body: str) -> Tuple[str, Path, Path, Path]:
    """OMS 三重包裹：同时输出 OXML（机器解析）+ SPV（SPSS Viewer）+ HTML（浏览器）。

    XD 模式下不能用 OUTPUT SAVE，OMS 自身支持 SPV/HTML/OXML 等格式可直接写。
    多个 OMS 块并行运行，互不干扰。
    """
    out_xml = OUTPUT / f"{name}.xml"
    out_spv = SPV_DIR / f"{name}.spv"
    out_html = HTML_DIR / f"{name}.html"
    for p in (out_xml, out_spv, out_html):
        if p.exists():
            p.unlink()
    syntax = f"""OMS /SELECT TABLES /DESTINATION FORMAT=OXML OUTFILE='{out_xml}' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=SPV OUTFILE='{out_spv}' VIEWER=NO.
OMS /SELECT TABLES /DESTINATION FORMAT=HTML OUTFILE='{out_html}' VIEWER=NO.
{body.strip()}
OMSEND.
"""
    # 同时把语法写到 syntax/ 留档
    (SYNTAX / f"{name}.sps").write_text(syntax, encoding="utf-8")
    return syntax, out_xml, out_spv, out_html


async def main() -> None:
    engine = SpssEngine()
    print("→ 启动 SPSS 27 引擎...")
    ok, msg = await engine.ensure_started()
    print(f"  {'✓' if ok else '✗'} {msg}\n")
    if not ok:
        return

    results = []
    for idx, (name, desc, body) in enumerate(ANALYSES, 1):
        syntax, out_xml, out_spv, out_html = wrap_oms(name, body)
        print(f"[{idx:2d}/{len(ANALYSES)}] {name:<28} {desc}")
        result = await engine.submit(
            full_syntax=syntax, output_file=str(out_xml), viewer_file=str(out_spv),
        )
        err = result.get("err_level", 99)
        warn = result.get("warn") or ""
        sizes = {
            "xml":  out_xml.stat().st_size if out_xml.exists() else 0,
            "spv":  out_spv.stat().st_size if out_spv.exists() else 0,
            "html": out_html.stat().st_size if out_html.exists() else 0,
        }
        all_ok = err == 0 and all(s > 0 for s in sizes.values())
        status = "✓ PASS" if all_ok else "✗ FAIL"
        print(f"        {status}  err={err}  "
              f"xml={sizes['xml']}B  spv={sizes['spv']}B  html={sizes['html']}B"
              f"{f'  warn={warn[:60]}' if warn else ''}")
        results.append({
            "name": name, "desc": desc,
            "err_level": err,
            "xml_exists": out_xml.exists(), "xml_size": sizes["xml"],
            "spv_exists": out_spv.exists(), "spv_size": sizes["spv"],
            "html_exists": out_html.exists(), "html_size": sizes["html"],
            "warn": warn,
        })

    await engine.stop()

    # 汇总（按三格式分别统计）
    n_xml = sum(1 for r in results if r["xml_exists"])
    n_spv = sum(1 for r in results if r["spv_exists"])
    n_html = sum(1 for r in results if r["html_exists"])
    total = len(results)
    print(f"\n══════════════ 多格式输出汇总 ══════════════")
    print(f"  OXML（机器解析）: {n_xml:2d}/{total}")
    print(f"  SPV （SPSS GUI）: {n_spv:2d}/{total}")
    print(f"  HTML（浏览器）  : {n_html:2d}/{total}")
    print(f"\n══════════════ 逐项 ══════════════")
    for r in results:
        flag = "✓" if r["err_level"] == 0 and r["xml_exists"] else "✗"
        marks = (
            ("X" if r["xml_exists"] else "·")
            + ("V" if r["spv_exists"] else "·")
            + ("H" if r["html_exists"] else "·")
        )
        print(f"  {flag} [{marks}]  {r['name']:<28} {r['desc']}")

    # 保存结果摘要
    import json
    summary_path = DAY / "reports" / "run_summary.json"
    summary_path.parent.mkdir(exist_ok=True)
    summary_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8",
    )
    print(f"\n摘要写入：{summary_path}")


if __name__ == "__main__":
    asyncio.run(main())
