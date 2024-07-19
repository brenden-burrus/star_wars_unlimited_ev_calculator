def average_value(rarity: str, printing: str, exclude_hyperfoil: bool, exclude_regular: bool, market_value_df) -> float:
    filtered_df = market_value_df[market_value_df['Rarity'] == rarity]

    if exclude_hyperfoil:
        filtered_df = filtered_df[~filtered_df['Product Name'].str.contains("(Hyperspace)")]
    elif exclude_regular:
        filtered_df = filtered_df[filtered_df['Product Name'].str.contains("(Hyperspace)")]

    filtered_df = filtered_df[filtered_df['Printing'] == printing]

    average_price = filtered_df["Market Price"].astype(float).sum() / len(filtered_df.index)

    return average_price