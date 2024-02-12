import matplotlib as plt
import pandas as pd
import numpy as np

data = pd.read_csv("seq_real_calibrated_SCG.wav")

plt.plot(data)
plt.show()

exit()