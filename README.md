# Pydantic BaseModels extended with TOML and YAML loaders.

Very simple subclasses that just add TOML and YAML loaders to [Pydantic BaseModel](https://docs.pydantic.dev/latest/).

Uses [PyYaml](https://pyyaml.org/) for YAML and [tomli](https://github.com/hukkin/tomli) and [tomli-w](https://github.com/hukkin/tomli-w) for TOML.

## Example 

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

# We can inherit just from:
# TomlBaseModel for TOML
# YamlBaseModel for YAML
class TestToml(base_model_io.TomlBaseModel, base_model_io.YamlBaseModel):
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
TestToml.to_toml("./some_other.toml")
```

### YAML

#### Use the YAML loader 
```
TestYaml.from_yaml("./some.yaml")
```

#### Use the YAML writer 
```
TestYaml.to_yaml("./some_other.yaml")