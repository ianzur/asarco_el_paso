"""Two sample t-test

Are the average blood lead levels different between children who spent
the first 2 years of life within a mile of the smelter as compared to
children who did not in 1972? In 1973?

H_o: u_a == u_b
H_a: u_a != u_b

Ian Zurutuza
8 July 2020
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats

plt.style.use('seaborn-deep')

DATA_PATH = Path("../4. EL PASO DATA.sav")


def ci_diff(a, b):
    """
    assuming equal variances

    Daniel pg. 179 
    eq. 6.4.2 - 6.4.4
    """

    a = a.dropna()
    b = b.dropna()

    dof = (len(a) + len(b) - 2)
    std_pooled = np.sqrt(((len(a) - 1)*a.var() + (len(b) - 1)*b.var()) / dof) 

    diff_mean = a.mean() - b.mean()
    MoE = scipy.stats.t.ppf(0.975, dof) * std_pooled * np.sqrt(1/len(a) + 1/len(b))

    print ('The difference between groups is {:3.4f} [{:3.4f} to {:3.4f}] (mean [95% CI])'.format(diff_mean, diff_mean - MoE, diff_mean + MoE))


def main():

    el_paso_df = pd.read_spss(str(DATA_PATH))
    # print(el_paso_df['FST2YRS'].unique())

    # rename for plot
    el_paso_df = el_paso_df.rename(columns={'Lead_72': '1972', 'Lead_73': '1973'})
    # print(el_paso_df.columns)

    ### plot
    fig, ax = plt.subplots()

    ax1, ax2 = el_paso_df.boxplot(column=['1972', '1973'], by=['FST2YRS'], ax=ax)
    ax1.set_ylabel(r'$\mathrm{Blood\ Lead\ Level}\ (\frac{\mu g}{dL})$')
    ax1.set_xlabel('')
    ax2.set_xlabel('')

    fig.text(0.5, 0.06, 'spent the first 2 years of life within a mile of ASARCO', ha='center')
    plt.suptitle('Blood Lead Levels')
    
    plt.savefig('../p2.2_two_sample_ttest/boxplot.png')
    ### end plot

    print(f"\t1-sided critical value = {scipy.stats.t.ppf(0.95, len(el_paso_df['1972'].dropna())-1):3.4f}")

    tstat, pval = scipy.stats.ttest_ind(el_paso_df[el_paso_df['FST2YRS'] == 'Yes']['1972'].dropna(), el_paso_df[el_paso_df['FST2YRS'] == 'No']['1972'].dropna())
    
    print(1-scipy.stats.t.cdf(abs(tstat), len(el_paso_df['1972'].dropna())-1))
    
    print()
    print(f"1972\tn_yes={len(el_paso_df[el_paso_df['FST2YRS'] == 'Yes']['1972'].dropna())}, n_no={len(el_paso_df[el_paso_df['FST2YRS'] == 'No']['1972'].dropna())}")
    print('-'*45)
    print(f"\tcritical value = {scipy.stats.t.ppf(0.975, len(el_paso_df['1972'].dropna())-1):3.4f}")
    print(f"\tt-statistic    = {tstat:3.4f}")
    print(f"\tp-value        = {pval:3.4f}")
    print(f"\tmean (yes)     = {el_paso_df[el_paso_df['FST2YRS']=='Yes']['1972'].mean():3.4f}")
    print(f"\tmean (no)      = {el_paso_df[el_paso_df['FST2YRS']=='No']['1972'].mean():3.4f}")

    ci_diff(el_paso_df[el_paso_df['FST2YRS']=='Yes']['1972'], el_paso_df[el_paso_df['FST2YRS']=='No']['1972'])

    tstat, pval = scipy.stats.ttest_ind(el_paso_df[el_paso_df['FST2YRS'] == 'Yes']['1973'].dropna(), el_paso_df[el_paso_df['FST2YRS'] == 'No']['1973'].dropna())

    print(1-scipy.stats.t.cdf(abs(tstat), len(el_paso_df['1972'].dropna())-1))


    print()
    print(f"1973\tn_yes={len(el_paso_df[el_paso_df['FST2YRS'] == 'Yes']['1973'].dropna())}, n_no={len(el_paso_df[el_paso_df['FST2YRS'] == 'No']['1973'].dropna())}")
    print('-'*45)
    print(f"\tcritical value = {scipy.stats.t.ppf(0.975, len(el_paso_df['1973'].dropna())-1):3.4f}")
    print(f"\tt-statistic    = {tstat:3.4f}")
    print(f"\tp-value        = {pval:3.4f}")
    print(f"\tmean (yes)     = {el_paso_df[el_paso_df['FST2YRS']=='Yes']['1973'].mean():3.4f}")
    print(f"\tmean (no)      = {el_paso_df[el_paso_df['FST2YRS']=='No']['1973'].mean():3.4f}")

    ci_diff(el_paso_df[el_paso_df['FST2YRS']=='Yes']['1973'], el_paso_df[el_paso_df['FST2YRS']=='No']['1973'])


if __name__=="__main__":
    main()

