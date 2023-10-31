import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


data = pd.read_csv("output_seq_synth_calibrated_35.csv")
x = np.linspace(0, len(data), len(data))
plt.plot(data)
plt.title("Output of Sequenced, Synthesized, Calibrated, Heartsound Data")
plt.ylabel("Amplitude")
plt.xlabel("Samples")

plt.show()