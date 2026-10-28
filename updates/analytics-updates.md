# Progress & Analytics updates (Role 5, Mingxi)

This file tracks changes to `analytics.html` that affect other pages, and anything I need from other roles. It isn't part of the website.

## 2026-10-28: aligned with the interface wireframes and the logging page

- **User-facing label:** SUSPENDED is shown to users as "Paused", as agreed on the interface and goals pages. Analytics keeps SUSPENDED internally, but chart labels and summaries now say "paused".
- **Reports across several activities (new Section 2.8, DD-59):** the Reports & Statistics page (FIG-11) can show all activities at once, so analytics now combines per-activity results. The combined daily average matches the wireframe example: 48 h 30 min over 30 days = 1 h 37 min.
- **New statistics:**
  - `sessionCount` for "Sessions Logged"
  - `metPeriods` / `countedPeriods` for "number and percentage of targets achieved"
- **"Adherence Rate":** this is the interface's name for the analytics completion rate.
- **Projection graph:** `Projection` now carries a daily cumulative series for the solid history line. The dashed line runs to the projected total.
- **Logging names:** analytics uses Adil's C-04 (Time Logging Service), C-05 (Time Entry Repository), and `TimeRecord.entryDate` / `durationMinutes`.
- **Formatting:** fixed indentation inside formula blocks and stray spaces such as "( FR-05)", both left by the HTML beautifier.

## 2026-10-23: aligned with the goals page and the new requirements

Commit `55cc19e`. Josh's goals page and Joseph's FR-19/FR-20 changes came in after my first version, so I updated analytics to match.

### What changed

- **Terminology:** "Paused" is now **Suspended** everywhere, matching FR-06 and goals.html. Status is read from Josh's `StatusPeriod` records (SUSPENDED / ARCHIVED with start and end dates).
- **Goal model:** the class diagram (FIG-51) now uses Josh's `Goal` (type, targetMinutes, startDate, endDate) and `StatusPeriod` instead of my old `GoalVersion`. The Goal Manager is referred to as **C-30**.
- **New requirements covered:**
  - **FR-19:** restoring an archived activity makes its days count again.
  - **FR-20:** past days and weeks keep the target that applied at the time.
- **FR-08:** deleting an activity removes its records, so all of its cached reports are removed too.
- **Goal edited today:** when a goal is edited, the new goal applies from that same day. This matches FIG-32 on the goals page.
- **Dashboard summary (new, Section 2.7):** analytics now provides the four dashboard numbers from interface.html:
  - time logged today
  - time logged this week
  - daily goals achieved ("X of Y")
  - weekly goals achieved ("X of Y")
- **Completion rate and streaks:** counted in the goal's own unit, days for daily goals and weeks for weekly goals.
- **Projection:** the 28-day average now ends yesterday, so an unfinished today doesn't lower it.
- **Time of day:** records can include a time of day (the interface log forms have one), but analytics groups records by date only.
- **NFR-07:** reports only include the requesting user's own activities.
- **Traceability:** the component table, traceability table, and each DD's related requirements now match. FR/NFR numbers link to `index.html`.

### Two new rules: Josh, please confirm

Both depend on how suspend and archive are defined on the goals page. See analytics.html Sections 2.2 to 2.5 and DD-57:

1. **Partly suspended weeks are prorated.** A weekly goal is scaled to the days that weren't suspended. For example, a 7 h goal with 2 suspended days becomes 5 h for that week. A week is only marked Suspended if every day in it was suspended.
2. **Archived days are left out of averages and projections**, the same as suspended days. No time can be logged while an activity is archived, so counting those days would lower the average after it's restored.

If you agree, could you add one line to goals.html Section 2.2 saying weekly targets are prorated for suspended days? If not, tell me and I'll change analytics.

## What analytics needs from other pages

| Who | Page | Request |
|---|---|---|
| Josh (Role 3) | goals.html | Confirm the two rules above. Already matching: Monday week start, goals kept with start and end dates, `StatusPeriod`, `GoalChanged` event. |
| Adil (Role 4) | logging.html | Provide a query for records by activity and date range, with duration in whole minutes. Publish a `RecordChanged` event (activity, record, old date, new date) after every create, edit, or delete. Please also pick the class name: analytics uses `TimeRecord` / `durationMinutes`, while goals FIG-30 shows `TimeLog` / `minutes`. I'll match whatever you choose. |

| Role 2 | architecture.html | Analytics components are **C-50 to C-56**, decisions are **DD-50 to DD-59**, and figures are **FIG-50 to FIG-53**. The traceability rows in analytics.html Section 7 can be merged into the full matrix. |

## ID ranges in use

| Page | Components | Decisions | Figures |
|---|---|---|---|
| index.html | none | none | FIG-01 to FIG-02 |
| interface.html | none | DD-60 to DD-63 | FIG-03 to FIG-11 |
| logging.html | C-04, C-05 | DD-04 to DD-06 | FIG-40 to FIG-41 |
| goals.html | C-30 | DD-30 to DD-34 | FIG-30 to FIG-34 |
| analytics.html | C-50 to C-56 | DD-50 to DD-59 | FIG-50 to FIG-53 |

## Diagrams

The analytics SVGs are generated by `tools/gen_analytics_svgs.py`. To change a diagram, edit the script and run `python tools/gen_analytics_svgs.py` from the repo root. Don't edit the SVGs by hand.
