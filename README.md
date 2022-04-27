# CS6111 - Advanced Database System - Project 3

## Team Members
```
Name: Aditya Kelvianto Sidharta
UNI: aks2266
```

## List of Files
```
├── LICENSE -> Lincensing of the repository
├── README.md -> Readme file explaining about how to navigate the repository
├── data -> Folder containing the raw dataset downloaded from Open NYC data
├── download_dataset.sh -> Bash script used to download, preprocess, and transform the raw dataset into integrated dataset
├── dummy.csv -> Sample integrated dataset used to test the validity of the algorithm
├── example-run.txt -> Sample run of the algorithm
├── main.py -> Main Script used to run the algortihm
├── notebooks
│ ├── main.ipynb -> Notebook used to test the algorithm
│ └── preprocessing.ipynb -> Notebook used to test the preprocessing script
├── output.txt -> Sample run of the algorithm
├── requirements.txt -> Library used in this algorithm
├── run.sh -> Bash script used to run the algorithm
└── src
    ├── __init__.py
    ├── algorithm.py -> Script containing the algortihm logic
    ├── config.py -> Parameters to be set
    ├── display.py -> Script containing printing functions
    ├── paths.py -> Script containing all paths in the repository
    └── preprocessing.py -> Script to preprocess the raw dataset
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
bash run.sh INTEGRATED-DATASET.csv 0.003 0.15 
```

### NYC Open Dataset

The NYC Open Dataset used to create the `INTEGRATED-DATASET.csv` is [https://data.cityofnewyork.us/Housing-Development/Complaint-Problems/a2nx-4u46](Complaint Problems), 
where it is records of complaints that are made by the public through the 311 Citizen Services Center. 
In this dataset, a single complaint is associated with one or more problems reported by the complainant.

Using this fact, we are able to create a "market basket" of complaints to learn about association between different problems reported to the 311 Citizen Services Center.
As problems that co-occur or results in another problem are usually reported in a single complaint call, we are able to group all problems (Indicated by the `ProblemID`)
that occur in the same complaint (Indicated by the `ComplaintID`) into a single row at `INTEGRATED-DATASET.csv`

Upon inspection on the dataset, it appears that the dataset is not normalized. We need to ensure the 1:1 relationship
between the ID and Description of the columns (i.e `UnitTypeID` - `UnitType`, `SpaceTypeID` - `SpaceType`), and thus 
we need to perform some manual cleanup on the dataset

The complaints' dataset is comprehensive, as each of the problem is indicated by the Unit Type where the problem was reported (`UnitType`), The Space Type where the problem 
was reported (`SpaceType`), The major category of the problem (`MajorCategory`), The minor category of the problem (`MinorCategory`), and the code of the problem (`Code`). After experimentation,
the combination of Minor Category and Code provides the most expansive yet concise definition of the complaints, and then it is used as the entity within the market basket

The code in order to download the dataset, cleanup the dataset, and aggregate it into the INTEGRATED-DATASET.csv format is contained in the `processing.py` and `download_dataset.sh`

In order to generate the dataset,

```
bash download_dataset.sh
```

Do take note that huge amount of memory is needed to load the dataset. The bash script was run in a laptop with 16GB of Memory. In order to skip this step,
the `INTEGRATED-DATASET.csv` has been provided instead.

### Apriori Algorithm

In order to run the algorithm,

```
bash run.sh INTEGRATED-DATASET.csv 0.003 0.15
```

We are using the Apriori algorithm specified in Agrawal and Srikant paper in VLDB 1994. To be specific, we are implementing the 2.1.1 subsection in order to 
select the Lk candidate of the entity set by matching all (1...k-1)th item within two sets, and adding it to the candidate if kth item of first set is lexicographically lesser than the second set. 
After that, we employ pruning stage where a candidate is pruned if any combination of the subsets of the candidate does not appear in l(k-1) sets. 

Due to the vast amount of different complaints and the dataset size, we need to choose a small amount of support in order to extract interesting associations of problems that 
does not appear often in the dataset. However, we are keeping the Confidence level high in order to make sure that the association is less likely to appear by chance, but they co-occur together pretty often. Therefore,
min_sup = 0.003 and min_conf = 0.15 is chosen for that reason.