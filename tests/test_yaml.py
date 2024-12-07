import datetime
import os
from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from typing import Any

from pydantic import AnyUrl, BaseModel
from pytest import fixture

import base_model_io

test_yaml_dict = {
    "some_title": "TOML test",
    "some_int": 1,
    "some_float": 2.0,
    "section1": {
        "some_url": AnyUrl("http://example.com/"),
        "some_ipv4": IPv4Address("192.168.1.1"),
        "some_ipv6": IPv6Address("2001:0:130f::9c0:876a:130b"),
        "some_date": datetime.datetime(
            1985,
            8,
            27,
            12,
            32,
            tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
        ),
        "some_list": ["str1", "str2", "str3"],
        "some_bool": True,
    },
    "section2": {
        "first": {"some_float": None, "some_int": 1},
        "second": {"some_float": 2.0, "some_int": None},
    },
    "section3": {"list_of_lists": [["abc", "defg"], [1, 2]]},
}


@fixture(scope="module")
def TestYaml():
    class Section1(BaseModel):
        some_url: AnyUrl
        some_ipv4: IPv4Address
        some_ipv6: IPv6Address
        some_date: datetime.datetime
        some_list: list[Any]
        some_bool: bool

    class Section2(BaseModel):
        some_float: float | None
        some_int: int | None = None

    class Section3(BaseModel):
        list_of_lists: list[list[Any]]

    class TestYaml(base_model_io.YamlBaseModel):
        some_title: str
        some_int: int
        some_float: float
        section1: Section1
        section2: dict[str, Section2]
        section3: Section3

    return TestYaml


def test_yaml_read(TestYaml):
    test_yaml = TestYaml.from_yaml(Path(__file__).parent / "test.yaml")
    assert test_yaml.model_dump() == test_yaml_dict


@fixture
def write_yaml():
    write_yaml = Path(__file__).parent / "test_write.yaml"
    yield write_yaml
    os.remove(write_yaml)


def test_yaml_write(TestYaml, write_yaml):
    test_yaml = TestYaml(**test_yaml_dict)
    test_yaml.to_yaml(write_yaml)

    test_yaml_read = TestYaml.from_yaml(write_yaml)
    assert test_yaml_read.model_dump() == test_yaml_dict
