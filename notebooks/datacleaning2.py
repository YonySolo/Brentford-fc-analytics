import pandas as pd
import numpy as np

# ============================================
# DATASET 1: MATCHES
# ============================================

print("Cleaning match dataset....")
matches = pd.read_csv("data/raw_brentford_matches.csv")
print(f"  Raw shape: {matches.shape}")

# 1. remove duplicated rows
matches = matches.drop_duplicates()
print(f"  After removing duplicates:")

#2. Standardise venue (home/away)
matches["Venue"] = matches["Venue"].str.strip().str.lower()
matches["Venue"] = matches["Venue"].replace({"h": "Home", "a": "Away", "home": "Home", "away": "Away"})
print(f"  Venue now: {matches['Venue'].unique()}")

# 4. Fix opponent names - map all variations to one clean name
opponent_mapping = {
    "arsenal": "Arsenal", "ARSENAL": "Arsenal", " Arsenal": "Arsenal",
    "Arsenal ": "Arsenal", "Arsenl": "Arsenal",
    "crystal palace": "Crystal Palace", "Crystal palace": "Crystal Palace",
    "C. Palace": "Crystal Palace    ", "Crystal Palace ": "Crystal Palace",
    "aston villa": "Aston Villa", "Aston villa": "Aston Villa",
    "A. Villa": "Aston Villa", " Aston Villa": "Aston Villa",
    "brighton": "Brighton", "Brighton ": "Brighton",
    "Brighton & Hove Albion": "Brighton", "Brighton&HA": "Brighton",
    "wolves": "Wolves", "WOLVES": "Wolves",
    "Wolverhampton": "Wolves", "Wolverhampton Wanderers": "Wolves",
    "west ham": "West Ham", "West ham": "West Ham",
    " West Ham": "West Ham", "West Ham United": "West Ham",
    "liverpool": "Liverpool", "LIVERPOOL": "Liverpool",
    "Liverpool ": "Liverpool", "Liverpoool": "Liverpool",
    "chelsea": "Chelsea", "CHELSEA": "Chelsea",
    "Chelsea ": "Chelsea", " Chelsea": "Chelsea",
    "leicester": "Leicester", "LEICESTER": "Leicester",
    "Leicester City": "Leicester", "Leicester city": "Leicester",
    "norwich": "Norwich", "Norwich City": "Norwich", "Norwich city": "Norwich",
    "newcastle": "Newcastle", "NEWCASTLE": "Newcastle",
    "Newcastle United": "Newcastle", "Newcastle Utd": "Newcastle",
    "everton": "Everton", "EVERTON": "Everton",
    "Everton ": "Everton", " Everton": "Everton",
    "man united": "Man United", "Manchester United": "Man United",
    "Man Utd": "Man United", "Manchester Utd": "Man United", "MUFC": "Man United",
    "leeds": "Leeds", "LEEDS": "Leeds",
    "Leeds United": "Leeds", "Leeds Utd": "Leeds",
    "tottenham": "Tottenham", "TOTTENHAM": "Tottenham",
    "Spurs": "Tottenham", "Tottenham Hotspur": "Tottenham",
    "watford": "Watford", "WATFORD": "Watford", "Watford ": "Watford",
    "man city": "Man City", "MANCHESTER CITY": "Man City",
    "Manchester City": "Man City", "Man. City": "Man City",
    "burnley": "Burnley", "BURNLEY": "Burnley", "Burnley ": "Burnley",
    "southampton": "Southampton", "SOUTHAMPTON": "Southampton",
    "Southampton FC": "Southampton", "Soton": "Southampton",
    "fulham": "Fulham", "FULHAM": "Fulham", "Fulham ": "Fulham",
    "bournemouth": "Bournemouth", "AFC Bournemouth": "Bournemouth",
    "Bournemouth ": "Bournemouth",
    "nottm forest": "Nottm Forest", "NOTTM FOREST": "Nottm Forest",
    "Nottingham Forest": "Nottm Forest", "Nott'm Forest": "Nottm Forest",
    "luton": "Luton", "Luton Town": "Luton", "Luton town": "Luton",
    "sheffield utd": "Sheffield Utd", "Sheffield United": "Sheffield Utd",
    "Sheff Utd": "Sheffield Utd",
    "ipswich": "Ipswich", "Ipswich Town": "Ipswich", "Ipswich town": "Ipswich",
}
matches["Opponent"] = matches["Opponent"].replace(opponent_mapping)
print(f" Unique Opponent now: {sorted(matches['Opponent'].unique())}")

# 5. Fix GF column (has "two" and whitespace issues)
matches["GF"] = matches["GF"].astype(str).str.strip()
matches["GF"] = matches["GF"].replace({"two": "2"})
matches["GF"] = pd.to_numeric(matches["GF"], errors="coerce")

# 6. Fix xGA - replace missing markers with NaN
matches["xGA"] = matches["xGA"].replace({"N/A": np.nan, "n/a": np.nan, "-": np.nan, "NULL": np.nan, "": np.nan})
matches["xGA"] = pd.to_numeric(matches["xGA"], errors="coerce")

# 7. Fix Possession - replace bad values
matches["Possession"] = matches["Possession"].replace({"N/A": np.nan, "n/a": np.nan, "-": np.nan, "NULL": np.nan, "": np.nan})
matches["Possession"] = pd.to_numeric(matches["Possession"], errors="coerce")
# Fix impossible values (possession > 100)
matches.loc[matches["Possession"] > 100, "Possession"] = np.nan

# 8. Fix Attendance - remove bad values
matches["Attendance"] = matches["Attendance"].replace({"N/A": np.nan, "n/a": np.nan, "-": np.nan, "NULL": np.nan, "": np.nan})
matches["Attendance"] = pd.to_numeric(matches["Attendance"], errors="coerce")
# Fix negative attendance
matches.loc[matches["Attendance"] < 0, "Attendance"] = np.nan

# 9. Fix Corners
matches["Corners"] = pd.to_numeric(matches["Corners"], errors="coerce")

# 10. Fix impossibly high xG (99.9)
matches.loc[matches["xG"] > 10, "xG"] = np.nan

# 11. Standardise dates to dd/mm/yyyy
def parse_date(date_str):
    """Try multiple date formats and return standardised format"""
    formats = [
        "%d/%m/%Y",      # 13/08/2021
        "%Y-%m-%d",      # 2021-08-13
        "%d-%m-%Y",      # 13-08-2021
        "%m/%d/%Y",      # 08/13/2021
        "%d %b %Y",      # 13 Aug 2021
    ]
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

matches["Date"] = matches["Date"].apply(parse_date)
print(f"  Date range: {matches['Date'].min()} to {matches['Date'].max()}")

# 12. Sort by date
matches = matches.sort_values("Date").reset_index(drop=True)

print(f"  Final shape: {matches.shape}")
print(f"  Remaining missing values:\n{matches.isnull().sum()}")

# ============================================
# DATASET 2: EPL COMPARISON
# ============================================
print("\n" + "=" * 60)
print("Cleaning EPL comparison dataset...")
epl = pd.read_csv("data/raw_epl_comparison.csv")

# 1. Standardise team names
epl_name_mapping = {
    "Liverpool FC": "Liverpool",
    "manchester city": "Man City",
    "Chelsea FC": "Chelsea",
    "aston villa": "Aston Villa",
    "Newcastle United": "Newcastle",
    "Brighton & Hove Albion": "Brighton",
    "Nottingham Forest": "Nottm Forest",
    "AFC Bournemouth": "Bournemouth",
    "Man Utd": "Man United",
    "Fulham FC": "Fulham",
    "Spurs": "Tottenham",
    "West Ham Utd": "West Ham",
    "Everton FC": "Everton",
    "wolverhampton wanderers": "Wolves",
    "Leicester City": "Leicester",
    "Ipswich Town": "Ipswich",
    "Southampton FC": "Southampton",
}
epl["Team"] = epl["Team"].str.strip().replace(epl_name_mapping)

# 2. Fix Possession% - remove % symbol
epl["Possession%"] = epl["Possession%"].astype(str).str.replace("%", "").str.strip()
epl["Possession%"] = epl["Possession%"].replace({"N/A": np.nan, "nan": np.nan})
epl["Possession%"] = pd.to_numeric(epl["Possession%"], errors="coerce")
epl = epl.rename(columns={"Possession%": "Possession"})

# 3. Fix Net_Spend_M - remove text
epl["Net_Spend_M"] = epl["Net_Spend_M"].astype(str).str.replace("M", "").str.strip()
epl["Net_Spend_M"] = pd.to_numeric(epl["Net_Spend_M"], errors="coerce")

# 4. Fix xG_Diff - some are N/A
epl["xG_Diff"] = pd.to_numeric(epl["xG_Diff"], errors="coerce")

# 5. Fix GD - some stored as string
epl["GD"] = pd.to_numeric(epl["GD"], errors="coerce")

# 6. Fix Yellows
epl["Yellows"] = pd.to_numeric(epl["Yellows"], errors="coerce")

# 7. Drop Notes column (not needed for analysis)
epl = epl.drop(columns=["Notes"])

print(f"  Team names now: {epl['Team'].tolist()}")
print(f"  Shape: {epl.shape}")

# ============================================
# DATASET 3: TRANSFERS
# ============================================
print("\n" + "=" * 60)
print("Cleaning transfers dataset...")
transfers = pd.read_csv("data/raw_brentford_transfers.csv")

# 1. Remove duplicates
transfers = transfers.drop_duplicates()
print(f"  After removing duplicates: {transfers.shape}")

# 2. Standardise player names to title case
transfers["Player_Name"] = transfers["Player_Name"].str.strip().str.title()

# 3. Clean transfer fees - convert all to numeric (in millions £)
def clean_fee(fee_str):
    """Convert messy fee strings to numeric millions"""
    if pd.isna(fee_str):
        return np.nan
    fee = str(fee_str).strip().lower()
    if fee in ["free", "0", ""]:
        return 0.0
    if "loan" in fee:
        return 0.0  # loan fees treated as 0
    # Remove currency symbols
    fee = fee.replace("£", "").replace("€", "").replace(",", "")
    # Handle different formats
    if "k" in fee:
        return float(fee.replace("k", "")) / 1000
    elif "m" in fee:
        return float(fee.replace("m", ""))
    elif len(fee) > 4:  # likely full number like 3000000
        return float(fee) / 1_000_000
    else:
        return float(fee)  # already in millions

transfers["Transfer_Fee_M"] = transfers["Transfer_Fee"].apply(clean_fee)
transfers["Sale_Price_M"] = transfers["Sale_Price"].apply(clean_fee)

# 4. Clean club names
transfers["Previous_Club"] = transfers["Previous_Club"].str.strip().str.title()
transfers["Buying_Club"] = transfers["Buying_Club"].str.strip().str.title()

# 5. Fix empty sold fields
transfers["Year_Sold"] = transfers["Year_Sold"].replace({"": np.nan, "N/A": np.nan})
transfers["Buying_Club"] = transfers["Buying_Club"].replace({"": np.nan, "N/A": np.nan, "Nan": np.nan})

# 6. Drop old messy fee columns, keep clean ones
transfers = transfers.drop(columns=["Transfer_Fee", "Sale_Price"])

print(f"  Clean fees: {transfers['Transfer_Fee_M'].tolist()}")

# ============================================
# DATASET 4: PLAYERS
# ============================================
print("\n" + "=" * 60)
print("Cleaning players dataset...")
players = pd.read_csv("data/raw_brentford_players.csv")

# 1. Standardise player names to title case
players["player"] = players["player"].str.strip().str.title()

# 2. Standardise positions
position_mapping = {
    "Right Winger": "RW",
    "Striker": "ST",
    "Attacking Mid": "AM",
    "Attacking Midfielder": "AM",
    "Central Midfield": "CM",
    "Defensive Mid": "DM",
    "Centre Back": "CB",
    "Left Back": "LB",
    "Goalkeeper": "GK",
    "ST / LW": "ST",
    "LW / RW": "LW",
    "CB / RB": "CB",
    "AM / LW": "AM",
    "RB / LB": "RB",
}
players["position"] = players["position"].str.strip().replace(position_mapping)

# 3. Fix pass_completion - remove % symbol
players["pass_completion"] = players["pass_completion"].astype(str).str.replace("%", "").str.strip()
players["pass_completion"] = players["pass_completion"].replace({"N/A": np.nan, "nan": np.nan})
players["pass_completion"] = pd.to_numeric(players["pass_completion"], errors="coerce")

# 4. Fix mins - remove commas
players["mins"] = players["mins"].astype(str).str.replace(",", "").str.strip()
players["mins"] = pd.to_numeric(players["mins"], errors="coerce")

# 5. Fix market_value - convert to numeric millions
def clean_market_value(val):
    if pd.isna(val):
        return np.nan
    val = str(val).strip().lower()
    if val in ["n/a", "nan", ""]:
        return np.nan
    val = val.replace("£", "").replace("€", "").replace(",", "")
    if "m" in val:
        return float(val.replace("m", ""))
    return float(val)

players["market_value_M"] = players["market_value"].apply(clean_market_value)
players = players.drop(columns=["market_value"])

# 6. Fix apps column (stored as string for some)
players["apps"] = pd.to_numeric(players["apps"], errors="coerce")

print(f"  Player names: {players['player'].tolist()}")
print(f"  Positions: {players['position'].tolist()}")
print(f"  Market values: {players['market_value_M'].tolist()}")


# SAVE ALL CLEANED DATASETS
# ============================================
print("\n" + "=" * 60)
print("Saving cleaned datasets...")

matches.to_csv("data/cleaned_matches.csv", index=False)
epl.to_csv("data/cleaned_epl_comparison.csv", index=False)
transfers.to_csv("data/cleaned_transfers.csv", index=False)
players.to_csv("data/cleaned_players.csv", index=False)

print("All 4 cleaned datasets saved to data/ folder!")
print(f"  cleaned_matches.csv       ({matches.shape[0]} rows)")
print(f"  cleaned_epl_comparison.csv ({epl.shape[0]} rows)")
print(f"  cleaned_transfers.csv     ({transfers.shape[0]} rows)")
print(f"  cleaned_players.csv       ({players.shape[0]} rows)")