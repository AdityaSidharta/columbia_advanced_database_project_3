# CS6111 - Advanced Database System - Project 3

## Team Members
```
Name: Aditya Kelvianto Sidharta
UNI: aks2266
```

## List of Files
```
├── LICENSE
├── README.md
├── data
├── download_dataset.sh
├── dummy.csv
├── main.py
├── notebooks
│ ├── main.ipynb
│ └── preprocessing.ipynb
├── output.txt
├── requirements.txt
├── run.sh
└── src
    ├── __init__.py
    ├── algorithm.py
    ├── config.py
    ├── display.py
    ├── paths.py
    └── preprocessing.py
```

## Running the Program

### Setting up the program

This program assumes that you have:

1. Python 3.6 or later installed. Installation instructions can be found at: [https://www.tecmint.com/install-python-in-ubuntu/](https://www.tecmint.com/install-python-in-ubuntu/)
2. Virtual Environment Installed. Installation instructions can be found at: [https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

Setting up and Activating Virtual Environment and Installing the Required packages
```
python -m venv cs6111_proj3
source cs6111_proj3/bin/activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:./src"
```
