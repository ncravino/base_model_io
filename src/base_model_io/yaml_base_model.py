"""Implementation of YAMLBaseModel."""

from pathlib import Path

import yaml
from pydantic import BaseModel


class YamlBaseModel(BaseModel):
    """Extension of Pydantic BaseModel with YAML loader and dumper."""

    @classmethod
    def from_yaml(cls, yaml_file_path: Path) -> "YamlBaseModel":
        """Create an instance of this YamlBaseModel from a YAML file.

        Args:
            yaml_file_path (Path): the .yaml file path

        Returns:
            YamlBaseModel: An instance of this YamlBaseModel

        """
        yaml_dict = yaml.safe_load(Path(yaml_file_path).read_text())
        return cls(**yaml_dict)

    def to_yaml(self, yaml_file_path: Path) -> None:
        """Write this YamlBaseModel to a file.

        Args:
            yaml_file_path (Path): the .yaml file path

        """
        with open(yaml_file_path, "w") as yaml_f_w:
            yaml.safe_dump(self.model_dump(mode="json"), yaml_f_w)
