import pandas as pd
import uuid
import pathlib
import json
import random
import os

# for generating corpus
script_path = pathlib.Path("../../data/ita-corpus/emotion_transcript_utf8.txt").resolve()
df_raw = pd.read_csv(str(script_path), header=None)
df_raw = df_raw[0].str.split(":")
df_corpus = pd.DataFrame(columns=["no", "content"])

for i, items in enumerate(df_raw):
    df_corpus = pd.concat([df_corpus, pd.DataFrame(data={
        "no": items[0],
        "content": items[1],
    }, index=[i])])

# Do NOT change order of participants! It may cause inconsistent order of corpus
participants_list_path = pathlib.Path("../../data/participants_list.json").resolve()
participants = json.load(open(str(participants_list_path), "r"))["participants_list"]

# for saving participants
df_participants = pd.DataFrame(columns=["name", "uuid"])

# mkdir
web_path = pathlib.Path(
    "../../speech-facial-movement-recording-system-for-avatar-animation-web").resolve()
os.makedirs(web_path / "assets" / "ita_scripts", exist_ok=True)
os.makedirs(web_path / "assets" / "vowel_scripts", exist_ok=True)
os.makedirs(web_path / "assets" / "user_data", exist_ok=True)

for i, p in enumerate(participants):
    # init
    vowels = [
        "あー－－－－－",
        "いー－－－－－",
        "うー－－－－－",
        "えー－－－－－",
        "おー－－－－－",
    ]
    vowels_map = {
        "あー－－－－－": 0,
        "いー－－－－－": 1,
        "うー－－－－－": 2,
        "えー－－－－－": 3,
        "おー－－－－－": 4,
    }
    conditions = [
        "normal",
        "low",
        "high",
        "muffled"
    ]
    conditions_ita_dict = {
        "normal": dict(),
        "low": dict(),
        "high": dict(),
        "muffled": dict(),
    }
    vowel_dict = {
        "normal": dict(),
        "low": dict(),
        "high": dict(),
        "muffled": dict(),
    }

    # setting for participants
    uuid_val = str(uuid.uuid5(uuid.NAMESPACE_URL, p))
    new_df = pd.DataFrame({
        "name": p,
        "uuid": uuid_val,
    }, index=[i])
    info_dict = new_df.to_dict()
    df_participants = pd.concat([df_participants, new_df], axis=0)

    random.seed(i)
    shuffled_conditions = random.sample(conditions[1:], len(conditions) - 1)  # without shuffled_conditions
    conditions_ita_dict["conditions"] = list()
    conditions_ita_dict["conditions"].append("normal")
    for condition in shuffled_conditions:
        conditions_ita_dict["conditions"].append(condition)

    for j, key_c in enumerate(conditions):
        # ITA-corpus
        corpus_shuffled_dict = df_corpus.sample(frac=1, random_state=i + j).reset_index(drop=True)
        conditions_ita_dict[key_c] = corpus_shuffled_dict.to_dict(orient="list")
        conditions_ita_dict[key_c]["timecode_start"] = ["00-00-00-00" for i in range(len(df_corpus.index))]
        conditions_ita_dict[key_c]["timecode_stop"] = ["00-00-00-00" for i in range(len(df_corpus.index))]

        # vowel corpus
        random.seed(i + j)
        shuffled_vowels = random.sample(vowels, len(vowels))
        vowel_dict[key_c]["no"] = ["vowel_" + str(vowels_map[shuffled_vowels[no]]) for no in
                                   range(len(shuffled_vowels))]
        vowel_dict[key_c]["content"] = shuffled_vowels
        vowel_dict[key_c]["timecode_start"] = ["00-00-00-00" for i in range(len(vowels))]
        vowel_dict[key_c]["timecode_stop"] = ["00-00-00-00" for i in range(len(vowels))]

    # add participant info_dict
    conditions_ita_dict["participant"] = uuid_val
    vowel_dict["participant"] = uuid_val
    # user_data_dict["participant"] = uuid_val

    # create corpus for each participant
    with open(web_path / "assets" / "ita_scripts" / ("ita_" + uuid_val + ".json"),
              "w", encoding="utf-8") as json_file:
        json.dump(conditions_ita_dict, json_file, indent=3, ensure_ascii=False)

    with open(web_path / "assets" / "vowel_scripts" / ("vowel_" + uuid_val + ".json"), "w",
              encoding="utf-8") as json_file:
        json.dump(vowel_dict, json_file, indent=3, ensure_ascii=False)

df_participants.to_csv(web_path / "assets" / "user_data" / "user_uuid_mapping.csv")
df_participants.to_json(web_path / "assets" / "user_data" / "user_uuid_mapping.json")
