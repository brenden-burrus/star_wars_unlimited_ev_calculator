def average_value(rarity: list, printing: str, exclude_hyperspace: bool, exclude_regular: bool, market_value_df) -> float:
    filtered_df = market_value_df[market_value_df['Rarity'].isin(rarity)]

    if exclude_hyperspace:
        filtered_df = filtered_df[~filtered_df['Product Name'].str.contains("(Hyperspace)")]
    elif exclude_regular:
        filtered_df = filtered_df[filtered_df['Product Name'].str.contains("(Hyperspace)")]

    filtered_df = filtered_df[filtered_df['Printing'] == printing]
    
    average_price = filtered_df["Market Price"].astype(float).sum() / len(filtered_df.index)

    return average_price


def get_expected_value(num_packs: int, pull_rates: dict, market_value_df):
    ev = 0

    base_common_avg = average_value(["Common"], "Normal", True, False, market_value_df)
    base_uc_avg = average_value(["Uncommon"], "Normal", True, False, market_value_df)
    base_rare_avg = average_value(["Rare"], "Normal", True, False, market_value_df)
    base_legendary_avg = average_value(["Legendary"], "Normal", True, False, market_value_df)

    hyper_c_uc_avg = average_value(["Common", "Uncommon"], "Normal", False, True, market_value_df)
    hyper_r_l_avg = average_value(["Rare", "Legendary"], "Normal", False, True, market_value_df)

    foil_c_uc_avg = average_value(["Common", "Uncommon"], "Foil", True, False, market_value_df)
    hyperfoil_r_l_avg = average_value(["Rare", "Legendary"], "Foil", False, True, market_value_df)

    showcase_avg = average_value(["Showcase"], "Foil", True, False, market_value_df)

    print(f"base common avg = {base_common_avg}")
    print(f"base uncommon avg = {base_uc_avg}")
    print(f"base rare avg = {base_rare_avg}")
    print(f"base lego avg = {base_legendary_avg}")

    print(f"hyper common/uncommon avg = {hyper_c_uc_avg}")
    print(f"hyper rare/lego avg = {hyper_r_l_avg}")

    print(f"foil c/uc avg = {foil_c_uc_avg}")
    print(f"hyperfoil r/l avg = {hyperfoil_r_l_avg}")
    print(f"showcase avg = {showcase_avg}")

    averages_per_pack = {}

    for key, value in pull_rates.items():
        print(f"{key}, {value}")
        match key:
            case "Common Pull Rate":
                averages_per_pack['Common'] = (base_common_avg * value)
            case "Uncommon Pull Rate":
                averages_per_pack['Uncommon'] = (base_uc_avg * value)
            case "Rare Pull Rate":
                averages_per_pack['Rare'] = (base_rare_avg * value)
            case "Legendary Pull Rate":
                averages_per_pack['Lego'] = (base_legendary_avg * value)
            case "Hyperspace C/UC Pull Rate":
                averages_per_pack['Hyper C/UC'] = (hyper_c_uc_avg * value)
            case "Hyperspace R/L Pull Rate":
                averages_per_pack['Hyper R/L'] = (hyper_r_l_avg * value)
            case "Foil Pull Rate":
                averages_per_pack['Foil'] = (foil_c_uc_avg * value)
            case "Hyperfoil R/L Pull Rate":
                averages_per_pack['Hyperfoil R/L'] = (hyperfoil_r_l_avg * value)
            case "Showcase Pull Rate":
                averages_per_pack['Showcase'] = (showcase_avg * value)


    for key in averages_per_pack:
        print(f"{key}: {averages_per_pack[key]} per pack. {(averages_per_pack[key] * num_packs)} per box")
        ev += (averages_per_pack[key] * num_packs)

    print(f"Expected Value of a box is {ev}")
