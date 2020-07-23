"""One sample t-test

For the low blood lead level group of children (<40ug/100mL), 
is the average blood lead level greater than the recent 
CDC threshold of 10 µg /100ml in 1972? In 1973?

H_o: u <= 10ug/100mL (CDC recommended level)
H_a: u > 10ug/100mL

Ian Zurutuza
8 July 2020
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


def plot_hist(s, ax, title, color='green'):
    """
    """

    n, bins, patches = ax.hist(s, bins='sturges', facecolor=color, alpha=0.5, label=title)
    # print(n,bins)
    
    ax.axvline(x=10, color='r')

    # ax.set_xlabel()
    ax.set_ylabel(title + ' count')

    return


def compute_ci_around_mean(s, confidence=0.95):

    assert scipy.stats.sem(s) == (s.std() / len(s)**0.5)

    return scipy.stats.t.interval(alpha=confidence, df=len(s)-1, loc=s.mean(), scale=scipy.stats.sem(s))


def main():

    el_paso_df = pd.read_spss(str(DATA_PATH))
    # print(el_paso_df)

    cdc_blood_lead_threshold = 10 # ug/mL

    # select 1972 under 40ug/mL
    el_paso_1972_u40 = el_paso_df[el_paso_df["Lead_72"] < 40]

    # select 1973 under 40ug/mL
    el_paso_1973_u40 = el_paso_df[el_paso_df["Lead_73"] < 40]

    # plot histograms separately
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex='all', sharey='all')

    plot_hist(el_paso_1972_u40["Lead_72"], ax[0], "1972")
    plot_hist(el_paso_1973_u40["Lead_73"], ax[1], "1973")

    # plt.suptitle('Histograms of Blood Lead Levels\n\n', fontsize='x-large', y=.9999)
    # plt.text(20, 47.5, 'binned by Sturges\' rule', fontsize='smaller', ha='center')
    plt.xlabel(r'$\mathrm{lead\ level}\ (\frac{\mu g}{dL})$')
    plt.savefig("../p2.1_one_sample_ttest/histograms_a.png")

    # # clear figure
    # plt.clf()

    # # plot histograms together
    # n, bins, patches = plt.hist(el_paso_1973_u40["Lead_73"], bins='fd', alpha=0.5, label="1973")
    # n, bins, patches = plt.hist(el_paso_1972_u40["Lead_72"], bins='fd', alpha=0.5, label="1972")
    # plt.legend(loc='upper left')
    # plt.ylabel('count')
    # plt.xlabel(r'$\mathrm{lead\ level}\ (\frac{\mu g}{mL})$')
    # plt.suptitle('Histograms of Blood Lead Levels by Year', size='x-large')
    # plt.title('binned by Freedman–Diaconis rule', size='smaller')
    # plt.savefig("../p2.1_one_sample_ttest/histograms_b.png")


    # calculate t-test statistic and p_value
    t_stat, pval = scipy.stats.ttest_1samp(el_paso_1972_u40["Lead_72"], cdc_blood_lead_threshold)
    
    print()
    print("1972")
    print(f"critical value = {scipy.stats.t.ppf(0.95, len(el_paso_1972_u40['Lead_72'])-1)}")
    print(f"t-statistic = {t_stat}")
    print(f"p-value = {pval}")
    print(f"sample mean = {el_paso_1972_u40['Lead_72'].mean()}")
    print(f"95% CI = {compute_ci_around_mean(el_paso_1972_u40['Lead_72'])}")

    t_stat, pval = scipy.stats.ttest_1samp(el_paso_1973_u40["Lead_73"], cdc_blood_lead_threshold)

    print()
    print("1973")
    print(f"critical value = {scipy.stats.t.ppf(0.95, len(el_paso_1973_u40['Lead_73'])-1)}")
    print(f"t-statistic = {t_stat}")
    print(f"p-value = {pval}")
    print(f"sample mean = {el_paso_1972_u40['Lead_73'].mean()}")
    print(f"95% CI = {compute_ci_around_mean(el_paso_1973_u40['Lead_73'])}")


if __name__=="__main__":

    main()

