"""
Irritability, hyperactivity, pica, and colic are associated with lead exposure;
however these symptoms are also associated with other environmental, behavioral and health problems. 

Use the chi-square test to test whether each of these four symptoms is related to whether children had blood lead levels less than 40 µg/100ml or blood lead levels between 40 to 68 µg/100ml.

Ho: Lead level and [Irritability, hyperactivity, pica, and colic] are independent (have no association)
Ha: a relationship exists between lead level and [Irritability, hyperactivity, pica, and colic]

power = 0.05

SPSS:
crosstabs -> Chi2

"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats

# customize plot styling 
# https://matplotlib.org/3.2.2/tutorials/introductory/customizing.html
plt.style.use('seaborn-deep')

DATA_PATH = Path("../4. EL PASO DATA.sav")
alpha = 0.05

def chi_squares(df, attribute):
    """

    """

    # convert from categorical to regular index
    df.columns = df.columns.tolist()

    df = df.astype(float)

    df.index = pd.MultiIndex.from_product([df.index, ['count']])
    # print(df)

    odds_ratio = (df.iloc[0,0] * df.iloc[1,1]) / (df.iloc[1,0] * df.iloc[0,1]) 

    chi2, p, dof, expected_freq = scipy.stats.chi2_contingency(df, correction=False)   

    expected_freq_df = pd.DataFrame(expected_freq, columns=df.columns, index=df.index.set_levels(['expected'], level=1))
    # print(expected_freq_df)

    pretty = pd.merge(df, expected_freq_df, how='outer', on=['No', 'Yes'], left_index=True, right_index=True).reindex(index=['<40', '40-68'], level=0)

    pretty = pretty.append(pretty.xs("count", level=1).sum(axis=0).rename(('total', '')))
    pretty = pretty.join(pretty.sum(axis=1).rename('total'))

    print(f'{attribute:-^50}')
    print(pretty)

    # if expected values are less than 5 use Yates correction
    if (expected_freq < 5).any():
        print("\n\tcorrect for expected value <5 using Yates method")
        chi2, p, dof, _ = scipy.stats.chi2_contingency(df, correction=True)

    print()
    print(f'test statistic: {chi2:10.3f}')
    print(f'p-value: \t{p:10.3f}')
    print(f'dof: \t\t{dof:6d}')
    print(f'odds ratio: \t{odds_ratio:10.3f}')

    print()

    if p < 0.05: 
        print('reject Ho')
    else:
        print('accept Ho')

    print()




def main():
    el_paso_df = pd.read_spss(str(DATA_PATH))

    print(f'critical value: {scipy.stats.chi2.ppf(1 - alpha, 1):10.2f}')
    print(f'reject Ho if test statisitic is greater than critical value or p-value is less than {alpha}')

    print("1972")
    
    u40 = el_paso_df[el_paso_df["Lead_72"] < 40][['Pica','Colic', 'Clumsiness', 'Irritability']].apply(lambda x: x.value_counts()).unstack().rename('<40')
    b40_68 = el_paso_df[(el_paso_df["Lead_72"] >= 40) & (el_paso_df["Lead_72"] <= 68)][['Pica','Colic', 'Clumsiness', 'Irritability']].apply(lambda x: x.value_counts()).unstack().rename('40-68')

    lead_72 = pd.DataFrame(
        [u40, b40_68]
    )

    # print(lead_72)
    # input()

    chi_squares(lead_72["Pica"], "Pica")
    chi_squares(lead_72["Colic"], "Colic")
    chi_squares(lead_72["Clumsiness"], "Clumsiness")
    chi_squares(lead_72["Irritability"], "Irritability")


    u40 = el_paso_df[el_paso_df["Lead_72"] < 40][['Taps_41_42']].apply(lambda x: x.value_counts()).unstack().rename('<40')
    b40_68 = el_paso_df[(el_paso_df["Lead_72"] >= 40) & (el_paso_df["Lead_72"] <= 68)][['Taps_41_42']].apply(lambda x: x.value_counts()).unstack().rename('40-68')

    hyper_df = pd.merge(u40, b40_68, right_index=True, left_index=True).T
    # print(hyper_df.columns)

    # low_hyper = (hyper_df[('Taps_41_42', 0.0)] +hyper_df[('Taps_41_42', 1.0)]).rename('low')
    # high_hyper = (hyper_df[('Taps_41_42', 2.0)] +hyper_df[('Taps_41_42', 3.0)]).rename('high')
    # print()

    # hyper_df = pd.merge(low_hyper, high_hyper, right_index=True, left_index=True)
    print(hyper_df)

    # chi_squares(hyper_df, "Hyperactivity")

    # odds_ratio = (hyper_df.iloc[0,0] * hyper_df.iloc[1,1]) / (hyper_df.iloc[1,0] * hyper_df.iloc[0,1]) 
    chi2, p, dof, expected_freq = scipy.stats.chi2_contingency(hyper_df, correction=True)   

    print(expected_freq)

    print()
    print(f'test statistic: {chi2:10.3f}')
    print(f'p-value: \t{p:10.3f}')
    print(f'dof: \t\t{dof:6d}')
    # print(f'odds ratio: \t{odds_ratio:10.3f}')

    input()
    print()

    print("1973")

    u40 = el_paso_df[el_paso_df["Lead_73"] < 40][['Pica','Colic', 'Clumsiness', 'Irritability']].apply(lambda x: x.value_counts()).unstack().rename('<40')
    b40_68 = el_paso_df[(el_paso_df["Lead_73"] >= 40) & (el_paso_df["Lead_73"] <= 68)][['Pica','Colic', 'Clumsiness', 'Irritability']].apply(lambda x: x.value_counts()).unstack().rename('40-68')

    lead_73 = pd.DataFrame(
        [u40, b40_68]
    )

    chi_squares(lead_73["Pica"], "Pica")
    chi_squares(lead_73["Colic"], "Colic")
    chi_squares(lead_73["Clumsiness"], "Clumsiness")
    chi_squares(lead_73["Irritability"], "Irritability")


    u40 = el_paso_df[el_paso_df["Lead_72"] < 40][['Taps_41_42']].apply(lambda x: x.value_counts()).unstack().rename('<40')
    b40_68 = el_paso_df[(el_paso_df["Lead_72"] >= 40) & (el_paso_df["Lead_72"] <= 68)][['Taps_41_42']].apply(lambda x: x.value_counts()).unstack().rename('40-68')

    hyper_df = pd.merge(u40, b40_68, right_index=True, left_index=True).T
    print(hyper_df)

    chi2, p, dof, expected_freq = scipy.stats.chi2_contingency(hyper_df, correction=True)   

    print(expected_freq)

    print()
    print(f'test statistic: {chi2:10.3f}')
    print(f'p-value: \t{p:10.3f}')
    print(f'dof: \t\t{dof:6d}')


    # print(lead_73)
    print()

if __name__=="__main__":
    main()