## Agenda

### Intro/Access
- **Duration:** 15 minutes


### Motivation
- **Duration:** 20 minutes


### Presentation: Data Acquisition, Preparation
- **Duration:** 1.5 hours
- **Hands On:** 
  - [Hands_On_Notebooks/1-SpyPlane-DataCleaning-Unsolved.ipynb](Hands_On_Notebooks/1-SpyPlane-DataCleaning-Unsolved.ipynb)


### Break
- **Duration:** 15 minutes


### Presentation: Model Experimentation
- **Duration:** 45 minutes
- **Hands On:** 
    - [Hands_On_Notebooks/2-SpyPlane-RandomForestClassifier-Unsolved.ipynb](Hands_On_Notebooks/2-SpyPlane-RandomForestClassifier-Unsolved.ipynb)


### Presentation: Model Evaluation
- **Duration:** 45 minutes
- **Hands On:** 
    - [Hands_On_Notebooks/3-SpyPlane-EvaluatingModels-Unsolved.ipynb](Hands_On_Notebooks/3-SpyPlane-EvaluatingModels-Unsolved.ipynb)


### If Time Permits: Hyperparameter Tuning
- **Hands On:** 
    - [misc_files/Spy-Plane-Project/4-SpyPlane-OptimizingModels-Unsolved.ipynb](misc_files/Spy-Plane-Project/4-SpyPlane-OptimizingModels-Unsolved.ipynb)
      - *NOTE: You may have to change the path for data or else broken upload errors will appear. Refer to previous notebooks to identify appropriate relevant path.*


### Q&A
- **Duration:** 10 minutes


## Background
This notebook contains materials for the Introduction to Machine Learning workshop. 

This data comes from a news [article](https://www.buzzfeednews.com/article/peteraldhous/hidden-spy-planes) that used machine learning 
to identify potential spy aircraft over the continental United States. 
The data is available in this [Github repository](https://github.com/BuzzFeedNews/2017-08-spy-plane-finder) and on 
[Kaggle](https://www.kaggle.com/jboysen/spy-plane-finder)
and the code in this notebook is based on details found [here](https://buzzfeednews.github.io/2017-08-spy-plane-finder/).

## Contents
The Demo-Notebooks folder contains the exercises for the Python overview,
linear regression example, and logistic regression example. 

The Spy-Plane-Project folder contains the following interactive activities:
* 1-SpyPlane-DataCleaning-Unsolved.ipynb
* 2-SpyPlane-RandomForestClassifier-Unsolved.ipynb
* 2-SpyPlane-RandomForestClassifier-Unsolved.ipynb
* 3-SpyPlane-EvaluatingModels-Unsolved.ipynb
* 4-SpyPlane-OptimizingModels-Unsolved.ipynb
* 5-SpyPlane-CreateModel.ipynb
* 6-SpyPlane-App-Visualizations.ipynb
* 7-SpyPlane-Flight-Path-Visualization.ipynb
* 8-SpyPlane-Feature-Engineering.ipynb
* Solved folder - contains solutions for each Unsolved notebook.

The Model-Comparison folder contains scripts to evaluate precision and recall for various
models using the domino stats features in the Jobs overview page.

The Intro-to-ML-Reference.pdf is a reference guide to many of the functions
needed for the intractive exercises. 

Note that the hyperparameter tuning contest will not work outside of live Domino workshops unless you set up your own S3 bucket or other storage option. 

## Dependencies
When copying this project onto a new Domino instance, it may be necessary to adjust
the Compute Environment.
The following Domino-provided base image contains all dependencies for this project:
`quay.io/domino/base:Ubuntu18_DAD_Py3.6_R3.6_20190918`.

These are the Pluggable Workspace settings for this base image:
```
jupyter:
  title: "Jupyter (Python, R, Julia)"
  iconUrl: "/assets/images/workspace-logos/Jupyter.svg"
  start: [ "/var/opt/workspaces/jupyter/start" ]
  httpProxy:
    port: 8888
    rewrite: false
    internalPath: "/{{ownerUsername}}/{{projectName}}/{{sessionPathComponent}}/{{runId}}/{{#if pathToOpen}}tree/{{pathToOpen}}{{/if}}"
    requireSubdomain: false
  supportedFileExtensions: [ ".ipynb" ]
jupyterlab:
  title: "JupyterLab"
  iconUrl: "/assets/images/workspace-logos/jupyterlab.svg"
  start: [  /var/opt/workspaces/Jupyterlab/start.sh ]
  httpProxy:
    internalPath: "/{{ownerUsername}}/{{projectName}}/{{sessionPathComponent}}/{{runId}}/{{#if pathToOpen}}tree/{{pathToOpen}}{{/if}}"
    port: 8888
    rewrite: false
    requireSubdomain: false
vscode:
 title: "vscode"
 iconUrl: "/assets/images/workspace-logos/vscode.svg"
 start: [ "/var/opt/workspaces/vscode/start" ]
 httpProxy:
    port: 8888
    requireSubdomain: false
rstudio:
  title: "RStudio"
  iconUrl: "/assets/images/workspace-logos/Rstudio.svg"
  start: [ "/var/opt/workspaces/rstudio/start" ]
  httpProxy:
    port: 8888
    requireSubdomain: false
```

See the [Domino documentation](https://docs.dominodatalab.com/en/latest/user_guide/f51038/environment-management/)
for more details about managing compute environments.
Additional package installations may be required if using other base images.
