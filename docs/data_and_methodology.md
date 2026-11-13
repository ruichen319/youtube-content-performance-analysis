# Data and methodology

## Snapshot lineage

The frozen source was collected on 2026-10-27. It contains 1,407 videos from 30 purposefully selected channels, using up to 50 historical high-view public videos per channel after upload-playlist enumeration. Deleted or private videos are outside the accessible source. The public package reproduces the analysis from a selected-column snapshot; it does not independently rerun or audit all historical API responses.

The sample's publication dates span 2015-08-19 to 2026-10-22. These are different exposure periods, not a common publication window. Metrics reflect the retrieval timestamp, not performance at publication.

The format analysis excludes a channel whose six current sampled videos were nonlegal, leaving 1,401 videos and 29 channels. The legal-topic analysis further excludes 43 unclear and 17 nonlegal rows, leaving 1,341 videos.

## Public file and fields

`data/public_video_snapshot.csv` is a whitelist-only extract. It includes public channel/video identifiers, titles, timestamps, numeric public metrics, sampling groups, analysis eligibility, format-evidence method, and annotation status. Full descriptions, external CTA destinations, internal documents, messages, and credentials are omitted.

| Fields | Purpose |
|---|---|
| `video_id`, `channel_id`, `channel_name` | Unique video key and public creator identity |
| `published_at`, `retrieved_at` | Publication and frozen metric-snapshot times |
| `view_count`, `like_count`, `comment_count` | Public cumulative snapshot counts; blanks remain missing |
| `duration_seconds`, `video_type`, `format_method` | Duration and recorded format verification method |
| `account_type` | `Lawyer-led`: people identifying as lawyers host legal explanations or cases. `AI-presented`: narration, presenters, or characters are described as AI-generated; this is not content teaching AI. These sampling groups are not independent credential or synthetic-media verification. |
| `content_category`, `content_category_label` | Machine-readable and readable provisional topic labels |
| `category_confidence`, `category_review_status` | Metadata annotation confidence and workflow status |
| `human_content_review_status` | `not_reviewed` throughout this snapshot |
| `category_evidence_scope` | Explicitly limits topic evidence to metadata |
| `analysis_format_eligible`, `analysis_topic_eligible` | Preserve the original sample-selection decisions |

## Calculations

- Video-level engagement rate = `(like_count + comment_count) / view_count`. If either interaction field is missing or views are zero, the rate is missing. Group summaries use the median of available video-level rates, not a ratio of aggregate sums.
- Same-channel format comparisons require at least five sampled videos of each format. Engagement differences additionally require five valid rates in each format; differences are percentage points.
- Lawyer-led Shorts topic sensitivity uses the same calculation with all sampled channels and after excluding Law By Mike. This checks dependence on creator composition; it is not a causal adjustment or a matched experiment.
- Topic-relative Shorts views = topic median views divided by that channel's overall Shorts median. Ratios are suppressed for categories with fewer than five valid view observations. The overall baseline includes the topic being compared, so this is a descriptive benchmark rather than an independent control group.

## Category boundaries

The taxonomy separates legal education, case stories, news/commentary, courtroom coverage, fictional legal stories, entertainment/challenges, nonlegal content, and insufficient evidence. AI-assisted labels have not been confirmed by full-video human review. A case-story label describes a narrative category and does not establish that a publisher's account is factually verified.

Shorts labels use recorded platform-tab evidence; some long-form labels use the recorded duration-exclusion method. The public package preserves these decisions and does not infer Shorts merely from a short duration or hashtag.

## Shorts pilot selection

The three proposed Shorts pilots are **Lawyer-led Legal Education**, **Lawyer-led Case Stories**, and **Lawyer-led News / Commentary**.

The third-pilot comparison covers four candidates and excludes Law By Mike. All 392 sampled Shorts count toward sample size and median views. The 345 with measurable engagement count toward median engagement and the benchmark comparison. To qualify, a video had to reach both thresholds set by the single observed AI-presented case story: 2,282,456 views and an engagement rate of `47,791 / 2,282,456` (about 2.09%). The comparison uses the unrounded rate.

News / Commentary was selected for its 4.11% median engagement and the highest count of videos meeting both benchmarks. It had 296,694 median views and 81 sampled videos across eight channels. Of 79 videos with measurable engagement, 20 met both benchmarks across three channels. AI-presented Fictional Legal Stories had 2.16% median engagement, with 14 of 256 measurable videos qualifying across four channels. Lawyer-led Entertainment had the highest median engagement (4.76%), with one of nine videos qualifying. Its sample covered two channels. The sole AI-presented Case Stories video met both thresholds by definition.

The sample favors historical high-view videos. One channel supplied 12 of the 20 qualifying News / Commentary videos. Excluding that channel leaves eight qualifying videos across two channels. At alternative cutoffs of 1M views and 2% engagement, 51 AI-presented Fictional Legal Stories videos and 24 News / Commentary videos meet both thresholds. Record cumulative views and engagement rate seven days after each pilot Short goes live and compare across pilots before scaling.

## Interpretation and sources

Public metrics do not expose audience retention, unique viewers, link clicks, qualified leads, or conversions. The analysis makes no claims about those outcomes. The commissioning organization, its specific business scope, and internal documents remain outside the public package. No pilot has been run.

- [YouTube video-resource fields](https://developers.google.com/youtube/data/reference/rest/v3/videos)
- [YouTube upload-playlist pagination](https://developers.google.com/youtube/data/reference/rest/v3/playlistItems/list)

The supplied snapshot supports reproducibility. Recheck current source availability and platform data-use requirements before redistributing, refreshing, or relying on a later snapshot.
