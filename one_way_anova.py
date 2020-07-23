"""


Are the average blood lead levels different between children based on the radius (miles) of the smelter where they spent the first two years of their life in 1972? In 1973?

Ho: proximity to the smelter during the first two years of life has NO effect on the mean blood lead level (mu_1 = mu_2)
Ha: proximity to the smelter during the first two years of life has an increases the mean blood lead level


SPSS:
ONEWAY /VARIABLES= Lead_72 Lead_73 BY FST2YRS
	/STATISTICS=DESCRIPTIVES HOMOGENEITY.

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

def main():

    el_paso_data = pd.read_spss(str(DATA_PATH))

    el_paso_data = el_paso_data.rename(
        columns={
            'FST2YRS': "lived first 2 years within 1 mile of ASARCO",
            'Lead_72': "1972 Blood Lead Level (ug / 100mL)",
            'Lead_73': "1973 Blood Lead Level (ug / 100mL)",
        }
    )

    # create boolean mask
    first_2_years = el_paso_data['lived first 2 years within 1 mile of ASARCO'] == 'Yes'

    # 1972
    bll_1972 = el_paso_data["1972 Blood Lead Level (ug / 100mL)"]
    print(scipy.stats.f_oneway(bll_1972[first_2_years].dropna(), bll_1972[~first_2_years].dropna()))

    # 1973
    bll_1973 = el_paso_data["1973 Blood Lead Level (ug / 100mL)"]
    print(scipy.stats.f_oneway(bll_1973[first_2_years].dropna(), bll_1973[~first_2_years].dropna()))

    mean_near_72 = bll_1972[first_2_years].mean()
    mean_far_72 = bll_1972[~first_2_years].mean()
    mean_near_73 = bll_1973[first_2_years].mean()
    mean_far_73 = bll_1973[~first_2_years].mean()

    plot_df = pd.DataFrame(
        {
            '1972': {'within 1 mile': mean_near_72, 'outside 1 mile': mean_far_72} ,
            '1973': {'within 1 mile': mean_near_73, 'outside 1 mile': mean_far_73},
        },
    ).unstack().rename('average blood lead levels ug/dL').sort_index(level=1)

    plot_df.index = [' '.join(col).strip() for col in plot_df.index.values]

    plot_df.plot(style='D-', rot=8)
    plt.show()



if __name__=="__main__":
    main()

