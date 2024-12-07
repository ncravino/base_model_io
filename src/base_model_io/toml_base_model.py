"""Implementation of TOMLBaseModel."""

from pathlib import Path

import tomli
import tomli_w
from pydantic import BaseModel


class TomlBaseModel(BaseModel):
    """Extension of Pydantic BaseModel with TOML loader and dumper."""

    @classmethod
    def from_toml(cls, toml_file_path: Path) -> "TomlBaseModel":
        """Create an instance of this TomlBaseModel from a TOML file.

        Args:
            toml_file_path (Path): the toml file path

        Returns:
            TomlBaseModel: An instance of this TomlBaseModel

        """
        toml_dict = tomli.loads(Path(toml_file_path).read_text())
        return cls(**toml_dict)

    def to_toml(self, toml_file_path: Path) -> None:
        """Write this TomlBaseModel to a file.

        Args:
            toml_file_path (Path): the toml file path

        """
        Path(toml_file_path).write_text(
            #                                     No None/Null in TOML Spec
            tomli_w.dumps(self.model_dump(mode="json", exclude_none=True))
        )
