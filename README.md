<<<<<<< HEAD
To setup the environment:

    conda activate base
    conda update conda -c conda-forge -y
    conda remove --name msvc_env --all -c conda-forge -y
    conda env create -f environment.yml
    conda activate msvc_env
    pip install -e .

To run the app locally:

    streamlit run msvc/src/app.py

[![Build Status](https://app.travis-ci.com/michen00/MSVC.svg?branch=main)](https://app.travis-ci.com/michen00/MSVC)

[![codecov](https://codecov.io/gh/michen00/MSVC/branch/main/graph/badge.svg?token=QHNSF30QZ7)](https://codecov.io/gh/michen00/MSVC)
=======
To setup the environment:

    conda activate base
    conda update conda -c conda-forge -y
    conda remove --name msvc_env --all -c conda-forge -y
    conda env create -f environment.yml
    conda activate msvc_env
    python -m pip install -e .

To run the app locally:

    streamlit run msvc/src/app.py

[![Build Status](https://app.travis-ci.com/michen00/MSVC.svg?branch=main)](https://app.travis-ci.com/michen00/MSVC)

[![codecov](https://codecov.io/gh/michen00/MSVC/branch/main/graph/badge.svg?token=QHNSF30QZ7)](https://codecov.io/gh/michen00/MSVC)
>>>>>>> 7653142f3135c6475adc055d5424e8cba0e383ef
