
# Books-API

## 1

### Setup a python virtual env with python mongodb installed

``` bash

# If pip is not present in you system

sudo apt update

sudo apt install python3-pip

  

# Install and activate virtual env (Linux/MacOS)

python3 -m pip install virtualenv

python3 -m venv ./venv

source ./venv/bin/activate

  

# Install and activate virtual env (Windows)

python3 -m pip install virtualenv

python3 -m venv ./venv

.\venv\Scripts\Activate.ps1

  

# Install project python requirements

pip install -r requirements.txt

```

## 2

### Initialize mongodb instance & run the indexes script

``` bash
# Initialize mongo instance
docker run --name mongodb -d -p 27017:27017 mongo

# run index creation
python3 create_index.py

```  

## 3

### Once the indexes are created, you can run the API service

### To run the API service

``` bash

python3 -m uvicorn main:app --reload

```

## 4

### To load data

Ensure you have a running mongodb instance

i.e.:

``` bash

docker run --name mongodb -d -p 27017:27017 mongo

```

Once your API service is running (see step above), run the populate script

``` bash

cd data/

python3 populate.py
