import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import os


def read_script(_script_path):
    return pd.read_csv(str(_script_path), header=None)


def remove_punctuations(_df_katakana):
    # create a row to count the letters
    # remove punctuations
    punctuations = ["、", "。"]
    for i, line in enumerate(_df_katakana):
        for p in punctuations:
            _df_katakana[i] = line.replace(p, "")
    # insert the row of length
    # create a row to count the letters
    _df_katakana = pd.concat([_df_katakana, _df_katakana.str.len()], axis=1)
    _df_katakana.columns = ["content", "length"]
    return _df_katakana


def plot_histogram(_df_katakana):
    # plot the median
    median, q1, q3 = calc_median_quartiles(_df_katakana)
    plt.hist(_df_katakana["length"], bins=30)
    plt.title("Distribution of the length of the scripts")
    plt.xlabel("Length of the scripts")
    plt.ylabel("Number of the scripts")
    plt.axvline(_df_katakana["length"].median(), color="red", linestyle="dashed", linewidth=1)
    # plot the value of median
    min_ylim, max_ylim = plt.ylim()
    plt.text(median * 1.1, max_ylim * 0.9, "Median: {:.2f}".format(_df_katakana["length"].median()))
    # quartiles
    # plot the quartiles
    plt.axvline(q1, color="red", linestyle="dashed", linewidth=1)
    plt.axvline(q3, color="red", linestyle="dashed", linewidth=1)
    # plot the value of quartiles
    plt.text(q1 * 1.1, max_ylim * 0.8, "Q1: {:.2f}".format(q1))
    plt.text(q3 * 1.1, max_ylim * 0.7, "Q3: {:.2f}".format(q3))
    # show
    plt.show()


def calc_median_quartiles(_df):
    _median = df_katakana["length"].median()
    _q1 = df_katakana["length"].quantile(0.25)
    _q3 = df_katakana["length"].quantile(0.75)
    return _median, _q1, _q3


def extract_script_by_length(_df_katakana, _median, _q1, _q3):
    # extract scripts by length
    # 1. less than _q1
    _df_less_q1 = _df_katakana[_df_katakana["length"] < _q1]
    # 2. between _q1 and _median
    _df_between_q1_median = _df_katakana[
        (_df_katakana["length"] >= _q1) & (_df_katakana["length"] < _median)
        ]
    # 3. between _median and _q3
    _df_between_median_q3 = _df_katakana[
        (_df_katakana["length"] >= _median) & (_df_katakana["length"] < _q3)
        ]
    # 4. more than _q3
    _df_more_q3 = _df_katakana[_df_katakana["length"] >= _q3]
    return _df_less_q1, _df_between_q1_median, _df_between_median_q3, _df_more_q3


if __name__ == "__main__":
    root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
    script_path = pathlib.Path(
        os.path.join(
            root_path, "data/ita-corpus/emotion_transcript_utf8.txt"
        )
    ).resolve()
    # extract selected script
    df_raw = read_script(script_path)
    df_katakana = df_raw[1]

    # remove punctuations
    df_katakana = remove_punctuations(df_katakana)

    # plot_histogram(df_katakana)

    # extract the scripts with length
    df_less_q1, df_between_q1_median, df_between_median_q3, df_more_q3 = extract_script_by_length(
        df_katakana, *calc_median_quartiles(df_katakana)
    )

    # the ratio to remove from the original df
    remove_script_ratio = 0.5
    # the number of scripts to remove
    remove_script_num = int(len(df_katakana) * remove_script_ratio)
    # the number of scripts to keep
    keep_script_num = len(df_katakana) - remove_script_num
    # remove scripts for each group until they reach `keep_script_num * 0.25`
    # note that seed is fixed
    random_state = 0
    # 1. less than _q1
    df_less_q1 = df_less_q1.sample(n=int(keep_script_num * 0.25), random_state=random_state)
    # 2. between _q1 and _median
    df_between_q1_median = df_between_q1_median.sample(n=int(keep_script_num * 0.25), random_state=random_state)
    # 3. between _median and _q3
    df_between_median_q3 = df_between_median_q3.sample(n=int(keep_script_num * 0.25), random_state=random_state)
    # 4. more than _q3
    df_more_q3 = df_more_q3.sample(n=int(keep_script_num * 0.25), random_state=random_state)

    # count the number of scripts in total
    print(len(df_less_q1) + len(df_between_q1_median) + len(df_between_median_q3) + len(df_more_q3))
    # each length
    print("less than Q1: {}".format(len(df_less_q1)))
    print("between Q1 and median: {}".format(len(df_between_q1_median)))
    print("between median and Q3: {}".format(len(df_between_median_q3)))
    print("more than Q3: {}".format(len(df_more_q3)))

    # concat the dataframes
    df_selected = pd.concat([df_less_q1, df_between_q1_median, df_between_median_q3, df_more_q3])
    # order index asc
    df_selected = df_selected.sort_index()
    # save the index
    index_list = list(df_selected.index)
    # save index_list
    with open(
        os.path.join(
            root_path, "data/ita-corpus/selected_index_ita_emo.txt"
        ), "w"
    ) as f:
        f.write("\n".join([str(i) for i in index_list]))
