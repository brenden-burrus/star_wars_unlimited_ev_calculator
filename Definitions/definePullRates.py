def get_pull_rates():
    # Pull Rates Defined here: https://starwarsunlimited.com/articles/boosting-ahead-of-release

    # Base Rarity Pull Rates. Rates are defined as #/pack on average
    base_common_pr = 9
    base_uncommon_pr = 3
    base_rare_pr = .875
    base_legendary_pr = .125

    # Hyperspace Rarity Pull Rates
    hyper_common_unc_pr = .667
    hyper_rare_lego_pr = .0667

    # Foil Rarity Pull Rates
    base_foil_pr = .98
    hyperfoil_rare_lego_pr = .02

    # Showcase
    showcase_pr = .00347

    return {
        "Common Pull Rate": base_common_pr,
        "Uncommon Pull Rate": base_uncommon_pr,
        "Rare Pull Rate": base_rare_pr,
        "Legendary Pull Rate": base_legendary_pr,
        "Hyperspace C/UC Pull Rate": hyper_common_unc_pr,
        "Hyperspace R/L Pull Rate": hyper_rare_lego_pr,
        "Foil Pull Rate": base_foil_pr,
        "Hyperfoil R/L Pull Rate": hyperfoil_rare_lego_pr,
        "Showcase Pull Rate": showcase_pr,
    }
