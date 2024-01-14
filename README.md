# MADE: BRFC - Behavior risk factors & cancer project

## MADE - Methods of Advanced Data Engineering
This repository contains exercises and a project developed during the course **Methods of Advanced Data Engineering** in winter semester 2023/2024 of the Master Programme AI at FAU (Friedrich-Alexander-Universität Erlangen-Nürnberg).

## Project: BRFC - Behavior risk factors & cancer project
The BRFC - Behavior risk factors & cancer project relates data of a nation wide study in the United States  
**BRFSS Behavioral Risk Factor Surveillance System**  
and cancer data of the   
**GDC - Genomic Data Commons**  
which is a research program of the National Cancer Institute (NCI) in the United States.

The hypotheses for this project are:  
(1) Behavioural risk factors are influencing the chance to develop cancer.  
(2) Behavioural risk factors are influencing the chance of mutation(s) in genes which are related to obesity.

The report supports both hypotheses. A classification is done on the final report to classify whether there are certain mutations in genes related to obesity combining both data sources.

For more information, see the [final report](project/report.ipynb)

## Exercises
Exercises were submitted during the couse and stored within the *exercise* folder.
These exercises were implemented in python or jayvee as an introduction to the project development.

## Environments
In order to choose the correct environment for either the exercises or the project, two files are located in the repositories root:  
- [made_exercise_environment.yml](made_exercise_environment.yml): to setup the environment for the exercies  
- [made_project_environment.yml](made_project_environment.yml): to setup the environment for the project  

These files can be used to automatically instantiate an environment with [Anaconda](https://www.anaconda.com/).

As a suggestion, the environment can be setup with [VSCode](https://code.visualstudio.com/) which neatly integrates [Anaconda](https://www.anaconda.com/), [Jayvee](https://github.com/jvalue/jayvee) and [Jupyter notebooks](https://jupyter.org/) with the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter).

Furthermore, the package for building and running [Jayvee](https://github.com/jvalue/jayvee) is installed via [NodeJs](https://nodejs.org/) (see [package.json](package.json)).
You can run the BRFSS data pipeline by 
```bash
npm install
"../node_modules/.bin/jv" data/brfss.jv
```
This way you do not have to install any tool manually and everything can be automated.

