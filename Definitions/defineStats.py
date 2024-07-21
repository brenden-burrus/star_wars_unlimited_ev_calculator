def average_value(rarity: list, printing: str, exclude_hyperspace: bool, exclude_regular: bool, market_value_df) -> float:
    filtered_df = market_value_df[market_value_df['Rarity'].isin(rarity)]
    print(filtered_df.to_string())
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


def get_diff_between_rarities(rarity: str, market_values):
    card_names = []
    values_dict = {}
    pct_avgs = [0, 0, 0]

    filtered_df = market_values[market_values['Rarity'].eq(rarity)]
    for i, row in filtered_df[~filtered_df['Product Name'].str.contains("(Hyperspace)")].iterrows():
        card_names.append(row["Product Name"])
        
    for name in card_names:
        temp_name_list = []
        temp_price_list = []
        temp_percent_list = []
        temp_name_list.append(name)
        temp_name_list.append(name + " (Hyperspace)")
        temp_df = filtered_df[filtered_df["Product Name"].isin(temp_name_list)]

        if temp_df.shape[0] == 4:
            temp_price_list.append(temp_df.loc[(temp_df["Product Name"] == temp_name_list[0]) & (temp_df["Printing"] == "Normal"), "Market Price"].item())
            temp_price_list.append(temp_df.loc[(temp_df["Product Name"] == temp_name_list[0]) & (temp_df["Printing"] == "Foil"), "Market Price"].item())
            temp_price_list.append(temp_df.loc[(temp_df["Product Name"] == temp_name_list[1]) & (temp_df["Printing"] == "Normal"), "Market Price"].item())
            temp_price_list.append(temp_df.loc[(temp_df["Product Name"] == temp_name_list[1]) & (temp_df["Printing"] == "Foil"), "Market Price"].item())
        
            temp_percent_list.append(round(((float(temp_price_list[1]) / float(temp_price_list[0]) - 1)*100), 2))
            temp_percent_list.append(round(((float(temp_price_list[2]) / float(temp_price_list[0]) - 1)*100), 2))
            temp_percent_list.append(round(((float(temp_price_list[3]) / float(temp_price_list[0]) - 1)*100), 2))
            values_dict[name] = temp_percent_list
    
    for name in card_names:
        if name in values_dict:
            pct_avgs[0] += values_dict[name][0]
            pct_avgs[1] += values_dict[name][1]
            pct_avgs[2] += values_dict[name][2]

    pct_avgs = [val/len(card_names) for val in pct_avgs]

    print(f"Average % Difference in Market Value between Base Rarity and Foil Rarity is {pct_avgs[0]}%")
    print(f"Average % Difference in Market Value between Base Rarity and Hyperspace Rarity is {pct_avgs[1]}%")
    print(f"Average % Difference in Market Value between Base Rarity and Hyperfoil Rarity is {pct_avgs[2]}%")

    for key, value in values_dict.items():
        if value[2] > pct_avgs[2]:
            print(f"{key} has a higher % difference in Base to Hyperfoil Price than average at {value[2]}%")
                