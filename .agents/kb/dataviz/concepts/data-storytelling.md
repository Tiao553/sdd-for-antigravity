# Data Storytelling

## The SCR Framework

Every data story follows three beats:

1. **Situation** — Establish shared context. What is happening? What is the normal state?
2. **Complication** — Introduce the tension. What changed, what is at risk, what is unexpected?
3. **Resolution** — What should the audience do or conclude?

```
Situation:  "Our monthly active users have been growing steadily at 8% MoM for six months."
Complication: "In March, growth dropped to 2% — the lowest in a year."
Resolution: "Retention in the 30-60 day cohort fell sharply. We recommend investigating onboarding changes made in February."
```

## The "So What" Principle

Every chart title and annotation must answer "so what for the audience."

| Descriptive title (weak) | Conclusion title (strong) |
|--------------------------|--------------------------|
| Monthly Revenue | Revenue grew 23% in Q4 — fastest quarter since 2021 |
| Regional Sales Breakdown | Southeast underperforms by 18% vs. target |
| Customer Churn Rate | Churn is accelerating: up 3 points in 60 days |

## Annotation Strategies

- **Callout** — Arrow + text pointing to the peak, trough, or threshold that matters
- **Reference line** — Target line, budget line, or historical average for context
- **Band annotation** — Shade a time period (product launch, outage, campaign)
- **Trend label** — Endpoint label showing the direction ("↑ 14% vs last year")

Write annotations as complete sentences addressed to the reader: "Sales spike coincides with Black Friday promotion."

## Progressive Disclosure

Design for three reading speeds:
1. **3 seconds** — Headline KPIs and chart titles answer the key question
2. **30 seconds** — Chart body and annotations support the headline
3. **3 minutes** — Detail table, footnotes, and methodology explain the data

Executives read at 3 seconds. Analysts read at 3 minutes. Design the 3-second layer first.

## Choosing the Right Story Structure

| Audience intent | Structure |
|----------------|-----------|
| Decision needed now | Lead with resolution, then evidence |
| Discovery / exploration | Lead with situation, build to complication |
| Reporting / update | Situation → performance → outlook |
| Persuasion | Complication first (create urgency), then resolution |

## Anti-Patterns

- **Data dump** — presenting every metric without a guiding question
- **Orphan chart** — a visualization with no title, label, or context
- **False precision** — "revenue increased 14.73%" when "~15%" suffices
- **Cherry-picking timeframe** — choose the start date that tells the honest story
- **Correlation as causation** — annotate confounding factors explicitly
