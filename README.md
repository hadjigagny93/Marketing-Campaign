# Advanced Machine Learning Project : Bénédicte - El Hadji - Juan 

## Description
This project is aim to use and assemble most of the tools for Machine Learning learned during the Yotta Academy Bootcamp.

### 0. Clone this repository
```
$ git clone https://gitlab.com/yotta-academy/cohort-2020/projects/ml-project/bej-aml.git
```

### 1. Setup your virtual environment and activate it

Before setting up your virtual environment, you must check your current **python version**. 
```
source init.sh
```
```
source activate.sh
```
After that, run for installing dependencies

```
pipenv install Pipfile
```
This last command install packages required for our code.

### 2. Data

You must locate your datasets (data.csv -- without subscription column and socio_eco.csv) in the folder **data/test/** .

To execute the code, you must use the following commands, below. The first one uses a forward method/ backward method to incorporate the socioeconomic data into the main dataset.

You will recover your predicted dataset in the data/test.

```
python src/application/main.py -mf -p
```
or 

```
python src/application/main.py -mb -p
```


### 3. Architecture

### 3. Architecture
```
├── assignment                            <- File .PDF Project
│
├── data                                  <- Folder for input data
│   ├── test
│   │     ├── data.csv                    <- Data file to be inserted here WITHOUT the target
│   │     ├── socio_eco.csv               <- Secondary socioeconomic file to be inserted here
│   │     └── .gitignore                  <- Files .csv ignored by git
│   │                
│   ├── data.csv                          <- Original file received for the project set up
│   ├── socio_eco.csv                     <- Secondary original file received for the project set up
│   └── .gitignore                        <- Files .csv ignored by git
│   
├── logs                                  <- Folder with log files
│    └── .gitignore                       <- Files .ipying ignored by git
│
├── notebooks                             <- Notebooks for analysis and testing
│    └── .gitignore                       <- Files .ipying ignored by git
│ 
├── src                                   <- Forecast model
│   ├── application                       <- Folder containing the main project files
│   │    ├── models/joblib-load           <- Save / Load parameters
│   │    ├── tests
│   │    │     ├── test_model.py
│   │    │     ├── test_process.py
|   |    |     └── test_pipelines.py
│   │    │
│   │    ├── main.py                      <- Main program
│   │    ├── model.py                     <- Model used
│   │    └── pipelines.py                 <- Pipeline functionality
│   │
│   ├── domain                            
│   │  
│   ├── infrastructure                    
│   │    ├── test                         <- Folder test
│   │    │     ├── test_pipeline.py       <- Test Pipeline functionality
│   │    │     └── test_process.py        <- Test Process functionality
│   │    │
│   │    ├── generate.py                   
│   │    ├── process.py                   <- Feature engineering functionality   
│   │    └── tools.py                     <- Pipeline functionality
│   │
│   ├── interface
│   │    └── vizualize.py                 <- Vizualize data
│   │
│   ├── settings 
│   │    └── base.py                      <- Contains variables
│   │
│   └── __init__.py
│
├── Pipfile                               <- Dependencies
│   
├── Pipfile.lock   
│  
├── .gitignore                            <- Files that should be ignored by git.
│   
├── .gitlab-ci.yml                        <- Files .yml for CI/CD
│   
├── README.md                             
│
├── activate.sh                            
│
└── init.sh                                
``` 