# Pydantic BaseModels extended with TOML and YAML loaders (Example PDM Project)

Example PDM (and Pydantic) project and micro-tutorial.

The project itself is just two very simple subclasses that just add TOML and YAML loaders to [Pydantic BaseModel](https://docs.pydantic.dev/latest/).

Uses [PyYaml](https://pyyaml.org/) for YAML and [tomli](https://github.com/hukkin/tomli) and [tomli-w](https://github.com/hukkin/tomli-w) for TOML.

### Tools Used

- PDM for managing dependencies, building, virtual environment, and scripts
- ruff for linting
- pyright for typechecking
- deptry for missing / bad dependencies

--- 

## What is PDM

PDM uses a PEP 621 compatible [pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) and allows us to manage lots of things.

In [Set Up](#set-up) and [Other Common Tasks](#other-common-tasks) we will go through a few of these:

- [virtual environments](https://pdm-project.org/latest/usage/venv/)
    - automatically created when installing dependencies
    - can also be manually managed via PDM
    - can use virtualenv, venv, or conda
    - can also use PEP 582 local package directories if you prefer
- [dependencies and dependency groups](https://pdm-project.org/latest/usage/dependency/) (e.g. dev stuff, tests, docs, etc)
    - no need for "pip install ..." or requirements.txt
    - produces a lock file including all transitive dependencies to ensure that environments have exactly the same versions (e.g. useful when deploying in production) 
    - can generate a requirements.txt if you really want one
    - has an opt-in centralized cache (like pnpm for node)
    - supports local dependenncies with relative paths    
- [the Python interpreter version](https://pdm-project.org/latest/usage/project/#choose-a-python-interpreter)
    - can manage multiple versions 
    - no need for pyenv

### Other useful things
- [NPM like scripts](https://pdm-project.org/latest/usage/scripts/) to automate tasks
    - no need to use extra tools for simple automations (Makefiles, Taskfile, etc)
- [project templates](https://pdm-project.org/latest/usage/template/)
    - e.g flask, django, etc on their centralized repo
    - can also use cookiecutter or copier templates
- multiple build backends
    - you can use PDM with any PEP 517 compatible backend like: pdm-backend, hatchling, setuptool, flit, maturin, and support is experimental for uv.
    - it uses uses PDM backend as default
- plugins to extend its functionality
- supports [publishing](https://pdm-project.org/latest/usage/publish/) to a repository like PyPI

Bellow we explore this simple project set up, and how to manage dependencies. 

--- 

## Set up 

### 1. Install PDM 

Follow the steps [Recommended Installation Method](https://pdm-project.org/en/latest/#recommended-installation-method)

Note: all commands have a `--help` flag if you need.

### 2. [Optional] Install Python 3.12 via PDM

PDM will try to match the version requirements present in the `pyproject.toml` you can ensure you have it installed using PDM itself.

You can just do:

```shell
pdm py install 3.12
pdm use 3.12
```

or specify the complete version:

```shell
pdm py install 3.12.7
pdm use 3.12.7
```

---

### 3. Install Dependencies + Create Environment

To install all dev and package requirements, do:

```shell
pdm install -G all
```

This might take some time the first time you do it (downloads et al.).

You can specify non-package dependency groups:

```shell
pdm install -G dev
```

This will create the `.venv` folder in the project root with the virtual environment and all depdencencies.

This will do an editable install of this package itself (so you can import base_model_io, see test files).

--- 

## Other Common tasks

### Using the environment in a shell

All commands ran with `pdm run` will search stuff in the virtual environment if executed on the project folder. 

E.g. to start a python3 interpreter using the one from the virtual environment:

```shell
pdm run python3
```

You can also activate the environment manually if needed.

In the root directory:

```shell
eval $(pdm venv activate)
```

---

### Run tests

To run the tests, use: 

```shell
pdm run pytest
``` 

### Building

Use: 

```shell
pdm build
```

to generate a wheel distribution (.whl) file and associated tar.gz.

---

### Run the PDM scripts defined for this project

For commands specified in the `tool.pdm.scripts` subsection of `pyproject.toml` you can run them in two ways.

The same way you run a command:

```shell
pdm name-of-the-script
```

or

```shell
pdm run name-of-the-script
```

(e.g. if your script may collide with a specified pdm command)

#### Ruff & Pyright

Just the checks (used e.g. in CI):

```shell
pdm check
```

or with automated ruff fixes:

```shell
pdm checkfix
```

#### Docs

To rebuild docs do:

```shell
pdm builddocs
```

---

### Listing installed packages

To list packages installed (including transitive) in the current enviroenment, use: 

```shell
pdm list
```

### Installing this a as package using PIP

A PDM project is a valid pip package.

If you need to install it using pip, use: 

```shell
pip install /yourprojectfolder
```
or for editable installs

```shell
pip install -e /yourprojectfolder
```

--- 

### Adding (and removing) dependencies 

You can add new dependencies with `pdm add` and remove them with `pdm remove`

Dependencies should be divided in:
- main package dependencies, e.g. things your main code depends on
- dev/test/other dependencies, e.g. like pytest, locust, mkdocs, ruff, etc

We use a ficticious package called "some-dependency-name" in the examples bellow.

#### Adding Dependencies Manually

For multiple packages it's probably easier to edit the `pyproject.toml` file directly.

Remember to update the lock afterwards:

```shell
pdm lock
```

#### Add package deps to the project

```shell
pdm add "some-dependency-name" 
```

which will use the latest version that works with other deps and add it in `pyproject.toml`.


#### Add package deps using [PEP-508](https://peps.python.org/pep-0508/) style version strings 

Use:

```shell
pdm add "some-dependency-name>=1.3.2,<2.0.0"
```
which will fail if the chosen version constraint is not compatible with other dependencies.

This is generally recommended to avoid surprises (or use =~).

#### Add package deps from git repository using tags or commmit strings

```shell
pdm add "pip @ git+https://github.com/some/repo.git@TAGX.Y"
```  

#### Add package deps from local folders

Folder must contain a valid pip project.

```shell
pdm add ./sub-package
```  

#### Add package deps from local whl files

```shell
pdm add ./first-1.0.0-py2.py3-none-any.whl
```  

#### Add other deps to a dependency group

```shell
pdm add -G dev "some-dev-dependency-name>=1.3.2,<2.0.0"
```

#### Remove main package dependency

Use:

```shell
pdm remove some-dev-dependency-name
```


#### Remove dependency from group

Use: 
```shell
pdm remove -G dev some-dev-dependency-name
```


---

## Create your own project

Just create a project for the folder and use init:

```shell
mkdir my-awesome-project
cd my-awesome-project
pdm init
```

and follow the steps.

See more info in [https://pdm-project.org/latest/usage/project/.](https://pdm-project.org/latest/usage/project/)

It already creates .gitignore and a simple pyproject.toml.

---

## Using this Example Project

### Define The model

```python

import datetime
from typing import Any
from pydantic import BaseModel
from pydantic.networks import AnyUrl, IPvAnyAddress

import base_model_io

class Section1(BaseModel):
    some_url: AnyUrl
    some_ipv4: IPvAnyAddress
    some_ipv6: IPvAnyAddress
    some_date: datetime.datetime
    some_list: list[Any]
    some_bool: bool

class Section2(BaseModel):
    some_float: float | None = None
    some_int: int | None = None

class Section3(BaseModel):
    list_of_lists: list[list[Any]]

class TestToml(base_model_io.TomlBaseModel):
    some_title: str
    some_int: int
    some_float: float
    section1: Section1
    section2: dict[str, Section2]
    section3: Section3

class TestYaml(base_model_io.YamlBaseModel):
    some_title: str
    some_int: int
    some_float: float
    section1: Section1
    section2: dict[str, Section2]
    section3: Section3
```

### TOML

#### Use the TOML loader 
```
TestToml.from_toml("./some.toml")
```

#### Use the TOML writer 
```
my_toml_model_instance = TestToml(...)
my_toml_model_instance.to_toml("./some_other.toml")
```

### YAML

#### Use the YAML loader 
```
TestYaml.from_yaml("./some.yaml")
```

#### Use the YAML writer 
```
my_toml_model_instance = TestYaml(...)
my_yaml_model_instance.to_yaml("./some_other.yaml")
```