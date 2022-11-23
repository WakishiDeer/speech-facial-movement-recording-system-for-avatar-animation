# Speech Facial Movement Recording System for Avatar Animation

This is a WEB-based implementation of "A Data Collection Protocol, Tool and Analysis for the Mapping of Speech Volume to
Avatar Facial Animation" for ICAT-EGVE 2022.

## Overview

This is an open-source project that aids researchers to collect multi-modal data during speech at different volume
levels.
You can record facial video and speech audio with phonemically well-balanced 100 Japanese Corpus.

Along with it, if you also record ARKit blendshapes-based facial movement, especially
for [Live Link Face](https://apps.apple.com/us/app/live-link-face/id1495370836), you can synchronize across these data
with timecodes.

Note that we cannot eliminate small-time error between WEB's timecodes and Live Link Face's for synchronization for now.
We will upgrade our system to be well-connected or try not to use third party app for perfect synchronization.

## Setup

Target platforms: Linux, Windows, and macOS

This repository relies on two submodules:

1. ITA Corpus - Japanese phoneme-balanced corpus provided by the [authors](#ita-corpushttpsgithubcommmoriseita-corpus)
2. WEB recording implementation
   by [Ryosuke Miyawaki](https://github.com/WakishiDeer/speech-facial-movement-recording-system-for-avatar-animation-web)

So, you need to clone with following command.

```bash
$ git clone --recursive https://github.com/WakishiDeer/speech-facial-movement-recording-system-for-avatar-animation
```

Or, if you already cloned this repository, just run following command.

```bash
$ git submodule update --remote --merge
```

After that, you can add participants to `data/participants_list.json`.
We added a user named `default` as a default setting.

If you complete adding, you have to run `src/script_randomizer/script_random_generator_ita.py` to generate randomized
order of scripts for each condition.
It will automatically create JSON files under
the `speech-facial-movement-recording-system-for-avatar-animation-web/assets/user_data/{PARTICIPANT_UUID}`.

For Windows user, there is a limitation of long length of path, so you need to allow it.
For more information, please refer
to [this site](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry).

The participants name was mapped to UUID to ensure unique ID.
This mapping was specified under the `user_uuid_mapping.json` and `user_uuid_mapping.csv` under
the `speech-facial-movement-recording-system-for-avatar-animation-web/assets/user_data/` directory.

So, please be sure to ignore such information containing privacy when managing version control system.

## Participant Data

By default, participant JSON file contains following information:

```json
{
  "{TASK_01}": {
    "normal": {
      "no": [],
      "content": [],
      "timecode_start": [],
      "timecode_stop": []
    },
    "high": {},
    "low": {},
    "muffled": {}
  },
  "{TASK_02}": {
    "normal": {
      "no": [],
      "content": [],
      "timecode_start": [],
      "timecode_stop": []
    },
    "high": {},
    "low": {},
    "muffled": {}
  },
  "participant": "{UUID}",
  "rms_max": 0.0,
  "rms_min": 0.0
}
```

For our project, we set `{TASK_01}` as [ITA Corpus](#ita-corpus-dependency) and `{TASK_02}` as five Japanese vowels.

If you follow this format and change some properties written in `index.vue`, you can use your preferred corpus.

## Credits

### ITA Corpus (dependency)

[Project Link](https://github.com/mmorise/ita-corpus) (Note that we customized ruby for the difficult Japanese Kanji)

- General Manager (プロジェクト総括)：小田恭央（SSS合同会社）
- Project Manager (プロジェクト管理)：金井郁也（明治大学）
- Creation and Management of Phrases (文章作成・管理)：小口純矢（明治大学）
- Phrase Extraction (文章抽出)：細田計
- Adviser (アドバイザ)：齊藤剛史（九州工業大学），森勢将雅（明治大学）

### Citation

- Under construction...

## License

This project is licensed under the MIT License.
