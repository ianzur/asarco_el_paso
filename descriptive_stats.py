"""descriptive stats

Ian Zurutuza
21 June 2020
"""

from pathlib import Path

import numpy as np
import pandas as pd


def unique_values(df, attribute):

    print(attribute)

    # 1972
    year_1972_lead_less_than_40ug = df[df["Lead_72"] < 40]
    year_1972_lead_between_40_68ug = df[(df["Lead_72"] >= 40) & (df["Lead_72"] <= 68)]

    s_u40 = year_1972_lead_less_than_40ug[attribute]
    s_40_to_68 = year_1972_lead_between_40_68ug[attribute]

    u40 = s_u40.value_counts()
    b40_68 = s_40_to_68.value_counts()

    data_1972 = pd.concat([u40, b40_68], axis=1, keys=["u40", "40-68"])

    tot_sum = data_1972.sum().sum()

    row_sum = data_1972.sum(axis=1)
    row_sum.name = "Total"

    data_1972 = data_1972.join(row_sum)
    data_1972.index = data_1972.index.to_list()

    column_sum = data_1972.sum(axis=0)
    column_sum.name = "Total"

    data_1972 = data_1972.append(column_sum)

    as_percent = (data_1972 / tot_sum) * 100
    as_percent = as_percent.round(2)

    data_1972 = data_1972.astype(str) + " (" + as_percent.astype(str) + ")"

    # 1973
    year_1973_lead_less_than_40ug = df[df["Lead_73"] < 40]
    year_1973_lead_between_40_68ug = df[(df["Lead_73"] >= 40) & (df["Lead_73"] <= 68)]

    s_u40 = year_1973_lead_less_than_40ug[attribute]
    s_40_to_68 = year_1973_lead_between_40_68ug[attribute]

    u40 = s_u40.value_counts()
    b40_68 = s_40_to_68.value_counts()

    data_1973 = pd.concat([u40, b40_68], axis=1, keys=["u40", "40-68"])

    tot_sum = data_1973.sum().sum()

    row_sum = data_1973.sum(axis=1)
    row_sum.name = "Total"

    data_1973 = data_1973.join(row_sum)
    data_1973.index = data_1973.index.to_list()

    column_sum = data_1973.sum(axis=0)
    column_sum.name = "Total"

    data_1973 = data_1973.append(column_sum)

    as_percent = (data_1973 / tot_sum) * 100
    as_percent = as_percent.round(2)

    data_1973 = data_1973.astype(str) + " (" + as_percent.astype(str) + ")"

    data = pd.concat([data_1972, data_1973], axis=1, keys=["1972", "1973"])

    return data


def calc_mean_median(df, attr):

    u40_1972 = df[df["Lead_72"] < 40]
    b4068_1972 = df[(df["Lead_72"] >= 40) & (df["Lead_72"] <= 68)]
    u40_1973 = df[df["Lead_73"] < 40]
    b4068_1973 = df[(df["Lead_73"] >= 40) & (df["Lead_73"] <= 68)]

    s = u40_1972[attr]
    sb = b4068_1972[attr]

    mean = s.mean().round(2)
    std = s.std().round(2)

    mean_std_as_str = mean.astype(str) + " (" + std.astype(str) + ")"

    mean = sb.mean().round(2)
    std = sb.std().round(2)

    bmean_std_as_str = mean.astype(str) + " (" + std.astype(str) + ")"

    # median = s.median().round(2)
    # iqr = (s.quantile(0.75, "midpoint") - s.quantile(0.25, "midpoint")).round(2)

    # median_iqr_as_str = median.astype(str) + " (" + iqr.astype(str) + ")"

    n = s.count().astype(str)

    data_1972 = pd.Series([mean_std_as_str, s.count().astype(str), bmean_std_as_str, sb.count().astype(str)], index=pd.MultiIndex.from_product([['<40 ug/dL', '40-68 ug/dL'], ['mean (std)', 'n']]))    
    print(data_1972)

    s = u40_1973[attr]
    sb = b4068_1973[attr]

    mean = s.mean().round(2)
    std = s.std().round(2)

    mean_std_as_str = mean.astype(str) + " (" + std.astype(str) + ")"

    mean = sb.mean().round(2)
    std = sb.std().round(2)

    bmean_std_as_str = mean.astype(str) + " (" + std.astype(str) + ")"

    # median = s.median().round(2)
    # iqr = (s.quantile(0.75, "midpoint") - s.quantile(0.25, "midpoint")).round(2)

    # median_iqr_as_str = median.astype(str) + " (" + iqr.astype(str) + ")"

    n = s.count().astype(str)

    data_1973 = pd.Series([mean_std_as_str, s.count().astype(str), bmean_std_as_str, sb.count().astype(str)], index=pd.MultiIndex.from_product([['<40 ug/dL', '40-68 ug/dL'], ['mean (std)', 'n']]))    

    data = pd.concat([data_1972, data_1973], keys=["1972", "1973"])

    return data


def main():

    df = pd.read_spss(str(Path("../4. EL PASO DATA.sav")))

    df.to_excel("elpaso_data.xlsx")

    print(df.columns)

    # categorical
    area = unique_values(df, "Area")
    sex = unique_values(df, "Sex")
    first2years = unique_values(df, "FST2YRS")
    pica = unique_values(df, "Pica")
    colic = unique_values(df, "Colic")
    clums = unique_values(df, "Clumsiness")
    irritab = unique_values(df, "Irritability")
    convuls = unique_values(df, "Convulsions")
    iq_type = unique_values(df, "IQ_Type")
    werry_weiss_peter = unique_values(df, "Taps_41_42")

    categorical = pd.concat(
        [
            area,
            sex,
            first2years,
            pica,
            colic,
            clums,
            irritab,
            convuls,
            iq_type,
            werry_weiss_peter,
        ],
        keys=pd.MultiIndex.from_tuples([
            ("Demographics", "Area of Residence"),
            ("Demographics", "Sex"),
            ("Exposure", "Did child Live for First 2 years within a Mile of Smelter"),
            ("Symptoms (Parent Reported)", "Pica"),
            ("Symptoms (Parent Reported)", "Colic"),
            ("Symptoms (Parent Reported)", "Clumsiness"),
            ("Symptoms (Parent Reported)", "Irritability"),
            ("Symptoms (Parent Reported)", "Convulsions"),
            ("IQ Test", "Type"),
            ("", "Werry Weiss-Peters Scale of Hyperactivity")
        ]),
    )

    print(categorical)
    # print(categorical.to_latex(longtable=True))
    print(categorical.to_latex(multirow=True))


    # continuous
    age = calc_mean_median(df, "Age_Corrected")
    total_num_years = calc_mean_median(df, "TOTYRS")
    iq_verbal = calc_mean_median(df, "IQ_Verbal")
    iq_performance = calc_mean_median(df, "IQ_Performance")
    iq_full = calc_mean_median(df, "IQ_Full")
    plate_taps_right = calc_mean_median(df, "Taps_right")
    plate_taps_left = calc_mean_median(df, "Taps_left")
    visual_react_right = calc_mean_median(df, "Taps_visual_right")
    visual_react_left = calc_mean_median(df, "Taps_visual_left")
    auditory_react_right = calc_mean_median(df, "Taps_auditory_right")
    auditory_react_left = calc_mean_median(df, "Taps_auditory_left")
    finger_right = calc_mean_median(df, "Taps_finger_right")
    finger_left = calc_mean_median(df, "Taps_finger_left")

    continuous = pd.concat(
        [
            age,
            total_num_years,
            iq_verbal,
            iq_performance,
            iq_full,
            plate_taps_right,
            plate_taps_left,
            visual_react_right,
            visual_react_left,
            auditory_react_right,
            auditory_react_left,
            finger_right,
            finger_left            
        ],
        keys=pd.MultiIndex.from_tuples([
            ("Demographics", "Age"),
            ("Exposure", "Total Number of Years Spent Within 4.1 Miles of Smelter"),
            ("IQ", "Verbal"),
            ("IQ", "Performance"),
            ("IQ", "Full"),
            ("Plate Taps", "Right Hand"),
            ("Plate Taps", "Left Hand"),
            ("Visual Reaction Time", "Right Hand"),
            ("Visual Reaction Time", "Left Hand"),
            ("Auditory Reaction Time", "Right Hand"),
            ("Auditory Reaction Time", "Left Hand"),
            ("Finger-Wrist Tapping Test", "Right Hand"),
            ("Finger-Wrist Tapping Test", "Left Hand"),
        ])
    )

    # print(continuous.unstack().unstack().swaplevel(axis=1).sort_index(axis=1).to_latex(longtable=True))
    # cont = continuous.unstack().unstack().unstack().swaplevel(axis=1, i=2, j=0).sort_index(axis=1).reindex(index=['Demographics', 'Exposure', 'IQ', 'Plate Taps', 'Visual Reaction Time', 'Auditory Reaction Time', 'Finger-Wrist Tapping Test'], level=0).reindex(columns=['<40 ug/dL', '40-68 ug/dL'], level=1)
    print(continuous.unstack().unstack().unstack().swaplevel(axis=1, i=2, j=0).sort_index(axis=1).reindex(index=['Demographics', 'Exposure', 'IQ', 'Plate Taps', 'Visual Reaction Time', 'Auditory Reaction Time', 'Finger-Wrist Tapping Test'], level=0).reindex(columns=['<40 ug/dL', '40-68 ug/dL'], level=1).to_latex(multirow=True))

    print(df['Age_Corrected'].describe())
    print(df['Sex'].describe())

    # print(continuous.unstack().unstack().unstack().swaplevel(axis=1).sort_index(axis=1).reindex(index=['Demographics', 'Exposure', 'IQ', 'Plate Taps', 'Visual Reaction Time', 'Auditory Reaction Time', 'Finger-Wrist Tapping Test'], level=0).to_latex(multirow=True))





if __name__ == "__main__":
    main()
