import matplotlib.pyplot as plt
import pandas as pd
import pathlib


def read_script(_script_path):
    return pd.read_csv(str(_script_path), header=None)


script_path = pathlib.Path("../../data/ita-corpus/emotion_transcript_utf8.txt").resolve()

# extract selected script
df_raw = read_script(script_path)
df_katakana = df_raw[1]
# create a row to count the letters
# remove punctuations
punctuations = ["、", "。"]
len_list = []
for i, line in enumerate(df_katakana):
    for p in punctuations:
        df_katakana[i] = line.replace(p, "")
# insert the row of length
df_katakana = pd.concat([df_katakana, df_katakana.str.len()], axis=1)
df_katakana.columns = ["content", "length"]

# matplotlib
# plot the median
plt.hist(df_katakana["length"], bins=30)
plt.title("Distribution of the length of the scripts")
plt.xlabel("Length of the scripts")
plt.ylabel("Number of the scripts")
plt.axvline(df_katakana["length"].median(), color="red", linestyle="dashed", linewidth=1)
# plot the value of median
min_ylim, max_ylim = plt.ylim()
plt.text(df_katakana["length"].median() * 1.1, max_ylim * 0.9, "Median: {:.2f}".format(df_katakana["length"].median()))
# quartiles
q1 = df_katakana["length"].quantile(0.25)
q3 = df_katakana["length"].quantile(0.75)
# plot the quartiles
plt.axvline(q1, color="red", linestyle="dashed", linewidth=1)
plt.axvline(q3, color="red", linestyle="dashed", linewidth=1)
# plot the value of quartiles
plt.text(q1 * 1.1, max_ylim * 0.8, "Q1: {:.2f}".format(q1))
plt.text(q3 * 1.1, max_ylim * 0.7, "Q3: {:.2f}".format(q3))

plt.show()
