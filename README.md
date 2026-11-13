# YouTube Content Performance and Account Test Priorities

Analyzed 1,401 videos across 29 public YouTube channels to recommend three initial Shorts account tests based on format performance, content topics, and the strength of the available evidence.

[Presentation PDF](presentation/youtube-content-performance-analysis.pdf) · [Python analysis](src/analyze.py) · [Analysis notebook](notebooks/youtube_analysis.ipynb) · [Creator sensitivity chart](outputs/figures/channel_sensitivity.svg) · [Data and methodology](docs/data_and_methodology.md)

The recommendations below reflect the final presentation and Tableau analysis. The methodology guide retains earlier pilot proposals.
## Business question

**Which three YouTube accounts should the client test first?**

The analysis compares Shorts and long-form videos, identifies promising topics, and recalculates topic results without a dominant creator to check whether one channel drives a category's apparent success. The objective is to prioritize account tests, not forecast new-account performance.

Two presentation groups are compared separately:

- **Lawyer-hosted channels:** people identifying themselves as lawyers explain legal questions or cases (`Lawyer-led` in the tables).
- **Channels using AI-generated narration, presenters, or characters:** the delivery method uses AI; these are legal-themed videos, not videos teaching AI (`AI-presented` in the tables).

## Analytical approach

1. Check video IDs, preserve missing metrics, and apply separate format- and topic-eligibility flags.
2. Calculate video-level engagement as `(likes + comments) / views`; retain missing rates when interactions are missing or views are zero.
3. Compare median views and engagement by presentation group, format, and topic, reporting video and channel counts.
4. Compare formats within channels with at least five sampled videos in each format; require five valid engagement observations for engagement comparisons.
5. Remove Law By Mike and recalculate lawyer-hosted Shorts topic medians to check dependence on that creator.
6. Compare each Shorts topic with its channel's overall Shorts median, suppressing view ratios for topics with fewer than five valid observations.
7. For the third pilot, compare four Shorts candidates after excluding Law By Mike. Count videos meeting both the view and engagement thresholds, then check how many channels contributed qualifying videos.

Python/pandas techniques include validated joins, grouped aggregation, reshaping, missing-value handling, sensitivity analysis, and within-channel benchmarks. Engagement differences use percentage points.

## Data and analytical unit

The YouTube Data API snapshot was collected on 27 October 2026, selecting up to 50 historical high-view videos per channel. The original 1,407 videos from 30 channels become **1,401 videos from 29 channels for format analysis** after excluding one off-topic channel; topic analysis includes 1,341 videos. The eligible sample contains 20 lawyer-hosted and nine AI-presentation channels.

Each row represents a video. Engagement summaries are medians of available video-level rates. Topic labels were AI-assisted from titles and description metadata, without full-video human review. Fictional stories remain separate from case stories. See the [data guide](docs/data_and_methodology.md) for definitions and eligibility.

## Findings

**Shorts merit an initial test, but pooled comparisons have limits.** Lawyer-hosted Shorts have 7.12M median views (328 videos, 11 channels), versus 603K for long-form (672 videos, 16 channels). AI-presentation Shorts have 256.6K (330 videos, nine channels), versus 2.2K for long-form (71 videos, only two channels). Shorts have higher pooled engagement only in the lawyer-hosted group; this is not a universal format advantage.

**Entertainment results depend heavily on one creator.** Law By Mike contributes 11 of 20 entertainment Shorts across three channels. Removing it reduces median views from 82.70M to 446K, with nine videos across two channels remaining.

**Education and case stories retain substantial views after that exclusion.** Legal education has 9.61M median views and 4.33% median engagement (116 videos, seven channels); case stories have 4.14M and 4.48% (34 videos, four channels). These support parallel topic tests, without proving a topic effect.

## Choosing the third Shorts pilot

**Lawyer-led News / Commentary is the third pilot because it combines 4.11% median engagement with the most videos meeting both benchmarks among the four shortlisted candidates.** It had 296,694 median views and 81 videos across eight channels. Of the 79 videos with measurable engagement, 20 met both benchmarks, across three channels.

| Candidate | Median views | Median engagement | Sample videos / channels | Qualified / measurable videos | Qualifying channels |
| --- | ---: | ---: | ---: | ---: | ---: |
| AI-presented Case Stories | 2,282,456 | 2.09% | 1 / 1 | 1 / 1 | 1 |
| AI-presented Fictional Legal Stories | 315,329 | 2.16% | 301 / 8 | 14 / 256 | 4 |
| Lawyer-led Entertainment | 446,142 | 4.76% | 9 / 2 | 1 / 9 | 1 |
| **Lawyer-led News / Commentary** | **296,694** | **4.11%** | **81 / 8** | **20 / 79** | **3** |

The comparison includes Shorts only and excludes Law By Mike. All 392 videos count toward sample size and median views. The 345 videos with measurable engagement are used for median engagement and benchmark comparisons. A video qualified if it reached both cutoffs set by the one observed AI-presented case story, approximately 2.28M views and 2.09% engagement. The counts use the unrounded values.

AI-presented Fictional Legal Stories had slightly higher median views and qualifying videos from four channels, compared with three for News / Commentary. News / Commentary had higher median engagement and more qualifying videos at the selected cutoffs. Entertainment had the highest median engagement, with nine sampled videos across two channels and one qualifying video. The AI-presented Case Stories row contains a single video from a single channel.

## Proposed next steps

1. **Lawyer-led Legal Education.** Answer recurring legal questions and explain practical next steps.
2. **Lawyer-led Case Stories.** Retell completed cases and explain their outcomes.
3. **Lawyer-led News / Commentary.** Explain current legal news and recent case developments.

Record cumulative views and engagement rate seven days after each Short goes live. Compare results across the three pilots before scaling.

## Tableau dashboards

[Download Tableau workbook (.twbx)](presentation/tableau-dashboards.twbx) and open it in Tableau to explore both dashboards.

- **YouTube Account Test Priorities** compares formats and Shorts topics and presents the first two pilot recommendations.
- **Choosing the Third Shorts Pilot** compares the four candidates and shows the video-level views and engagement behind the third recommendation.

## Repository structure

```text
youtube-content-performance-analysis/
├── README.md
├── presentation/         # Business presentation PDF
├── src/                  # Analysis and chart helper
├── notebooks/            # Executed notebook
├── data/                 # Public-data snapshot and label status
├── outputs/
│   ├── tables/           # Format, topic and sensitivity comparisons
│   └── figures/
├── docs/                 # Definitions and methodology
├── requirements.txt
└── requirements-notebook.txt
```

## How to run

From the repository root, using Python 3.10 or later:

```bash
python -m pip install -r requirements.txt
python src/analyze.py
```

The included snapshot supports offline reproduction without an API key. Review results under `outputs/`, or install `requirements-notebook.txt` for Jupyter. Seven result tables matched the original analysis numerically after label translation.

## Limitations

- The historical high-view sample describes past hits. Performance on new channels remains uncertain.
- Creator concentration matters. After excluding Law By Mike, removing the channel with the most sampled videos in each topic reduces median views from 9.61M to 1.31M for Legal Education and from 4.14M to 1.87M for Case Stories. One channel supplied 12 of the 20 qualifying News / Commentary videos.
- The joint benchmark comes from one AI case story. At alternative cutoffs of 1M views and 2% engagement, AI fiction has 51 qualifying videos and News / Commentary has 24. The third-pilot choice prioritizes observed engagement and depends on how the benchmarks are set.
- Video age, audience, language, and creator differences remain.
- Presentation groups reflect public descriptions, not independent credential or synthetic-media verification.
- Metadata-based labels require human review. Public metrics do not establish retention, conversions, revenue, or causal effects.
