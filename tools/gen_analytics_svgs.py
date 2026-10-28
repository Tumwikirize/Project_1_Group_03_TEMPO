"""Generate the Role 5 (analytics) diagrams FIG-50 to FIG-53 as SVG, matching the style of the use-case diagrams.

Usage (from the repository root):
    python tools/gen_analytics_svgs.py

Writes analytics-dataflow.svg, analytics-class.svg, analytics-seq-report.svg, and
analytics-seq-recalc.svg into images/. Pass a different output folder as the first argument if needed.
"""
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "images"
FONT = 'font-family="Arial, sans-serif"'
INK = "#24364e"
NAVY = "#183454"
BLUE = "#2c5d95"
FILL = "#f3f7fc"
LINE = "#4f6079"
MUTED = "#65778f"


def esc(s):
    return escape(s)


class Svg:
    def __init__(self, w, h, title, desc):
        self.w, self.h = w, h
        self.parts = [
            "<?xml version='1.0' encoding='utf-8'?>",
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
            f'  <title id="title">{esc(title)}</title>',
            f'  <desc id="desc">{esc(desc)}</desc>',
            "  <defs>",
            f'    <marker id="filled" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}" /></marker>',
            f'    <marker id="open" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,0.5 L10,5 L0,9.5" fill="none" stroke="{LINE}" stroke-width="1.4" /></marker>',
            "  </defs>",
            f'  <rect width="{w}" height="{h}" fill="#ffffff" />',
        ]

    def add(self, s):
        self.parts.append("  " + s)

    def text(self, x, y, s, size=14, weight="400", anchor="middle", fill=INK, italic=False, halo=False):
        extra = ' font-style="italic"' if italic else ""
        if halo:
            extra += ' stroke="#ffffff" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'
        self.add(f'<text x="{x}" y="{y}" text-anchor="{anchor}" {FONT} font-size="{size}" font-weight="{weight}" fill="{fill}"{extra}>{esc(s)}</text>')

    def line(self, pts, dashed=False, head="filled", width=1.8, color=LINE):
        d = " ".join(f"{x},{y}" for x, y in pts)
        dash = ' stroke-dasharray="7 5"' if dashed else ""
        mk = f' marker-end="url(#{head})"' if head else ""
        self.add(f'<polyline points="{d}" fill="none" stroke="{color}" stroke-width="{width}"{dash}{mk} />')

    def rect(self, x, y, w, h, fill="#ffffff", stroke=NAVY, rx=0, dashed=False, width=2):
        dash = ' stroke-dasharray="8 5"' if dashed else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"{dash} />')

    def save(self, name):
        self.parts.append("</svg>")
        (OUT / name).write_text("\n".join(self.parts) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- FIG-50: data flow
def fig50():
    s = Svg(1100, 610, "FIG-50 Analytics data flow",
            "Data flow through the analytics components. The user interface sends a report request to the Analytics "
            "Service (C-50). C-50 receives time records from the Time Entry Repository (C-05) and goals and status periods from "
            "the Goal Manager (C-30). It passes the records and range to the Period Calculator (C-51), which produces daily totals for "
            "the Progress (C-52), Statistics (C-53), and Projection (C-54) calculators. C-50 passes goals and status periods to C-52, "
            "and C-52 passes period statuses to C-53. The three calculators send their results to the Chart and Summary "
            "Builder (C-55), which returns the report data to C-50. C-50 stores reports in and reads them from the report "
            "cache (D3) and returns the report to the user interface. The Change Listener (C-56) receives record and goal "
            "change events and tells C-50 which activity is affected; C-50 then invalidates the cache and sends a refresh "
            "notice to the user interface.")

    def process(x, y, w, h, cid, lines):
        s.rect(x, y, w, h, fill=FILL, stroke=BLUE, rx=12, width=2.2)
        cy = y + h / 2 - (len(lines)) * 9 + 4
        s.text(x + w / 2, cy, cid, size=14, weight="700", fill=BLUE)
        for i, ln in enumerate(lines):
            s.text(x + w / 2, cy + 19 * (i + 1), ln, size=15, weight="600")

    def entity(x, y, w, h, name, caption):
        s.rect(x, y, w, h, stroke=NAVY, width=2.2)
        s.text(x + w / 2, y + h / 2 - 2, name, size=15, weight="600")
        s.text(x + w / 2, y + h / 2 + 16, caption, size=12, fill=MUTED)

    def store(x, y, w, h, sid, label, caption):
        s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fbfcfe" stroke="none" />')
        s.line([(x + w, y), (x, y), (x, y + h), (x + w, y + h)], head=None, color=NAVY, width=2)
        s.line([(x + 46, y), (x + 46, y + h)], head=None, color=NAVY, width=1.5)
        s.text(x + 23, y + h / 2 + 5, sid, size=14, weight="700", fill=NAVY)
        s.text(x + 56, y + h / 2 - 3, label, size=15, weight="600", anchor="start")
        s.text(x + 56, y + h / 2 + 15, caption, size=12, anchor="start", fill=MUTED)

    # external entities
    entity(30, 270, 150, 70, "User Interface", "(reports, dashboard)")
    entity(170, 30, 175, 60, "Time Logging", "(C-04, C-05, logging page)")
    entity(360, 30, 175, 60, "Goal Manager", "(C-30, goals page)")

    # analytics processes and store
    process(30, 140, 150, 64, "C-56", ["Change Listener"])
    process(250, 270, 190, 70, "C-50", ["Analytics Service"])
    process(510, 270, 180, 70, "C-51", ["Period Calculator"])
    process(770, 150, 210, 62, "C-52", ["Progress Calculator"])
    process(770, 270, 210, 62, "C-53", ["Statistics Calculator"])
    process(770, 390, 210, 62, "C-54", ["Projection Engine"])
    process(500, 485, 200, 76, "C-55", ["Chart & Summary", "Builder"])
    store(250, 470, 190, 52, "D3", "Report cache", "(owned by C-50)")

    # change events into C-56
    s.line([(170, 62), (140, 62), (140, 138)])
    s.text(146, 110, "record", size=12, anchor="start", halo=True)
    s.text(146, 124, "events", size=12, anchor="start", halo=True)
    s.line([(447, 30), (447, 14), (80, 14), (80, 138)])
    s.text(262, 18, "goal events", size=12, halo=True)
    s.line([(165, 204), (262, 268)])
    s.text(196, 252, "affected", size=12, anchor="end", halo=True)
    s.text(196, 266, "activity", size=12, anchor="end", halo=True)

    # data into C-50
    s.line([(280, 90), (280, 268)])
    s.text(286, 180, "time records", size=12, anchor="start", halo=True)
    s.line([(380, 90), (380, 268)])
    s.text(386, 122, "goals,", size=12, anchor="start", halo=True)
    s.text(386, 136, "status periods", size=12, anchor="start", halo=True)

    # UI <-> C-50
    s.line([(180, 292), (248, 292)])
    s.text(214, 284, "request", size=12, halo=True)
    s.line([(250, 320), (182, 320)])
    s.text(214, 336, "report,", size=12, halo=True)
    s.text(214, 350, "refresh notice", size=12, halo=True)

    # C-50 -> C-51, C-52
    s.line([(440, 305), (508, 305)])
    s.text(474, 297, "records,", size=12, halo=True)
    s.text(474, 326, "range", size=12, halo=True)
    s.line([(420, 270), (420, 172), (768, 172)])
    s.text(600, 164, "goals, status periods", size=12, halo=True)

    # C-51 -> calculators
    s.line([(690, 286), (768, 196)])
    s.line([(690, 301), (768, 301)])
    s.line([(690, 320), (768, 414)])
    s.text(729, 250, "daily totals", size=12, halo=True)

    # C-52 -> C-53
    s.line([(875, 212), (875, 268)])
    s.text(881, 244, "period statuses", size=12, anchor="start", halo=True)

    # results bus to C-55
    for y in (181, 301, 421):
        s.line([(980, y), (1015, y)], head=None)
    s.line([(1015, 181), (1015, 523), (702, 523)])
    s.text(1023, 330, "progress,", size=12, anchor="start", halo=True)
    s.text(1023, 345, "statistics,", size=12, anchor="start", halo=True)
    s.text(1023, 360, "projection", size=12, anchor="start", halo=True)

    # C-55 -> C-50
    s.line([(512, 485), (432, 342)])
    s.text(484, 392, "report data,", size=12, anchor="start", halo=True)
    s.text(484, 406, "chart, summary", size=12, anchor="start", halo=True)

    # C-50 <-> D3
    s.line([(290, 340), (290, 468)])
    s.text(284, 410, "store /", size=12, anchor="end", halo=True)
    s.text(284, 424, "invalidate", size=12, anchor="end", halo=True)
    s.line([(400, 470), (400, 342)])
    s.text(406, 440, "cached", size=12, anchor="start", halo=True)
    s.text(406, 454, "report", size=12, anchor="start", halo=True)

    # legend
    s.rect(30, 580, 18, 14, fill=FILL, stroke=BLUE, rx=4, width=1.5)
    s.text(54, 592, "Process (analytics component)", size=12, anchor="start", fill=MUTED)
    s.line([(270, 580), (250, 580), (250, 594), (270, 594)], head=None, color=NAVY, width=1.5)
    s.text(276, 592, "Data store", size=12, anchor="start", fill=MUTED)
    s.rect(370, 580, 18, 14, stroke=NAVY, width=1.5)
    s.text(394, 592, "External entity (outside analytics)", size=12, anchor="start", fill=MUTED)
    s.save("analytics-dataflow.svg")


# ---------------------------------------------------------------- FIG-51: class diagram
def class_box(s, x, y, w, name, attrs, ops=(), stereo=None, external=False):
    head = 46 if stereo else 30
    h = head + len(attrs) * 18 + 12 + ((len(ops) * 18 + 12) if ops else 0)
    s.rect(x, y, w, h, fill="#ffffff" if external else FILL, stroke=NAVY if not external else MUTED,
           dashed=external, width=2)
    ty = y + 20
    if stereo:
        s.text(x + w / 2, ty, f"«{stereo}»", size=12, fill=MUTED)
        ty += 17
    s.text(x + w / 2, ty, name, size=15, weight="700", fill=NAVY)
    s.line([(x, y + head), (x + w, y + head)], head=None, color=NAVY if not external else MUTED, width=1.5)
    for i, a in enumerate(attrs):
        s.text(x + 10, y + head + 18 * (i + 1), a, size=13, anchor="start")
    if ops:
        oy = y + head + len(attrs) * 18 + 12
        s.line([(x, oy), (x + w, oy)], head=None, color=NAVY, width=1.5)
        for i, o in enumerate(ops):
            s.text(x + 10, oy + 18 * (i + 1), o, size=13, anchor="start")
    return (x, y, w, h)


def composition(s, start, end):
    """Line with a filled diamond at `start` (the whole)."""
    (x1, y1), (x2, y2) = start, end
    ang = math.atan2(y2 - y1, x2 - x1)
    L, W = 16, 7
    tip = (x1, y1)
    mid = (x1 + L / 2 * math.cos(ang), y1 + L / 2 * math.sin(ang))
    back = (x1 + L * math.cos(ang), y1 + L * math.sin(ang))
    left = (mid[0] - W * math.sin(ang), mid[1] + W * math.cos(ang))
    right = (mid[0] + W * math.sin(ang), mid[1] - W * math.cos(ang))
    s.line([back, end], head=None)
    pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in (tip, left, back, right))
    s.add(f'<polygon points="{pts}" fill="{NAVY}" stroke="{NAVY}" stroke-width="1" />')


def fig51():
    s = Svg(1290, 800, "FIG-51 Analytics report data model",
            "UML class diagram of the report objects produced by the analytics components. A ReportRequest for one or more activities produces a "
            "ProgressReport. A ProgressReport is composed of one or more PeriodSummary objects, one Statistics object, "
            "an optional Projection, and one ChartSeries. Each PeriodSummary covers one ReportingPeriod and has a "
            "PeriodStatus. Time records from the logging design are grouped into reporting periods. The Goal and "
            "StatusPeriod classes from the goals design (C-30) supply the target in effect and any suspended or "
            "archived days for each period. A separate DashboardSummary holds the cross-activity totals and goal "
            "counts shown on the dashboard.")

    rr = class_box(s, 30, 40, 250, "ReportRequest",
                   ["activityIds: ID [1..*]", "periodType: DAY | WEEK", "rangeStart: Date", "rangeEnd: Date",
                    "projectionDate: Date [0..1]"])
    pr = class_box(s, 370, 40, 320, "ProgressReport",
                   ["activityName: String", "unit: String = \"minutes\"", "rangeStart: Date", "rangeEnd: Date",
                    "goalLabel: String [0..1]", "textSummary: String", "generatedAt: DateTime"])
    cs = class_box(s, 800, 40, 270, "ChartSeries",
                   ["labels: String [*]", "valuesMinutes: Integer [*]", "goalLineMinutes: Integer [0..1]",
                    "statuses: PeriodStatus [*]"])
    rp = class_box(s, 30, 330, 250, "ReportingPeriod",
                   ["type: DAY | WEEK", "start: Date", "end: Date"], ops=["contains(date: Date): Boolean"])
    ps = class_box(s, 370, 330, 300, "PeriodSummary",
                   ["totalMinutes: Integer", "targetMinutes: Integer [0..1]", "percentOfGoal: Integer [0..1]",
                    "remainingMinutes: Integer", "status: PeriodStatus [0..1]"])
    st = class_box(s, 740, 330, 260, "Statistics",
                   ["totalMinutes: Integer", "daysInRange: Integer", "activeDays: Integer",
                    "avgDailyMinutes: Decimal", "avgActiveDayMinutes: Decimal", "sessionCount: Integer",
                    "bestPeriodMinutes: Integer", "metPeriods: Integer", "countedPeriods: Integer",
                    "completionRate: Decimal [0..1]", "currentStreak: Integer", "longestStreak: Integer"])
    pj = class_box(s, 1030, 330, 210, "Projection",
                   ["targetDate: Date", "baselineMinutes: Integer", "windowDays: Integer", "windowAvg: Decimal",
                    "projectedMinutes: Integer", "sufficientData: Boolean",
                    "cumulativeMinutes: Integer [*]"])
    en = class_box(s, 370, 570, 220, "PeriodStatus", ["MET", "IN_PROGRESS", "MISSED", "SUSPENDED", "NO_GOAL"],
                   stereo="enumeration")
    tr = class_box(s, 30, 590, 250, "TimeRecord", ["activityId: ID", "entryDate: Date", "durationMinutes: Integer"],
                   stereo="Time Logging, C-05", external=True)
    class_box(s, 740, 620, 240, "Goal",
              ["type: DAILY | WEEKLY", "targetMinutes: Integer", "startDate: Date", "endDate: Date [0..1]"],
              stereo="Activities & Goals, C-30", external=True)
    class_box(s, 1010, 620, 230, "StatusPeriod",
              ["type: SUSPENDED | ARCHIVED", "startDate: Date", "endDate: Date [0..1]"],
              stereo="Activities & Goals, C-30", external=True)

    # ReportRequest produces ProgressReport
    s.line([(280, 100), (368, 100)], dashed=True, head="open")
    s.text(324, 92, "«produces»", size=12, fill=MUTED, halo=True)
    # compositions
    composition(s, (470, 40 + pr[3]), (470, 330))
    s.text(478, 228, "1", size=13, anchor="start")
    s.text(478, 322, "history 1..*", size=13, anchor="start")
    composition(s, (620, 40 + pr[3]), (820, 330))
    s.text(828, 322, "1", size=13, anchor="start")
    composition(s, (690, 180), (1110, 330))
    s.text(1116, 322, "0..1", size=13, anchor="start")
    composition(s, (690, 90), (800, 90))
    s.text(794, 82, "1", size=13, anchor="end")
    # PeriodSummary -> ReportingPeriod
    s.line([(370, 390), (282, 390)], head="open")
    s.text(290, 382, "period 1", size=13, anchor="start", halo=True)
    # PeriodSummary ..> PeriodStatus
    s.line([(480, 462), (480, 568)], dashed=True, head="open")
    # TimeRecord grouped into ReportingPeriod
    s.line([(155, 590), (155, 458)], dashed=True, head="open")
    s.text(163, 530, "«grouped by date»", size=12, anchor="start", fill=MUTED, halo=True)
    # PeriodSummary uses Goal and StatusPeriod
    s.line([(640, 462), (738, 670)], dashed=True, head="open")
    s.text(652, 540, "«target from»", size=12, anchor="end", fill=MUTED, halo=True)
    s.line([(670, 450), (715, 450), (715, 604), (1125, 604), (1125, 618)], dashed=True, head="open")
    s.text(1062, 598, "«status from»", size=12, fill=MUTED, halo=True)
    # cross-activity dashboard summary (standalone result of getDashboardSummary)
    class_box(s, 1090, 40, 185, "DashboardSummary",
              ["date: Date", "minutesToday: Integer", "minutesThisWeek: Integer", "dailyGoalsMet: Integer",
               "dailyGoals: Integer", "weeklyGoalsMet: Integer", "weeklyGoals: Integer"])
    s.save("analytics-class.svg")


# ---------------------------------------------------------------- sequence diagrams
class Seq:
    def __init__(self, s, lifelines, top=30, actor_first=True):
        self.s = s
        self.ll = lifelines  # list of (key, x, [lines])
        self.x = {k: x for k, x, _ in lifelines}
        self.top = top
        self.actor_first = actor_first

    def heads(self, bottom):
        s = self.s
        for i, (k, x, lines) in enumerate(self.ll):
            if i == 0 and self.actor_first:
                cy = self.top + 8
                s.add(f'<circle cx="{x}" cy="{cy}" r="8" fill="none" stroke="{NAVY}" stroke-width="2" />')
                s.line([(x, cy + 8), (x, cy + 26)], head=None, color=NAVY, width=2)
                s.line([(x - 12, cy + 15), (x + 12, cy + 15)], head=None, color=NAVY, width=2)
                s.line([(x - 10, cy + 38), (x, cy + 26), (x + 10, cy + 38)], head=None, color=NAVY, width=2)
                s.text(x, cy + 56, lines[0], size=13, weight="600")
                start = cy + 62
            else:
                w = 124
                s.rect(x - w / 2, self.top, w, 50, fill=FILL, stroke=BLUE, width=2)
                for j, ln in enumerate(lines):
                    y = self.top + (19 if len(lines) == 2 else 30) + j * 17
                    s.text(x, y, ln, size=13, weight="700" if j == 0 and ln.startswith(("C-", "D3")) else "600",
                           fill=BLUE if j == 0 and ln.startswith(("C-", "D3")) else INK)
                start = self.top + 50
            s.add(f'<line x1="{x}" y1="{start}" x2="{x}" y2="{bottom}" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="6 5" />')

    def bar(self, key, y1, y2):
        x = self.x[key]
        self.s.rect(x - 6, y1, 12, y2 - y1, fill="#dfe8f5", stroke=BLUE, width=1.4)

    def msg(self, a, b, y, label, kind="sync"):
        s = self.s
        xa, xb = self.x[a], self.x[b]
        off = 6
        if xb > xa:
            xa, xb2 = xa + off, xb - off
        else:
            xa, xb2 = xa - off, xb + off
        if kind == "sync":
            s.line([(xa, y), (xb2, y)], head="filled")
        elif kind == "async":
            s.line([(xa, y), (xb2, y)], head="open")
        else:
            s.line([(xa, y), (xb2, y)], head="open", dashed=True)
        s.text((xa + xb2) / 2, y - 6, label, size=13, halo=True)

    def self_msg(self, a, y, label):
        x = self.x[a] + 6
        self.s.line([(x, y), (x + 34, y), (x + 34, y + 18), (x + 2, y + 18)])
        self.s.text(x + 42, y + 13, label, size=13, anchor="start", halo=True)

    def frame(self, x1, y1, x2, y2, tag, guard=None):
        s = self.s
        s.rect(x1, y1, x2 - x1, y2 - y1, fill="none", stroke=NAVY, width=1.5)
        w = 12 + 8 * len(tag)
        s.add(f'<polygon points="{x1},{y1} {x1 + w},{y1} {x1 + w},{y1 + 14} {x1 + w - 8},{y1 + 22} {x1},{y1 + 22}" fill="#ffffff" stroke="{NAVY}" stroke-width="1.5" />')
        s.text(x1 + 6, y1 + 16, tag, size=13, weight="700", anchor="start", fill=NAVY)
        if guard:
            s.text(x1 + w + 8, y1 + 16, guard, size=13, anchor="start", fill=NAVY, italic=True)

    def divider(self, x1, x2, y, guard):
        self.s.add(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="8 5" />')
        self.s.text(x1 + 8, y + 16, guard, size=13, anchor="start", fill=NAVY, italic=True)


def fig52():
    s = Svg(1240, 850, "FIG-52 Generate a progress report",
            "UML sequence diagram. The user opens a report. The user interface calls getReport on the Analytics "
            "Service (C-50), which checks the report cache. On a cache hit the cached report is returned. Otherwise C-50 "
            "asks the Period Calculator (C-51) for reporting periods, retrieves time records from the Time Entry Repository (C-05) "
            "and goals and status periods from the Goal Manager, has C-51 group records into daily totals, asks the calculators "
            "(C-52 to C-54) for period summaries, statistics, and the projection, asks the Chart and Summary Builder "
            "(C-55) for chart series and a written summary, stores the report in the cache, and returns it to the user "
            "interface, which displays it.")
    xs = [70, 205, 345, 485, 620, 760, 895, 1030, 1165]
    q = Seq(s, [
        ("user", xs[0], ["User"]),
        ("ui", xs[1], ["User", "Interface"]),
        ("c50", xs[2], ["C-50", "Analytics Service"]),
        ("cache", xs[3], ["D3", "Report Cache"]),
        ("c51", xs[4], ["C-51", "Period Calculator"]),
        ("tr", xs[5], ["C-05", "Entry Repository"]),
        ("gm", xs[6], ["C-30", "Goal Manager"]),
        ("calc", xs[7], ["C-52 to C-54", "Calculators"]),
        ("c55", xs[8], ["C-55", "Chart & Summary"]),
    ])
    q.heads(830)
    y = 125
    step = 34
    q.bar("ui", y - 4, 770)
    q.bar("c50", y + step - 4, 735)
    q.msg("user", "ui", y, "open report view")
    y += step
    q.msg("ui", "c50", y, "getReport(req)")
    y += step
    q.msg("c50", "cache", y, "lookup(key)")
    y += 18
    alt_top = y
    y += 46
    q.msg("cache", "c50", y, "cached report", "return")
    y += 20
    div = y
    y += 40
    q.msg("c50", "c51", y, "resolvePeriods(req)")
    y += step
    q.msg("c51", "c50", y, "periods", "return")
    y += step
    q.msg("c50", "tr", y, "findRecords(activity, start, end)")
    y += step
    q.msg("tr", "c50", y, "time records", "return")
    y += step
    q.msg("c50", "gm", y, "getGoalHistory(activity)")
    y += step
    q.msg("gm", "c50", y, "goals, status periods", "return")
    y += step
    q.msg("c50", "c51", y, "bucket(records, periods)")
    y += step
    q.msg("c51", "c50", y, "daily totals", "return")
    y += step
    q.msg("c50", "calc", y, "compute(totals, goals, req)")
    y += step
    q.msg("calc", "c50", y, "summaries, statistics, projection", "return")
    y += step
    q.msg("c50", "c55", y, "build(reportData)")
    y += step
    q.msg("c55", "c50", y, "chart series, text summary", "return")
    y += step
    q.msg("c50", "cache", y, "store(key, report)")
    y += 18
    q.frame(285, alt_top, 1228, y, "alt", "[cache hit]")
    q.divider(285, 1228, div, "[cache miss]")
    y += 34
    q.msg("c50", "ui", y, "ProgressReport", "return")
    y += step
    q.msg("ui", "user", y, "chart, totals, summary", "return")
    s.save("analytics-seq-report.svg")


def fig53():
    s = Svg(1060, 640, "FIG-53 Recalculate after a time record changes",
            "UML sequence diagram. The user edits a time record. The user interface calls updateRecord on the Time "
            "Logging Service, which validates and saves the change and publishes a RecordChanged event to the Change "
            "Listener (C-56), then confirms the save. C-56 identifies the affected activity and calls invalidate on "
            "the Analytics Service (C-50), which removes every cached report for that activity from the report cache and notifies the user interface that reports changed. If a report view is open, the user "
            "interface requests the report again, which is generated as in FIG-52, and displays the updated totals "
            "and chart.")
    xs = [70, 240, 420, 600, 780, 960]
    q = Seq(s, [
        ("user", xs[0], ["User"]),
        ("ui", xs[1], ["User", "Interface"]),
        ("tl", xs[2], ["C-04", "Time Logging"]),
        ("c56", xs[3], ["C-56", "Change Listener"]),
        ("c50", xs[4], ["C-50", "Analytics Service"]),
        ("cache", xs[5], ["D3", "Report Cache"]),
    ])
    q.heads(625)
    y = 125
    step = 36
    q.bar("tl", y + step - 4, y + step * 4 + 6)
    q.msg("user", "ui", y, "edit date / duration")
    y += step
    q.msg("ui", "tl", y, "updateRecord(id, changes)")
    y += step - 8
    q.self_msg("tl", y, "validate and save")
    y += step + 16
    q.msg("tl", "c56", y, "RecordChanged(event)", "async")
    y += step
    q.msg("tl", "ui", y, "save confirmed", "return")
    y += step - 8
    q.bar("c56", y - 6, y + 2 * step + 4)
    q.self_msg("c56", y, "identify affected activity")
    y += step + 6
    q.msg("c56", "c50", y, "invalidate(activity)")
    y += step
    q.bar("c50", y - 6, y + step + 6)
    q.msg("c50", "cache", y, "removeAll(activity)")
    y += step
    q.msg("c50", "ui", y, "reportsChanged(activity)", "async")
    y += 22
    opt_top = y
    y += 40
    q.msg("ui", "c50", y, "getReport(req)")
    y += 14
    s.rect(xs[4] - 40, y, xs[5] - xs[4] + 80, 36, fill="#ffffff", stroke=NAVY, width=1.5)
    s.add(f'<polygon points="{xs[4] - 40},{y} {xs[4]},{y} {xs[4]},{y + 12} {xs[4] - 6},{y + 18} {xs[4] - 40},{y + 18}" fill="#ffffff" stroke="{NAVY}" stroke-width="1.5" />')
    s.text(xs[4] - 34, y + 14, "ref", size=12, weight="700", anchor="start", fill=NAVY)
    s.text((xs[4] + xs[5]) / 2 + 10, y + 24, "Generate report (FIG-52)", size=13, weight="600")
    y += 36 + 26
    q.msg("c50", "ui", y, "updated ProgressReport", "return")
    y += step - 6
    q.msg("ui", "user", y, "updated totals and chart", "return")
    y += 16
    q.frame(30, opt_top, 1045, y, "opt", "[a report view is open]")
    s.save("analytics-seq-recalc.svg")


fig50()
fig51()
fig52()
fig53()
print("ok")
