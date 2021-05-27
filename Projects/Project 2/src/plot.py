import pandas as pd

bean_data = pd.read_excel("../input/Dry_Bean_Dataset.xls")

import matplotlib.pyplot as plt
import seaborn as sb
sb.pairplot(bean_data, hue='Class')

plt.savefig('out.png')