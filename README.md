This app detects whether a human speech utterance is colored with negative, neutral, or positive emotional valence. Try the app on [Streamlit Cloud](https://bit.ly/MSVC_app).

To setup the environment:

    conda activate base
    conda update conda -c conda-forge -y
    conda remove --name msvc_env_mm --all -c conda-forge -y
    conda env create -f requirements.yml
    conda activate msvc_env_mm
    python -m pip install -e .

To run the app locally:

    streamlit run msvc/src/app.py

The training data consists of FRILL embeddings [1] derived from datasets collected by the [Unified Multilingual Dataset of Emotional Human Utterances](https://github.com/michen00/unified_multilingual_dataset_of_emotional_human_utterances) [2] as well as subsets of [3], [4], and [5].

1. J. Peplinski, J. Shor, S. Joglekar, J. Garrison, and S. Patel, "FRILL: A non-semantic speech embedding for mobile devices," in *Proc. INTERSPEECH 2021*, Brno, Czech Republic, Aug. 30–Sep. 3, 2021, pp. 1204–1208. Accessed: Feb. 1, 2022. doi: https://doi.org/10.21437/Interspeech.2021-2070.

1. M. I. Chen. "Unified multilingual dataset of emotional human utterances. V0.1.0." Github. Accessed: Jan. 29, 2022. [Online]. Available: https://github.com/michen00/unified_multilingual_dataset_of_emotional_human_utterances

1. T. Müller and D. Kreutz, *Thorsten - Open German Voice (Emotional) Dataset. V2.0.* Jun. 13, 2021. Distributed by Zenodo. Accessed: Jan. 29, 2022. [Dataset]. doi: https://doi.org/10.5281/zenodo.5525023.

1. A. Rockikz. "Speech Emotion Recognition. 914ecac." Github. Accessed: Jan. 29, 2022. [Online]. Available: https://github.com/x4nth055/emotion-recognition-using-speech

1. S. Seo and S. Choi. "로봇의 감정 및 개성을 표현할 수 있는 대화형 음성합성 오픈소스 플랫폼. b0612a0." Github. Accessed: Jan. 29, 2022. [Online]. Available: https://github.com/emotiontts/emotiontts_open_db

[![Build Status](https://app.travis-ci.com/michen00/MSVC.svg?branch=main)](https://app.travis-ci.com/michen00/MSVC)

[![codecov](https://codecov.io/gh/michen00/MSVC/branch/main/graph/badge.svg?token=QHNSF30QZ7)](https://codecov.io/gh/michen00/MSVC)
