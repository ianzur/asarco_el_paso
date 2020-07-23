""" 

For each of the standard IQ measures, evaluate whether there is a statistically significant linear relationship with blood lead levels in 1972. 

Ho: the is no relationship between IQ measures and blood lead levels
Ha: there is a relationship between lead levels and standard IQ measures

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


def simple_regression(df, ax):

    x_axis = np.linspace(df.iloc[:,0].min(), df.iloc[:,0].max(), 1000)
    # print(df)
    
    # Drop rows which contain missing values.
    df = df.dropna()

    original_count = len(df)

    # remove outliers
    q1 = df.iloc[:, 1].quantile(q=0.25, interpolation='midpoint') 
    q3 = df.iloc[:, 1].quantile(q=0.75, interpolation='midpoint') 
    iqr = q3 - q1
    outliers = (df.iloc[:,1] < (q1 - 1.5 * iqr)) | (df.iloc[:,1] > (q3 + 1.5 * iqr))

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(df[~outliers])

    ax.plot(df[~outliers].iloc[:,0], df[~outliers].iloc[:,1], 'o')
    ax.plot(df[outliers].iloc[:,0], df[outliers].iloc[:,1], 's', label='outlier')
    ax.plot(x_axis, intercept + slope*x_axis, '-', label=f'$\^y = {slope:.3f}*x + {intercept:.3f}$', aa=True)

    ax.set_xlabel(df.columns[0])
    ax.set_ylabel(df.columns[1])

    ax.legend()

    print(f'{" vs. ".join(df.columns):-^40}')
    print(f'linear fit: y = {slope:.3f}*x + {intercept:.3f}')   
    print(f'r^2: \t\t{r_value**2:10.4f}')
    print(f'p-val: \t\t{p_value:10.4f}')
    print(f'std_err: \t{std_err:10.4f}')
    print(f'# of outliers: {outliers.sum():6d}')
    print()
    print()



def main():

    el_paso_df = pd.read_spss(str(DATA_PATH))
    # print(el_paso_df.columns)

    # x = el_paso_df['Lead_72']
    # iq_full = el_paso_df['IQ_Full']
    # iq_verbal = el_paso_df['IQ_Verbal']
    # iq_performance = el_paso_df['IQ_Performance']

    el_paso_df = el_paso_df.rename(columns={
        'Lead_72': 'Blood Lead Levels 1972 (ug / 100mL)',
        'Lead_73': 'Blood Lead Levels 1973 (ug / 100mL)'
    })

    fig, ax1 = plt.subplots()
    simple_regression(el_paso_df[['Blood Lead Levels 1972 (ug / 100mL)', 'IQ_Full']], ax=ax1)
    plt.savefig("lead_lvl_72_v_iq_full.png")

    fig, ax2 = plt.subplots()
    simple_regression(el_paso_df[['Blood Lead Levels 1972 (ug / 100mL)', 'IQ_Verbal']], ax=ax2)
    plt.savefig("lead_lvl_72_v_iq_verbal.png")


    fig, ax3 = plt.subplots()
    simple_regression(el_paso_df[['Blood Lead Levels 1972 (ug / 100mL)', 'IQ_Performance']], ax=ax3)
    plt.savefig("lead_lvl_72_v_iq_performance.png")


    fig, ax3 = plt.subplots()
    simple_regression(el_paso_df[['Blood Lead Levels 1973 (ug / 100mL)', 'IQ_Performance']], ax=ax3)
    plt.savefig("lead_lvl_73_v_iq_performance.png")


if __name__=="__main__":
    main()