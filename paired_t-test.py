"""Paired t-test

Is there a difference between the 1972 and 1973 average blood lead levels among the children?

H_o:  u_diff == 0 
H_a:  u_diff != 0

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


def main():

    el_paso_df = pd.read_spss(str(DATA_PATH))

    el_paso_df = el_paso_df.rename(columns={'Lead_72': '1972', 'Lead_73': '1973'})
    el_paso_df.boxplot(column=['1972', '1973'])

    plt.ylabel(r'$\mathrm{Blood\ Lead\ Level}\ (\frac{\mu g}{dL})$')
    plt.suptitle('Blood Lead Level by Year', size='x-large')

    plt.savefig('../p2.3_paired_samples_ttest/boxplot.png')

    diff = el_paso_df['1973'] - el_paso_df['1972']
        
    sample_mean = diff.mean()
    sample_std = diff.std()
    n = diff.count()

    # +|- (two sided)
    critical_value = scipy.stats.t.ppf(.975, n-1)
    # print(critical_value)

    sample_std_error = sample_std / n**0.5
    t = sample_mean / sample_std_error
    # print(t)

    tstat, pval = scipy.stats.ttest_1samp(diff.dropna(), 0)

    print(f"{'paired samples t-test 1973-1972':^45}")
    print("-"*45)
    print(f"\tcritical value = \u00B1{critical_value:>8.4f}")
    print(f"\tt-statistic    = {tstat:>9.4f}")
    print(f"\tp-value        = {pval:>9.4f}")
    print(f'\tThe difference between groups is {sample_mean:3.4f} [{sample_mean - critical_value * sample_std_error:3.4f} to {sample_mean + critical_value * sample_std_error:3.4f}] (mean [95% CI])')


if __name__=='__main__':
    main()