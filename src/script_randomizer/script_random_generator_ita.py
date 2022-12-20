"""
This script generates a random script for the ITA-corpus and Japanese vowels.
You can edit and optimize your own script by changing the parameters in the lines.

This script is distributed under the MIT License
Copyright (c) 2022 Ryosuke Miyawaki
"""

import pandas as pd
import uuid
import pathlib
import json
import random
import os


def read_script(_script_path):
    return pd.read_csv(str(_script_path), header=None)


is_counterbalance = True

# for generating corpus
script_path = pathlib.Path("../../data/ita-corpus/emotion_transcript_utf8.txt").resolve()
web_path = pathlib.Path(
    "../../speech-facial-movement-recording-system-for-avatar-animation-web").resolve()

# formatting for ita-corpus
df_raw = read_script(script_path)
df_raw = df_raw[0].str.split(":")
df_corpus = pd.DataFrame(columns=["no", "content"])
# give no and its content
for i, items in enumerate(df_raw):
    df_corpus = pd.concat([df_corpus, pd.DataFrame(data={
        "no": items[0],
        "content": items[1],
    }, index=[i])])
# for extract selected corpus
extracted_index_path = pathlib.Path("../../data/ita-corpus/selected_index_ita_emo.txt").resolve()
series_extracted_corpus = pd.read_csv(str(extracted_index_path), header=None)[0]
# extract selected corpus
df_corpus = df_corpus[df_corpus.index.isin(series_extracted_corpus[:])]

# timecodes setting
init_timecode_format = "00-00-00-00"

# Do NOT change order of participants! It may cause inconsistent order of corpus
participants_list_path = pathlib.Path("../../data/participants_list.json").resolve()
participants = json.load(open(str(participants_list_path), "r"))["participants_list"]
num_participants = len(participants)
# for saving participants
df_participants = pd.DataFrame(columns=["name", "uuid"])

for i, p in enumerate(participants):
    # init vowels
    vowels = [
        "あー－－－－－",
        "いー－－－－－",
        "うー－－－－－",
        "えー－－－－－",
        "おー－－－－－",
    ]
    # create vowels_map with index
    vowels_map = {}
    for j, vow in enumerate(vowels):
        # note that keys are string type and values are int type
        vowels_map[vow] = j

    # create random order of scripts
    conditions = [
        "normal",
        "high",
        "muffled"
    ]
    ita_dict = {}
    vowel_dict = {}
    for cond in conditions:
        ita_dict[cond] = dict()
        vowel_dict[cond] = dict()

    # setting for participants
    uuid_val = str(uuid.uuid5(uuid.NAMESPACE_URL, p))
    new_df = pd.DataFrame({
        "name": p,
        "uuid": uuid_val,
    }, index=[i])
    info_dict = new_df.to_dict()
    df_participants = pd.concat([df_participants, new_df], axis=0)

    # generate randomized conditions and scripts
    random.seed(i)
    shuffled_conditions = list()  # without normal condition
    if is_counterbalance:
        # counterbalance based on the number of participants
        if i % 2 == 0:
            shuffled_conditions.append("high")
            shuffled_conditions.append("muffled")
        else:
            shuffled_conditions.append("muffled")
            shuffled_conditions.append("high")
    else:
        shuffled_conditions = random.sample(conditions[1:], len(conditions) - 1)

    ita_dict["conditions"] = list()
    ita_dict["conditions"].append("normal")
    for condition in shuffled_conditions:
        ita_dict["conditions"].append(condition)

    for j, key_c in enumerate(conditions):
        # ITA-corpus
        corpus_shuffled_dict = df_corpus.sample(frac=1, random_state=i + j).reset_index(drop=True)
        ita_dict[key_c] = corpus_shuffled_dict.to_dict(orient="list")
        ita_dict[key_c]["timecode_start"] = [init_timecode_format for _ in range(len(df_corpus.index))]
        ita_dict[key_c]["timecode_stop"] = [init_timecode_format for _ in range(len(df_corpus.index))]

        # vowel corpus
        random.seed(i + j)
        shuffled_vowels = random.sample(vowels, len(vowels))
        vowel_dict[key_c]["no"] = ["vowel_" + str(vowels_map[shuffled_vowels[no]]) for no in
                                   range(len(shuffled_vowels))]
        vowel_dict[key_c]["content"] = shuffled_vowels
        vowel_dict[key_c]["timecode_start"] = [init_timecode_format for _ in range(len(vowels))]
        vowel_dict[key_c]["timecode_stop"] = [init_timecode_format for _ in range(len(vowels))]

    # merge both dict with user_data_dict
    user_data_dict = dict()
    user_data_dict["ita"] = ita_dict
    user_data_dict["vowel"] = vowel_dict
    user_data_dict["timecode_sync"] = init_timecode_format
    # add info into user_data_dict
    user_data_dict["rms_min"] = 0.0
    user_data_dict["rms_max"] = 0.0
    user_data_dict["participant"] = uuid_val

    # create corpus for each participant
    user_data_dir_path = web_path / "assets" / "user_data" / uuid_val
    # create dirs
    os.makedirs(user_data_dir_path, exist_ok=True)
    if (user_data_dir_path / ("data_" + uuid_val + ".json")).exists():
        print(f"The file already exists: {uuid_val}")
    else:
        with open(user_data_dir_path / ("data_" + uuid_val + ".json"), "w", encoding="utf-8") as json_file:
            json.dump(user_data_dict, json_file, indent=3, ensure_ascii=False)

    df_participants.to_csv(web_path / "assets" / "user_data" / "user_uuid_mapping.csv")
    df_participants.to_json(web_path / "assets" / "user_data" / "user_uuid_mapping.json")
