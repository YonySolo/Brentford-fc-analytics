import pandas as pd

#Load all 4 raw datasets
matches = pd.read_csv("data/raw_brentford_matches.csv")
epl = pd.read_csv("data/raw_epl_comparison.csv")
transfers = pd.read_csv("data/raw_brentford_transfers.csv")
players = pd.read_csv("data/raw_brentford_players.csv")

# ---MATCHES DATASET---
print("=" * 60)
print("MATCHES DATASET")
print("=" * 60)
print(f"shape: {matches.shape[0]} rows, {matches.shape[1]} columns")
print(f"\nColumn types:\n{matches.dtypes}")
print(f"\nMissing values:\n{matches.isnull().sum()}")
print(f"\nFirst 5 rows:")
print(matches.head())
print(f"\nUnique opponents (look for duplicates/typos):")
print(sorted(matches["Opponent"].unique()))

# ----EPL COMPARISON----
print("\n" + "=" * 60)
print("EPL COMPARISON DATASET")
print("=" * 60)
print(f"Shape: {epl.shape[0]} rows, {epl.shape[1]} columns")
print(f"\nColumn types:\n{epl.dtypes}")
print(f"\nFirst 5 rows:")
print(epl.head())
print(f"\nTeam names:")
print(epl["Team"].tolist())

#----Transfer----
print("\n" + "=" * 60)
print("TRANSFERS DATASET")
print("=" * 60)
print(f"Shape: {transfers.shape[0]} rows, {transfers.shape[1]} columns")
print(f"\nTransfer fees (look at the mess):")
print(transfers["Transfer_Fee"].tolist())
print(f"\nDuplicate rows: {transfers.duplicated().sum()}")

# ---- PLAYERS ----
print("\n" + "=" * 60)
print("PLAYERS DATASET")
print("=" * 60)
print(f"Shape: {players.shape[0]} rows, {players.shape[1]} columns")
print(f"\nPlayer names (inconsistent casing):")
print(players["player"].tolist())
print(f"\nPositions (inconsistent format):")
print(players["position"].tolist())
print(f"\nMarket values (mixed formats):")
print(players["market_value"].tolist())