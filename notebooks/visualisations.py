# ============================================
# Brentford FC Analytics - Step 3: Visualisations
# Professional-grade charts for portfolio
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np

# ============================================
# STYLE SETUP - Brentford brand colours
# ============================================
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Segoe UI", "Arial", "Helvetica"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor": "#FAFAFA",
    "axes.edgecolor": "#CCCCCC",
    "text.color": "#1A1A1A",
    "axes.labelcolor": "#1A1A1A",
    "xtick.color": "#4A4A4A",
    "ytick.color": "#4A4A4A",
})

RED = "#E30613"
DARK_RED = "#B8050F"
BLACK = "#1A1A1A"
GREY = "#7F8C8D"
LIGHT_GREY = "#BDC3C7"
GREEN = "#27AE60"
AMBER = "#F39C12"
LOSS_RED = "#C0392B"
BG = "#FAFAFA"

# Load cleaned data
matches = pd.read_csv("data/cleaned_matches.csv")
epl = pd.read_csv("data/cleaned_epl_comparison.csv")
transfers = pd.read_csv("data/cleaned_transfers.csv")
players = pd.read_csv("data/cleaned_players.csv")

# ============================================
# CHART 1: Points Per Season with context
# ============================================
season_pts = matches.groupby("Season").agg(
    W=("Result", lambda x: (x == "W").sum()),
    D=("Result", lambda x: (x == "D").sum()),
    L=("Result", lambda x: (x == "L").sum()),
    GF=("GF", "sum"),
    GA=("GA", "sum"),
).reset_index()
season_pts["Points"] = (season_pts["W"] * 3) + (season_pts["D"] * 1)
positions = {
    "2021-22": "13th", "2022-23": "9th", "2023-24": "16th", "2024-25": "10th"
}

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(season_pts["Season"], season_pts["Points"], color=RED, width=0.55,
              edgecolor="white", linewidth=1.5, zorder=3)

for bar, (_, row) in zip(bars, season_pts.iterrows()):
    height = bar.get_height()
    pos = positions.get(row["Season"], "")
    ax.text(bar.get_x() + bar.get_width()/2, height + 1.5,
            f'{int(height)} pts', ha="center", fontsize=15, fontweight="bold", color=BLACK)
    ax.text(bar.get_x() + bar.get_width()/2, height - 4,
            pos, ha="center", fontsize=11, fontweight="bold", color="white")

ax.set_title("Brentford's Premier League Journey", fontsize=18, fontweight="bold", pad=20, loc="left")
ax.set_ylabel("")
ax.set_xlabel("")
ax.set_ylim(0, 75)
ax.tick_params(axis="x", labelsize=13)
ax.tick_params(axis="y", left=False, labelleft=False)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.axhline(y=40, color=GREY, linestyle=":", alpha=0.5, label="Typical survival line (40 pts)")
ax.legend(fontsize=10, loc="upper right")
plt.tight_layout()
plt.savefig("visualisations/01_points_per_season.png", dpi=200, bbox_inches="tight")
plt.close()
print("Chart 1 saved: points_per_season.png")

# ============================================
# CHART 2: Win/Draw/Loss Stacked by Season
# ============================================
fig, ax = plt.subplots(figsize=(10, 6))
seasons = season_pts["Season"]
x = np.arange(len(seasons))
width = 0.55

ax.bar(x, season_pts["W"], width, label="Wins", color=GREEN, edgecolor="white", linewidth=1)
ax.bar(x, season_pts["D"], width, bottom=season_pts["W"], label="Draws", color=AMBER,
       edgecolor="white", linewidth=1)
ax.bar(x, season_pts["L"], width, bottom=season_pts["W"] + season_pts["D"], label="Losses",
       color=LOSS_RED, edgecolor="white", linewidth=1)

for i, (_, row) in enumerate(season_pts.iterrows()):
    ax.text(i, row["W"]/2, str(row["W"]), ha="center", va="center", fontsize=12,
            fontweight="bold", color="white")
    ax.text(i, row["W"] + row["D"]/2, str(row["D"]), ha="center", va="center", fontsize=12,
            fontweight="bold", color="white")
    ax.text(i, row["W"] + row["D"] + row["L"]/2, str(row["L"]), ha="center", va="center",
            fontsize=12, fontweight="bold", color="white")

ax.set_xticks(x)
ax.set_xticklabels(seasons, fontsize=13)
ax.set_title("Season-by-Season Record", fontsize=18, fontweight="bold", pad=20, loc="left")
ax.set_ylabel("Matches", fontsize=12)
ax.legend(fontsize=11, loc="upper right", framealpha=0.9)
ax.set_ylim(0, 42)
ax.tick_params(axis="y", left=False, labelleft=False)
plt.tight_layout()
plt.savefig("visualisations/02_win_draw_loss.png", dpi=200, bbox_inches="tight")
plt.close()
print("Chart 2 saved: win_draw_loss.png")

# ============================================
# CHART 3: Squad Cost vs League Position
# ============================================
fig, ax = plt.subplots(figsize=(12, 8))

for _, row in epl.iterrows():
    is_brentford = row["Team"] == "Brentford"
    color = RED if is_brentford else LIGHT_GREY
    size = 250 if is_brentford else 100
    edge = DARK_RED if is_brentford else GREY
    zorder = 10 if is_brentford else 5
    ax.scatter(row["Est_Squad_Cost_M"], row["Pos"], c=color, s=size,
               edgecolors=edge, linewidth=1.5, zorder=zorder)
    
    fontweight = "bold" if is_brentford else "normal"
    fontsize = 11 if is_brentford else 9
    color_text = RED if is_brentford else GREY
    offset = 30
    ax.annotate(row["Team"], (row["Est_Squad_Cost_M"] + offset, row["Pos"]),
                fontsize=fontsize, fontweight=fontweight, color=color_text, va="center")

ax.annotate("Brentford: 10th with a\n£180M squad — outperforming\nclubs worth 5x more",
            xy=(180, 10), xytext=(400, 14),
            fontsize=10, fontstyle="italic", color=DARK_RED,
            arrowprops=dict(arrowstyle="->", color=DARK_RED, lw=1.5),
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF0F0", edgecolor=DARK_RED, alpha=0.9))

ax.set_title("Squad Cost vs League Position — The Brentford Effect",
             fontsize=16, fontweight="bold", pad=20, loc="left")
ax.set_xlabel("Estimated Squad Cost (£M)", fontsize=12)
ax.set_ylabel("League Position", fontsize=12)
ax.invert_yaxis()
ax.set_yticks(range(1, 21))
ax.grid(axis="x", alpha=0.2, linestyle="--")
plt.tight_layout()
plt.savefig("visualisations/03_cost_vs_position.png", dpi=200, bbox_inches="tight")
plt.close()
print(" Chart 3 saved: cost_vs_position.png")

# ============================================
# CHART 4: Moneyball Transfers
# ============================================
transfer_scorers = transfers[transfers["PL_Goals"] > 0].copy()

fig, ax = plt.subplots(figsize=(12, 7))

scatter = ax.scatter(transfer_scorers["Transfer_Fee_M"], transfer_scorers["PL_Goals"],
                     s=transfer_scorers["PL_Apps"] * 4, alpha=0.75, color=RED,
                     edgecolors=DARK_RED, linewidth=1, zorder=5)

for _, row in transfer_scorers.iterrows():
    y_offset = 1 if row["PL_Goals"] > 5 else 0.8
    ax.annotate(row["Player_Name"],
                (row["Transfer_Fee_M"], row["PL_Goals"] + y_offset),
                fontsize=9, ha="center", color=BLACK)

ax.axvspan(-1, 7, alpha=0.08, color=GREEN, zorder=1)
ax.text(3, 37, "BARGAIN\nZONE", fontsize=11, ha="center", color=GREEN,
        fontweight="bold", alpha=0.6)

ax.set_title("The Moneyball Effect — Transfer Fee vs Goals Scored",
             fontsize=16, fontweight="bold", pad=20, loc="left")
ax.set_xlabel("Transfer Fee (£M)", fontsize=12)
ax.set_ylabel("Premier League Goals", fontsize=12)
ax.set_xlim(-1, 35)
ax.text(0.98, 0.02, "Bubble size = appearances", transform=ax.transAxes,
        fontsize=9, ha="right", color=GREY, fontstyle="italic")
ax.grid(alpha=0.2, linestyle="--")
plt.tight_layout()
plt.savefig("visualisations/04_moneyball_transfers.png", dpi=200, bbox_inches="tight")
plt.close()
print("Chart 4 saved: moneyball_transfers.png")

# ============================================
# CHART 5: Home vs Away — Donut Charts
# ============================================
home = matches[matches["Venue"] == "Home"]
away = matches[matches["Venue"] == "Away"]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
colors = [GREEN, AMBER, LOSS_RED]

for ax, data, title in [(axes[0], home, "Home"), (axes[1], away, "Away")]:
    results = data["Result"].value_counts().reindex(["W", "D", "L"], fill_value=0)
    wedges, texts, autotexts = ax.pie(results, labels=["Win", "Draw", "Loss"],
                                       autopct="%1.0f%%", colors=colors,
                                       textprops={"fontsize": 12},
                                       pctdistance=0.75, startangle=90,
                                       wedgeprops={"edgecolor": "white", "linewidth": 2})
    for autotext in autotexts:
        autotext.set_fontweight("bold")
        autotext.set_color("white")
    centre = plt.Circle((0, 0), 0.5, fc=BG)
    ax.add_artist(centre)
    total = len(data)
    ax.text(0, 0, f"{title}\n{total} games", ha="center", va="center",
            fontsize=13, fontweight="bold", color=BLACK)

fig.suptitle("Brentford FC — Home vs Away Record (All PL Seasons)",
             fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("visualisations/05_home_vs_away.png", dpi=200, bbox_inches="tight")
plt.close()
print("Chart 5 saved: home_vs_away.png")

# ============================================
# CHART 6: Top Scorers — Horizontal Lollipop
# ============================================
scorers = players[players["goals"] > 0].sort_values("goals", ascending=True).copy()

fig, ax = plt.subplots(figsize=(10, 7))
y_pos = range(len(scorers))

ax.hlines(y=y_pos, xmin=0, xmax=scorers["goals"], color=LIGHT_GREY, linewidth=2, zorder=1)
ax.scatter(scorers["goals"], y_pos, color=RED, s=120, zorder=5, edgecolors=DARK_RED, linewidth=1)

for i, (_, row) in enumerate(scorers.iterrows()):
    ax.text(row["goals"] + 0.3, i, str(int(row["goals"])), va="center",
            fontsize=12, fontweight="bold", color=BLACK)

ax.set_yticks(y_pos)
ax.set_yticklabels(scorers["player"], fontsize=11)
ax.set_title("Top Scorers 2024-25", fontsize=18, fontweight="bold", pad=20, loc="left")
ax.set_xlabel("Goals", fontsize=12)
ax.set_xlim(0, max(scorers["goals"]) + 3)
ax.grid(axis="x", alpha=0.2, linestyle="--")
plt.tight_layout()
plt.savefig("visualisations/06_top_scorers.png", dpi=200, bbox_inches="tight")
plt.close()
print("Chart 6 saved: top_scorers.png")

# ============================================
# CHART 7: xG vs Actual Goals Rolling Average
# ============================================
matches_xg = matches.dropna(subset=["xG"]).copy().reset_index(drop=True)

fig, ax = plt.subplots(figsize=(14, 6))

ax.fill_between(matches_xg.index,
                matches_xg["GF"].rolling(10).mean(),
                matches_xg["xG"].rolling(10).mean(),
                alpha=0.15, color=RED)
ax.plot(matches_xg.index, matches_xg["GF"].rolling(10).mean(),
        color=RED, linewidth=2.5, label="Actual Goals (10-game avg)", zorder=5)
ax.plot(matches_xg.index, matches_xg["xG"].rolling(10).mean(),
        color=GREY, linewidth=2, linestyle="--", label="Expected Goals (10-game avg)", zorder=4)

season_starts = [0]
for i in range(1, len(matches_xg)):
    if matches_xg.loc[i, "Season"] != matches_xg.loc[i-1, "Season"]:
        season_starts.append(i)

for start in season_starts[1:]:
    ax.axvline(x=start, color=LIGHT_GREY, linestyle=":", alpha=0.6)

for start, season in zip(season_starts, matches_xg.loc[season_starts, "Season"]):
    ax.text(start + 2, ax.get_ylim()[1] - 0.1, season, fontsize=9, color=GREY, fontstyle="italic")

ax.set_title("Actual Goals vs Expected Goals — Are Brentford Clinical or Lucky?",
             fontsize=15, fontweight="bold", pad=20, loc="left")
ax.set_xlabel("Match Number", fontsize=12)
ax.set_ylabel("Goals per Match (10-game rolling avg)", fontsize=11)
ax.legend(fontsize=11, loc="upper right", framealpha=0.9)
ax.grid(alpha=0.2, linestyle="--")
plt.tight_layout()
plt.savefig("visualisations/07_xg_vs_actual.png", dpi=200, bbox_inches="tight")
plt.close()
print("Chart 7 saved: xg_vs_actual.png")

print("\n All 7 visualisations saved to visualisations/ folder!")
