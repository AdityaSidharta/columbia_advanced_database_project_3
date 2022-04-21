FILE=data/dataset.csv

if [ -f $FILE ]; then
   python src/preprocessing.py
else
   wget https://data.cityofnewyork.us/api/views/a2nx-4u46/rows.csv\?accessType\=DOWNLOAD -O $FILE
   python src/preprocessing.py
fi
