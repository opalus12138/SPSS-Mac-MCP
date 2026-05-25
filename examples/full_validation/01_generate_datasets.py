"""生成 6 套覆盖性模拟数据，验证 SPSS 各类分析。"""
import numpy as np
import pandas as pd
import pyreadstat
from pathlib import Path

RNG = np.random.default_rng(seed=20260525)
DATASETS = Path(__file__).parent / "datasets"
DATASETS.mkdir(exist_ok=True)


def save_sav(df, name, labels, value_labels=None, measures=None):
    """写 .sav 并打印摘要。"""
    path = DATASETS / f"{name}.sav"
    pyreadstat.write_sav(
        df,
        str(path),
        column_labels=[labels.get(c, c) for c in df.columns],
        variable_value_labels=value_labels or {},
        variable_measure=measures or {},
    )
    print(f"✓ {name}.sav  N={len(df):<5}  vars={list(df.columns)}")


# ════════════════════════════════════════════════════════════════
# 数据集 1：企业面板（DTI → IP → TQ）
# ════════════════════════════════════════════════════════════════
N1 = 3000
N_FIRMS = 500
N_YEARS = 6
firm_id = np.repeat(np.arange(1, N_FIRMS + 1), N_YEARS).astype(float)
year = np.tile(np.arange(2019, 2019 + N_YEARS), N_FIRMS).astype(float)

firm_size = np.repeat(RNG.normal(22.0, 1.0, N_FIRMS), N_YEARS) + RNG.normal(0, 0.2, N1)
firm_lev = np.clip(
    np.repeat(RNG.beta(2, 3, N_FIRMS) * 0.7 + 0.15, N_YEARS) + RNG.normal(0, 0.04, N1),
    0.05, 0.92,
)
SOE = np.repeat(RNG.binomial(1, 0.30, N_FIRMS), N_YEARS).astype(float)
ROA = np.clip(RNG.normal(0.045, 0.06, N1), -0.20, 0.25)
Dual = RNG.binomial(1, 0.30, N1).astype(float)

DTI = np.clip(
    1.6 + 0.30 * SOE + 0.15 * (firm_size - 22.0) - 0.60 * (firm_lev - 0.43)
    + RNG.normal(0, 0.9, N1), 0, None,
)
IP = np.clip(0.9 + 0.12 * DTI + 0.18 * (firm_size - 22.0) + 0.30 * SOE
             + RNG.normal(0, 0.7, N1), 0, None)
TQ = np.clip(3.5 + 0.05 * DTI + 0.08 * IP - 0.30 * firm_lev + 3.0 * ROA
             - 0.10 * (firm_size - 22.0) + RNG.normal(0, 0.7, N1), 0.5, None)
# 二分类衍生变量（用于 Logistic 演示）
HighTQ = (TQ > np.median(TQ)).astype(float)

df1 = pd.DataFrame({
    "firm_id": firm_id, "year": year,
    "TQ": TQ, "DTI": DTI, "IP": IP,
    "Lev": firm_lev, "ROA": ROA, "Size": firm_size,
    "Dual": Dual, "SOE": SOE, "HighTQ": HighTQ,
})
save_sav(
    df1, "firm_panel",
    labels={
        "firm_id": "企业代码", "year": "年份",
        "TQ": "企业价值（托宾Q）", "DTI": "数字化转型强度",
        "IP": "创新绩效（专利对数）", "Lev": "资产负债率",
        "ROA": "总资产收益率", "Size": "企业规模（总资产对数）",
        "Dual": "两职合一", "SOE": "产权性质",
        "HighTQ": "高价值企业（TQ > 中位数）",
    },
    value_labels={
        "Dual": {0.0: "分离", 1.0: "合一"},
        "SOE": {0.0: "非国有", 1.0: "国有"},
        "HighTQ": {0.0: "低价值", 1.0: "高价值"},
    },
)


# ════════════════════════════════════════════════════════════════
# 数据集 2：问卷量表（双因子结构 + 人口学）
# ════════════════════════════════════════════════════════════════
N2 = 400
gender = RNG.binomial(1, 0.5, N2).astype(float)  # 1=女
age_group = RNG.choice([1, 2, 3], size=N2, p=[0.4, 0.35, 0.25]).astype(float)

# 真实潜变量：F1=数字化感知, F2=创新意愿
F1 = RNG.normal(0, 1, N2)
F2 = RNG.normal(0, 1, N2) + 0.3 * F1  # 两因子轻度相关
# F1 ← Q1-Q6 (载荷 0.7)；F2 ← Q7-Q12 (载荷 0.7)
Q = np.zeros((N2, 12))
for i in range(6):
    Q[:, i] = np.clip(np.round(3 + 0.7 * F1 + RNG.normal(0, 0.6, N2)), 1, 5)
for i in range(6, 12):
    Q[:, i] = np.clip(np.round(3 + 0.7 * F2 + RNG.normal(0, 0.6, N2)), 1, 5)

# 综合得分（用于 T-TEST / ONEWAY）：女性平均得分略高
total = Q.sum(axis=1).astype(float) + 1.5 * gender + RNG.normal(0, 2, N2)

df2 = pd.DataFrame({
    **{f"Q{i+1}": Q[:, i] for i in range(12)},
    "gender": gender, "age_group": age_group, "total": total,
})
save_sav(
    df2, "survey_likert",
    labels={**{f"Q{i+1}": f"题项{i+1}（5点李克特）" for i in range(12)},
            "gender": "性别", "age_group": "年龄段", "total": "总分"},
    value_labels={
        "gender": {0.0: "男", 1.0: "女"},
        "age_group": {1.0: "青年（<35）", 2.0: "中年（35-50）", 3.0: "中老年（>50）"},
    },
    measures={**{f"Q{i+1}": "ordinal" for i in range(12)},
              "gender": "nominal", "age_group": "ordinal"},
)


# ════════════════════════════════════════════════════════════════
# 数据集 3：实验设计（处理 × 时间，含重复测量）
# ════════════════════════════════════════════════════════════════
N3 = 150  # 每人 4 个时间点
subjects = np.repeat(np.arange(1, N3 + 1), 1)
treatment = RNG.choice([0, 1, 2], size=N3, p=[0.34, 0.33, 0.33]).astype(float)
intensity = RNG.choice([1, 2], size=N3).astype(float)  # 强度水平用于 2×3 ANOVA

# 4 个时间点的重复测量（处理组有时间效应）
base = RNG.normal(50, 8, N3)
t1 = base + RNG.normal(0, 3, N3)
t2 = base + 2 * treatment + RNG.normal(0, 3, N3)
t3 = base + 4 * treatment + 1.5 * intensity + RNG.normal(0, 3, N3)
t4 = base + 6 * treatment + 2.5 * intensity + RNG.normal(0, 3, N3)

df3 = pd.DataFrame({
    "subject": subjects.astype(float),
    "treatment": treatment, "intensity": intensity,
    "t1_baseline": t1, "t2_week2": t2, "t3_week4": t3, "t4_week8": t4,
    # 派生变量给配对 t 检验和 Wilcoxon 用
    "pre_test": t1, "post_test": t4,
})
save_sav(
    df3, "experiment",
    labels={
        "subject": "被试编号",
        "treatment": "处理组", "intensity": "强度水平",
        "t1_baseline": "基线测量", "t2_week2": "第2周",
        "t3_week4": "第4周", "t4_week8": "第8周",
        "pre_test": "前测", "post_test": "后测",
    },
    value_labels={
        "treatment": {0.0: "对照组", 1.0: "处理A", 2.0: "处理B"},
        "intensity": {1.0: "低强度", 2.0: "高强度"},
    },
)


# ════════════════════════════════════════════════════════════════
# 数据集 4：列联与多分类（行业 × 数字化等级）
# ════════════════════════════════════════════════════════════════
N4 = 800
industry = RNG.choice([1, 2, 3], size=N4, p=[0.4, 0.35, 0.25]).astype(float)
# 制造业更多基础数字化，服务业更多高级数字化
prob_map = {1: [0.5, 0.3, 0.2], 2: [0.3, 0.4, 0.3], 3: [0.2, 0.3, 0.5]}
digital_level = np.array([
    RNG.choice([1, 2, 3], p=prob_map[int(ind)]) for ind in industry
]).astype(float)
# 数字化等级 + 行业共同决定盈利水平
profit = (10 + 5 * digital_level + 3 * (industry == 3).astype(int)
          + RNG.normal(0, 4, N4))
firm_age = RNG.gamma(3, 2, N4)

df4 = pd.DataFrame({
    "industry": industry, "digital_level": digital_level,
    "profit": profit, "firm_age": firm_age,
})
save_sav(
    df4, "categorical",
    labels={
        "industry": "所属行业", "digital_level": "数字化等级",
        "profit": "盈利水平", "firm_age": "成立年限",
    },
    value_labels={
        "industry": {1.0: "制造业", 2.0: "服务业", 3.0: "科技业"},
        "digital_level": {1.0: "初级", 2.0: "中级", 3.0: "高级"},
    },
    measures={"industry": "nominal", "digital_level": "ordinal"},
)


# ════════════════════════════════════════════════════════════════
# 数据集 5：非参数（偏态收入 × 三组地区）
# ════════════════════════════════════════════════════════════════
N5 = 300
region = RNG.choice([1, 2, 3], size=N5, p=[0.4, 0.35, 0.25]).astype(float)
# 对数正态偏态分布；东部更高
income = np.exp(RNG.normal(np.array([10.5, 10.0, 9.5])[region.astype(int) - 1],
                            0.6, N5))
satisfaction = np.clip(np.round(5 + 0.3 * (region - 1) * 2
                                + RNG.normal(0, 1, N5)), 1, 10).astype(float)
# 排名变量
rank_var = RNG.permutation(N5).astype(float) + 1

df5 = pd.DataFrame({
    "region": region, "income": income,
    "satisfaction": satisfaction, "rank_var": rank_var,
})
save_sav(
    df5, "nonparametric",
    labels={
        "region": "地区", "income": "年收入（元）",
        "satisfaction": "满意度（1-10）", "rank_var": "综合排名",
    },
    value_labels={"region": {1.0: "东部", 2.0: "中部", 3.0: "西部"}},
    measures={"region": "nominal", "satisfaction": "ordinal", "rank_var": "scale"},
)


# ════════════════════════════════════════════════════════════════
# 数据集 6：聚类 + 生存分析
# ════════════════════════════════════════════════════════════════
N6 = 500
# 三个真实簇
cluster_true = RNG.choice([0, 1, 2], size=N6, p=[0.4, 0.35, 0.25])
cluster_means = np.array([[10, 5, 20], [50, 25, 60], [80, 70, 30]])
features = cluster_means[cluster_true] + RNG.normal(0, 5, (N6, 3))
x1, x2, x3 = features[:, 0], features[:, 1], features[:, 2]

# 生存数据：簇 0 风险最高
hazard_rate = np.array([0.05, 0.02, 0.01])[cluster_true]
survival_time = RNG.exponential(1 / hazard_rate)
censor_time = RNG.uniform(30, 100, N6)
observed_time = np.minimum(survival_time, censor_time)
event = (survival_time <= censor_time).astype(float)

df6 = pd.DataFrame({
    "x1_spend": x1, "x2_freq": x2, "x3_recency": x3,
    "true_segment": cluster_true.astype(float),
    "time": observed_time, "event": event,
})
save_sav(
    df6, "cluster_survival",
    labels={
        "x1_spend": "消费金额", "x2_freq": "购买频次", "x3_recency": "最近购买间隔",
        "true_segment": "真实分群（仅供对比）",
        "time": "观察时长（天）", "event": "事件发生（1=流失，0=删失）",
    },
    value_labels={"true_segment": {0.0: "活跃低值", 1.0: "中间稳定", 2.0: "高频高价值"}},
)


print("\n══════════════════════════════════════")
print(f"6 个数据集已生成于：{DATASETS}")
