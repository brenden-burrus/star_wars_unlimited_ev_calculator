import pandas as pd

from Definitions.defineStats import average_value, get_expected_value, get_diff_between_rarities
from Definitions.definePullRates import get_pull_rates

# List of Showcases
leaders = [
    "Gar Saxon - Viceroy of Mandalore", 
    "Qi'ra - I Alone Survived", 
    "Finn - This is a Rescue", 
    "Rey - More Than a Scavenger", 
    "Hondo Ohnaka - That's Good Business", 
    "Jabba the Hutt - His High Exaltedness", 
    "Boba Fett - Daimyo",
    "Hunter - Outcast Sergeant", 
    "Bossk - Hunting His Prey", 
    "Kylo Ren - Rash and Deadly", 
    "Bo-Katan Kryze - Princess in Exile", 
    "Han Solo - Worth the Risk", 
    "Cad Bane - He Who Needs No Introduction", 
    "Doctor Aphra - Rapacious Archaeologist",
    "Fennec Shand - Honoring the Deal", 
    "Lando Calrissian - With Impeccable Taste"
]

def cleanse_market_value_csv(csv_name, leaders):

    # Read Market Data CSV
    df = pd.read_csv(csv_name)

    hyper_leaders = []
    for leader in leaders:
        hyper_leaders.append(leader + " (Hyperspace)")

    #Cleaning up Market data to remove bases and add the showcase printing option
    showcase_filter = df['Product Name'].isin(leaders)
    base_filter = df['Product Name'].str.contains("//")
    hyper_leader_filter = df['Product Name'].isin(hyper_leaders)

    df = df[~showcase_filter]
    df = df[~base_filter]
    df = df[~hyper_leader_filter]

    df['Market Price'] = df['Market Price'].map(lambda x: x.replace('$',''))

    df["Rarity"] = df["Rarity"].mask(df['Product Name'].str.contains("(Showcase)"), "Showcase")

    return df


if __name__ == "__main__":

    mv_df = cleanse_market_value_csv('market_values_7_20_24.csv', leaders)
    pull_rates = get_pull_rates()
    get_expected_value(24, pull_rates, mv_df)
    get_diff_between_rarities("Legendary", mv_df)
    get_diff_between_rarities("Rare", mv_df)
