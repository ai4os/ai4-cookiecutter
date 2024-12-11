# {{cookiecutter.project_name}}
[![Build Status](https://jenkins.services.ai4os.eu/buildStatus/icon?job=AI4OS-hub/{{ cookiecutter.__repo_name }}/main)](https://jenkins.services.ai4os.eu/job/AI4OS-hub/job/{{ cookiecutter.__repo_name }}/job/main/)

{{cookiecutter.description}}

## Usage

To launch it, first install the package then run [deepaas](https://github.com/ai4os/DEEPaaS):
```bash
git clone {{ cookiecutter.__git_base_url }}/{{ cookiecutter.__repo_name }}
cd {{ cookiecutter.__repo_name }}
pip install -e .
deepaas-run --listen-ip 0.0.0.0
```

## Contributing

This module tries to enforce best practices by using [Black](https://github.com/psf/black)
to format the code.

For an optimal development experience, we recommend installing the VScode extensions
[Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
and [Format on Auto Save](https://marketplace.visualstudio.com/items?itemName=BdSoftware.format-on-auto-save).
Their configurations are automatically included in the [`.vscode`](./.vscode) folder.
This will format the code during the automatic saves, though you can force formatting with
`CTRL + Shift + I` (or `CTRL + S` to save).

To enable them only for this repository: after installing, click `Disable`,
then click `Enable (workspace)`.

In the Black _global_ settings, we also recommend setting `black-formatter.showNotification = off`.

## Project structure
```
│
├── Dockerfile             <- Describes main steps on integration of DEEPaaS API and
│                             {{cookiecutter.__app_name}} application in one Docker image
│
├── Jenkinsfile            <- Describes basic Jenkins CI/CD pipeline (see .sqa/)
│
├── LICENSE                <- License file
│
├── README.md              <- The top-level README for developers using this project.
│
├── VERSION                <- {{cookiecutter.__app_name}} version file
│
├── .sqa/                  <- CI/CD configuration files
│
├── {{cookiecutter.__app_name}}    <- Source code for use in this project.
│   │
│   ├── __init__.py        <- Makes {{cookiecutter.__app_name}} a Python module
│   │
│   ├── api.py             <- Main script for the integration with DEEPaaS API
│   |
│   ├── config.py          <- Configuration file to define Constants used across {{cookiecutter.__app_name}}
│   │
│   └── misc.py            <- Misc functions that were helpful accross projects
│
├── data/                  <- Folder to store the data
│
├── models/                <- Folder to store models
│
├── tests/                 <- Scripts to perfrom code testing
|
├── metadata.json          <- Metadata information propagated to the AI4OS Hub
│
├── pyproject.toml         <- a configuration file used by packaging tools, so {{cookiecutter.__app_name}}
│                             can be imported or installed with  `pip install -e .`
│
├── requirements.txt       <- The requirements file for reproducing the analysis environment, i.e.
│                             contains a list of packages needed to make {{cookiecutter.__app_name}} work
│
├── requirements-test.txt  <- The requirements file for running code tests (see tests/ directory)
│
└── tox.ini                <- Configuration file for the tox tool used for testing (see .sqa/)
```
