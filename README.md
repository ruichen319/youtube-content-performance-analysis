# YouTube Content Performance and Account Test Priorities

Analyzed 1,401 videos across 29 public YouTube channels to recommend three initial Shorts account tests based on format performance, content topics, and the strength of the available evidence.

[Presentation PDF](presentation/youtube-content-performance-analysis.pdf) · [Python analysis](src/analyze.py) · [Analysis notebook](notebooks/youtube_analysis.ipynb) · [Creator sensitivity chart](outputs/figures/channel_sensitivity.svg) · [Data and methodology](docs/data_and_methodology.md)

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

Python/pandas techniques include validated joins, grouped aggregation, reshaping, missing-value handling, sensitivity analysis, and within-channel benchmarks. Engagement differences use percentage points.

## Data and analytical unit

The YouTube Data API snapshot was collected on 27 October 2026, selecting up to 50 historical high-view videos per channel. The original 1,407 videos from 30 channels become **1,401 videos from 29 channels for format analysis** after excluding one off-topic channel; topic analysis includes 1,341 videos. The eligible sample contains 20 lawyer-hosted and nine AI-presentation channels.

Each row represents a video. Engagement summaries are medians of available video-level rates. Topic labels were AI-assisted from titles and description metadata, without full-video human review. Fictional stories remain separate from case stories. See the [data guide](docs/data_and_methodology.md) for definitions and eligibility.

## Findings

**Shorts merit an initial test, but pooled comparisons have limits.** Lawyer-hosted Shorts have 7.12M median views (328 videos, 11 channels), versus 603K for long-form (672 videos, 16 channels). AI-presentation Shorts have 256.6K (330 videos, nine channels), versus 2.2K for long-form (71 videos, only two channels). Shorts have higher pooled engagement only in the lawyer-hosted group; this is not a universal format advantage.

**Entertainment results depend heavily on one creator.** Law By Mike contributes 11 of 20 entertainment Shorts across three channels. Removing it reduces median views from 82.70M to 446K, with nine videos across two channels remaining.

**Education and case stories retain substantial views after that exclusion.** Legal education has 9.61M median views and 4.33% median engagement (116 videos, seven channels); case stories have 4.14M and 4.48% (34 videos, four channels). These support parallel topic tests, without proving a topic effect.

**AI case stories provide a high-view signal for an exploratory pilot.** The directly labeled AI Shorts case-story sample has 2.28M median views and 2.09% median engagement (one video, one channel), versus 179.5K and 1.16% for legal education (17 videos, one channel). Case stories have the highest reported median views among the AI Shorts categories; engagement is close to, but below, fictional legal/police stories at 2.16% (315.3K median views; 301 videos, eight channels). This supports prioritizing a case-story pilot, not claiming a repeatable topic advantage. Fictional stories remain separate and do not validate factual case storytelling.

## Proposed next steps

**Prioritize three Shorts accounts for the initial test:**

1. **Lawyer-hosted legal education:** test concise explanations of legal questions and processes.
2. **Lawyer-hosted case stories:** test case narratives alongside education as a separate topic route.
3. **AI-presented case stories:** test legal case narratives using AI presentation. The existing sample's 2.28M median views and 2.09% median engagement support an exploratory pilot; the evidence is only one labeled video from one channel and requires validation before scaling.

Treat account 3 as a validation test: expand the directly labeled case-story sample and assess whether the signal holds beyond one video and one channel. Before production, review source material and provisional topic labels. Compare pilot views and engagement at equal video ages, tracking each account separately before deciding continued production. Separate accounts do not isolate a causal AI effect.

These are proposed tests; none has been run. A Tableau dashboard is planned, not completed.

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

- Historical hits do not represent typical uploads or new-account expectations.
- Video age, audience, language, and creator differences remain.
- Presentation groups reflect public descriptions, not independent credential or synthetic-media verification.
- Metadata-based labels require human review. Public metrics do not establish retention, conversions, revenue, or causal effects.
