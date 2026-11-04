"""Anonymized, portable version of the supplied YouTube analysis notebook."""

from pathlib import Path
try:
    ROOT = Path(__file__).resolve().parents[1]
except NameError:
    ROOT = Path.cwd().resolve()
    if not (ROOT / 'data').exists():
        ROOT = ROOT.parent
if not (ROOT / 'data').exists():
    raise FileNotFoundError('Run from the repository root or notebooks directory.')
OUT = ROOT / 'outputs' / 'tables'
OUT.mkdir(parents=True, exist_ok=True)
FIGURES = ROOT / 'outputs' / 'figures'
FIGURES.mkdir(parents=True, exist_ok=True)
if 'display' not in globals():
    try:
        from IPython.display import display
    except ImportError:
        def display(value):
            if hasattr(value, 'data'):
                value = value.data
            if hasattr(value, 'to_string'):
                print(value.to_string(index=False))
            else:
                print(value)

import pandas as pd
snapshot = pd.read_csv(ROOT / 'data/public_video_snapshot.csv', dtype={'video_id':'string','channel_id':'string'})
if snapshot.video_id.isna().any() or snapshot.video_id.duplicated().any():
    raise ValueError('Each snapshot row must have a unique video_id.')
format_df = snapshot.loc[snapshot.analysis_format_eligible.eq(True)].copy()
content_df = snapshot.loc[snapshot.analysis_topic_eligible.eq(True)].copy()
assert set(content_df.video_id).issubset(set(format_df.video_id))
print(f'Format analysis: {len(format_df):,} videos from {format_df.channel_id.nunique()} channels')
print(f'Topic analysis: {len(content_df):,} videos from {content_df.channel_id.nunique()} channels')
display(format_df[['channel_name','account_type','title','video_type','view_count','like_count','comment_count']].head())


# 对两份数据执行相同处理
for df in [format_df, content_df]:

    # 确保指标是数值类型
    for col in ["view_count", "like_count", "comment_count"]:
        df[col] = pd.to_numeric(df[col], errors="raise")

    # 播放量为0时不计算互动率
    valid_views = df["view_count"].where(df["view_count"] > 0)

    df["engagement_rate"] = (
        df["like_count"] + df["comment_count"]
    ) / valid_views

# 检查格式比较数据中的Missing情况
print("Missing values in the format sample:")
print(
    format_df[
        ["view_count", "like_count", "comment_count", "engagement_rate"]
    ].isna().sum()
)

# 仅为展示创建百分比列，原始互动率仍保留为数值
preview = format_df[
    ["channel_name", "video_type", "view_count", "engagement_rate"]
].head().copy()

preview["engagement_rate"] = preview["engagement_rate"].map(
    lambda x: f"{x:.2%}" if pd.notna(x) else "Missing"
)

display(preview)

# 按账户类型和Video format汇总
format_summary = (
    format_df
    .groupby(["account_type", "video_type"], observed=True)
    .agg(
        sample_videos=("video_id", "size"),
        sample_channels=("channel_id", "nunique"),
        median_views=("view_count", "median"),
        valid_engagement_videos=("engagement_rate", "count"),
        median_engagement_rate=("engagement_rate", "median")
    )
    .reset_index()
)

# 分别显示两组结果
for account_type in ["Lawyer-led", "AI-presented"]:

    print(f"\n{account_type}：Shorts vs Long-form")

    result = format_summary[
        format_summary["account_type"] == account_type
    ].copy()

    result = result.rename(columns={
        "video_type": "Video format",
        "sample_videos": "Videos",
        "sample_channels": "Channels",
        "median_views": "Median views",
        "valid_engagement_videos": "Valid engagement videos",
        "median_engagement_rate": "Median engagement"
    })

    # 只调整展示格式，不改变 format_summary 中的数值
    result["Median views"] = result["Median views"].map(
        lambda x: f"{x:,.0f}"
    )

    result["Median engagement"] = result["Median engagement"].map(
        lambda x: f"{x:.2%}" if pd.notna(x) else "Missing"
    )

    display(result.drop(columns="account_type"))

# 每个Channel分别计算两种格式的表现
channel_format = (
    format_df
    .groupby(
        ["account_type", "channel_id", "channel_name", "video_type"],
        observed=True
    )
    .agg(
        video_count=("video_id", "size"),
        median_views=("view_count", "median"),
        valid_engagement=("engagement_rate", "count"),
        median_engagement=("engagement_rate", "median")
    )
    .reset_index()
)

# 将 Shorts 和长视频并排放置
channel_comparison = channel_format.pivot(
    index=["account_type", "channel_id", "channel_name"],
    columns="video_type",
    values=[
        "video_count",
        "median_views",
        "valid_engagement",
        "median_engagement"
    ]
)

channel_comparison.columns = [
    f"{metric}_{video_format}"
    for metric, video_format in channel_comparison.columns
]

channel_comparison = channel_comparison.reset_index()

# 只保留Channels with at least 5 videos in both formats
channel_comparison = channel_comparison[
    (channel_comparison["video_count_Shorts"] >= 5)
    & (channel_comparison["video_count_Long-form"] >= 5)
].copy()

# ShortsMedian views ÷ 长视频Median views
channel_comparison["views_ratio"] = (
    channel_comparison["median_views_Shorts"]
    / channel_comparison["median_views_Long-form"].where(
        channel_comparison["median_views_Long-form"] > 0
    )
)

# 互动率差值：单位为“百分点”
# 两种格式都至少有5条有效互动数据时才计算
valid_engagement = (
    (channel_comparison["valid_engagement_Shorts"] >= 5)
    & (channel_comparison["valid_engagement_Long-form"] >= 5)
)

channel_comparison["engagement_difference_pp"] = (
    (
        channel_comparison["median_engagement_Shorts"]
        - channel_comparison["median_engagement_Long-form"]
    ) * 100
).where(valid_engagement)

# 分别展示Lawyer-led和AI-presented
for account_type in ["Lawyer-led", "AI-presented"]:

    print(f"\n{account_type}：Within-channel comparison")

    result = channel_comparison[
        channel_comparison["account_type"] == account_type
    ][[
        "channel_name",
        "video_count_Shorts",
        "video_count_Long-form",
        "median_views_Shorts",
        "median_views_Long-form",
        "views_ratio",
        "median_engagement_Shorts",
        "median_engagement_Long-form",
        "engagement_difference_pp"
    ]].copy()

    result = result.rename(columns={
        "channel_name": "Channel",
        "video_count_Shorts": "Shorts videos",
        "video_count_Long-form": "Long-form videos",
        "median_views_Shorts": "Shorts median views",
        "median_views_Long-form": "Long-form median views",
        "views_ratio": "Shorts / Long-form median views",
        "median_engagement_Shorts": "Shorts median engagement",
        "median_engagement_Long-form": "Long-form median engagement",
        "engagement_difference_pp": "Engagement difference (pp)"
    })

    display(result)

# 统计每组两种格式的Videos量
format_share = (
    format_df
    .groupby(["account_type", "video_type"], observed=True)
    .size()
    .reset_index(name="video_count")
)

# 占比 = 该格式Videos ÷ 该账户组的样本视频总数
format_share["video_share"] = (
    format_share["video_count"]
    / format_share.groupby("account_type")["video_count"].transform("sum")
)

# 分别展示
for account_type in ["Lawyer-led", "AI-presented"]:

    print(f"\n{account_type}：长短视频占比")

    result = (
        format_share[
            format_share["account_type"] == account_type
        ]
        .drop(columns="account_type")
        .rename(columns={
            "video_type": "Video format",
            "video_count": "Videos",
            "video_share": "样本占比"
        })
        .reset_index(drop=True)
    )

    display(result)

# 按账户类型和Content category汇总
content_summary = (
    content_df
    .groupby(
        ["account_type", "content_category_label"],
        observed=True
    )
    .agg(
        sample_videos=("video_id", "size"),
        sample_channels=("channel_id", "nunique"),
        median_views=("view_count", "median"),
        valid_engagement_videos=("engagement_rate", "count"),
        median_engagement_rate=("engagement_rate", "median")
    )
    .reset_index()
)

# 在各账户组内部，按Median views排序
content_summary = content_summary.sort_values(
    ["account_type", "median_views"],
    ascending=[True, False]
)

for account_type in ["Lawyer-led", "AI-presented"]:

    print(f"\n{account_type}：Content category performance")

    result = content_summary[
        content_summary["account_type"] == account_type
    ].copy()

    # 提示样本局限，不删除这些类别
    result["Sample note"] = result.apply(
        lambda row: "；".join(
            message
            for condition, message in [
                (row["sample_videos"] < 5, "Fewer than 5 videos"),
                (row["sample_channels"] < 3, "Fewer than 3 channels"),
                (
                    row["valid_engagement_videos"] < 5,
                    "Fewer than 5 engagement observations"
                )
            ]
            if condition
        ),
        axis=1
    )

    result = result.rename(columns={
        "content_category_label": "Content category",
        "sample_videos": "Videos",
        "sample_channels": "Channels",
        "median_views": "Median views",
        "valid_engagement_videos": "Valid engagement videos",
        "median_engagement_rate": "Median engagement"
    })

    display(result.drop(columns="account_type").reset_index(drop=True))

# 按账户类型、Video format、Content category汇总
content_format_summary = (
    content_df
    .groupby(
        ["account_type", "video_type", "content_category_label"],
        observed=True
    )
    .agg(
        sample_videos=("video_id", "size"),
        sample_channels=("channel_id", "nunique"),
        median_views=("view_count", "median"),
        valid_engagement_videos=("engagement_rate", "count"),
        median_engagement_rate=("engagement_rate", "median")
    )
    .reset_index()
)

# 分别显示：律师Shorts、律师长视频、AI Shorts、AI长视频
for account_type in ["Lawyer-led", "AI-presented"]:
    for video_type in ["Shorts", "Long-form"]:

        result = content_format_summary[
            (content_format_summary["account_type"] == account_type)
            & (content_format_summary["video_type"] == video_type)
        ].copy()

        if result.empty:
            continue

        print(f"\n{account_type}｜{video_type}：Content category performance")

        result = result.sort_values(
            "median_views",
            ascending=False
        )

        result["Sample note"] = result.apply(
            lambda row: "；".join(
                message
                for condition, message in [
                    (row["sample_videos"] < 5, "Fewer than 5 videos"),
                    (row["sample_channels"] < 3, "Fewer than 3 channels"),
                    (
                        row["valid_engagement_videos"] < 5,
                        "Fewer than 5 engagement observations"
                    )
                ]
                if condition
            ),
            axis=1
        )

        result = result.rename(columns={
            "content_category_label": "Content category",
            "sample_videos": "Videos",
            "sample_channels": "Channels",
            "median_views": "Median views",
            "valid_engagement_videos": "Valid engagement videos",
            "median_engagement_rate": "Median engagement"
        })

        display(result.drop(columns=["account_type","video_type"]).reset_index(drop=True))

# 先检查Lawyer-led Shorts 的Channel composition
lawyer_shorts = content_df[
    (content_df["account_type"] == "Lawyer-led")
    & (content_df["video_type"] == "Shorts")
].copy()

channel_contribution = (
    lawyer_shorts
    .groupby(
        ["content_category_label", "channel_id", "channel_name"],
        observed=True
    )
    .agg(
        sample_videos=("video_id", "size"),
        median_views=("view_count", "median"),
        valid_engagement_videos=("engagement_rate", "count"),
        median_engagement_rate=("engagement_rate", "median")
    )
    .reset_index()
)

# 每个Channel占该类别样本视频的比例
category_total = (
    channel_contribution
    .groupby("content_category_label")["sample_videos"]
    .transform("sum")
)

channel_contribution["sample_share"] = (
    channel_contribution["sample_videos"] / category_total
)

# 每个类别单独展示
category_order = [
    "Entertainment and challenges",
    "Legal education",
    "Case stories",
    "News and commentary"
]

for category in category_order:

    print(f"\nLawyer-led Shorts｜{category}：Channel composition")

    result = channel_contribution[
        channel_contribution["content_category_label"] == category
    ].sort_values(
        ["sample_videos", "median_views"],
        ascending=False
    )

    result = result[[
        "channel_name",
        "sample_videos",
        "sample_share",
        "median_views",
        "valid_engagement_videos",
        "median_engagement_rate"
    ]].rename(columns={
        "channel_name": "Channel",
        "sample_videos": "Videos",
        "sample_share": "Share of category videos",
        "median_views": "Median views",
        "valid_engagement_videos": "Valid engagement videos",
        "median_engagement_rate": "Median engagement"
    })

    display(result.reset_index(drop=True))

# 两种Scenario：All channels、暂时Exclude Law By Mike
comparison_data = {
    "All channels": lawyer_shorts,
    "Exclude Law By Mike": lawyer_shorts[
        lawyer_shorts["channel_name"] != "Law By Mike"
    ]
}

comparison_tables = []

for scenario, df in comparison_data.items():

    summary = (
        df.groupby("content_category_label", observed=True)
        .agg(
            sample_videos=("video_id", "size"),
            sample_channels=("channel_id", "nunique"),
            median_views=("view_count", "median"),
            valid_engagement_videos=("engagement_rate", "count"),
            median_engagement_rate=("engagement_rate", "median")
        )
        .reset_index()
    )

    summary["scenario"] = scenario
    comparison_tables.append(summary)

sensitivity_summary = pd.concat(
    comparison_tables,
    ignore_index=True
)

# 每个类别并排查看两种Scenario
for category in category_order:

    print(f"\nLawyer-led Shorts｜{category}")

    result = sensitivity_summary[
        sensitivity_summary["content_category_label"] == category
    ][[
        "scenario",
        "sample_videos",
        "sample_channels",
        "median_views",
        "valid_engagement_videos",
        "median_engagement_rate"
    ]].rename(columns={
        "scenario": "Scenario",
        "sample_videos": "Videos",
        "sample_channels": "Channels",
        "median_views": "Median views",
        "valid_engagement_videos": "Valid engagement videos",
        "median_engagement_rate": "Median engagement"
    })

    display(result.reset_index(drop=True))

MIN_SAMPLE = 5

# 1. 每个Channel自己的 Shorts 基准
# 使用 format_df，避免漏掉题材不明或非法律主题的 Shorts
shorts_baseline = (
    format_df[
        format_df["video_type"] == "Shorts"
    ]
    .groupby(
        ["account_type", "channel_id"],
        observed=True
    )
    .agg(
        baseline_videos=("video_id", "size"),
        baseline_median_views=("view_count", "median"),
        baseline_valid_engagement=("engagement_rate", "count"),
        baseline_median_engagement=("engagement_rate", "median")
    )
    .reset_index()
)

# 2. 每个Channel、每种题材的 Shorts 表现
shorts_categories = (
    content_df[
        content_df["video_type"] == "Shorts"
    ]
    .groupby(
        [
            "account_type",
            "channel_id",
            "channel_name",
            "content_category_label"
        ],
        observed=True
    )
    .agg(
        category_videos=("video_id", "size"),
        category_valid_views=("view_count", "count"),
        category_median_views=("view_count", "median"),
        category_valid_engagement=("engagement_rate", "count"),
        category_median_engagement=("engagement_rate", "median")
    )
    .reset_index()
)

# 3. 合并同一Channel的基准
relative_shorts = shorts_categories.merge(
    shorts_baseline,
    on=["account_type", "channel_id"],
    how="left",
    validate="many_to_one"
)

# 4. 播放量相对倍数
# 例如 1.50 表示：该题材播放中位数是Channel基准的1.5倍
relative_shorts["relative_views"] = (
    relative_shorts["category_median_views"]
    / relative_shorts["baseline_median_views"].where(
        relative_shorts["baseline_median_views"] > 0
    )
).where(
    relative_shorts["category_valid_views"] >= MIN_SAMPLE
)

# 5. 互动率相对于Channel基准的差值，单位为百分点
valid_engagement_comparison = (
    (relative_shorts["category_valid_engagement"] >= MIN_SAMPLE)
    & (relative_shorts["baseline_valid_engagement"] >= MIN_SAMPLE)
)

relative_shorts["engagement_difference_pp"] = (
    (
        relative_shorts["category_median_engagement"]
        - relative_shorts["baseline_median_engagement"]
    ) * 100
).where(valid_engagement_comparison)

# 6. Sample note
relative_shorts["sample_note"] = relative_shorts.apply(
    lambda row: "；".join(
        message
        for condition, message in [
            (
                row["category_valid_views"] < MIN_SAMPLE,
                "Fewer than 5 view observations"
            ),
            (
                row["category_valid_engagement"] < MIN_SAMPLE,
                "Fewer than 5 engagement observations"
            )
        ]
        if condition
    ),
    axis=1
)

# 7. Lawyer-led、AI-presented分别展示
for account_type in ["Lawyer-led", "AI-presented"]:

    print(f"\n{account_type}：Categories relative to the same channel Shorts baseline")

    result = relative_shorts[
        relative_shorts["account_type"] == account_type
    ].sort_values(
        ["channel_name", "relative_views"],
        ascending=[True, False],
        na_position="last"
    )

    result = result[[
        "channel_name",
        "content_category_label",
        "baseline_videos",
        "category_videos",
        "baseline_median_views",
        "category_median_views",
        "relative_views",
        "category_valid_engagement",
        "baseline_median_engagement",
        "category_median_engagement",
        "engagement_difference_pp",
        "sample_note"
    ]].rename(columns={
        "channel_name": "Channel",
        "content_category_label": "Content category",
        "baseline_videos": "Channel Shorts sample",
        "category_videos": "Category videos",
        "baseline_median_views": "Channel median views",
        "category_median_views": "Category median views",
        "relative_views": "Relative views",
        "category_valid_engagement": "Valid category engagement",
        "baseline_median_engagement": "Channel median engagement",
        "category_median_engagement": "Category median engagement",
        "engagement_difference_pp": "Engagement difference (pp)",
        "sample_note": "Sample note"
    })

    display(result.reset_index(drop=True))

import sys
sys.path.insert(0,str(ROOT/'src'))
from plot_svg import bars, COLORS
tables={'format_by_group':format_summary,'format_by_channel':channel_format,
        'within_channel_format_comparison':channel_comparison,'content_by_group':content_summary,
        'content_by_format':content_format_summary,'lawyer_shorts_channel_contribution':channel_contribution,
        'lawyer_shorts_sensitivity':sensitivity_summary,'shorts_relative_to_channel_baseline':relative_shorts}
for name,table in tables.items():table.to_csv(OUT/f'{name}.csv',index=False)
quality=pd.DataFrame([{'sample':'raw snapshot','videos':len(snapshot),'channels':snapshot.channel_id.nunique()},
                      {'sample':'format analysis','videos':len(format_df),'channels':format_df.channel_id.nunique()},
                      {'sample':'topic analysis','videos':len(content_df),'channels':content_df.channel_id.nunique()}])
quality.to_csv(OUT/'sample_flow.csv',index=False)
bars(FIGURES/'format_median_views.svg',[(f'{r.account_type} | {r.video_type}',r.median_views,COLORS[0 if r.account_type=='Lawyer-led' else 1]) for r in format_summary.itertuples(index=False)],
     'Video format comparisons depend on the channel group','Historical high-view sample; medians describe these selected videos','Median cumulative public views')

law=content_format_summary[(content_format_summary.account_type=='Lawyer-led') & (content_format_summary.video_type=='Shorts')].sort_values('median_views',ascending=False)
bars(FIGURES/'lawyer_shorts_topics.svg',[(f'{r.content_category_label} (n={r.sample_videos})',r.median_views,COLORS[0]) for r in law.itertuples(index=False)],
     'Lawyer-led Shorts: category performance needs a channel check','AI-assisted topic labels; not yet validated by full-video human review','Median cumulative public views')
sensitivity_rows=[]
for category in ['Entertainment and challenges','Legal education','Case stories']:
    scenarios=sensitivity_summary[sensitivity_summary.content_category_label.eq(category)]
    for r in scenarios.itertuples(index=False):
        sensitivity_rows.append((f'{r.content_category_label} | {r.scenario}',r.median_views,COLORS[0 if r.scenario=='All channels' else 1]))
bars(FIGURES/'channel_sensitivity.svg',sensitivity_rows,
     'One creator can change the pooled topic ranking','Lawyer-led Shorts; compare all channels with the sample excluding Law By Mike','Median cumulative public views')
display(quality)

