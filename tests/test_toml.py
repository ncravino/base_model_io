import datetime
import os
from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from typing import Any

from pydantic import AnyUrl, BaseModel
from pytest import fixture

import base_model_io

test_toml_dict = {
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
def TestToml():
    class Section1(BaseModel):
        some_url: AnyUrl
        some_ipv4: IPv4Address
        some_ipv6: IPv6Address
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

    return TestToml


def test_toml_read(TestToml):
    test_toml = TestToml.from_toml(Path(__file__).parent / "test.toml")
    assert test_toml.model_dump() == test_toml_dict


@fixture
def write_toml():
    write_toml = Path(__file__).parent / "test_write.toml"
    yield write_toml
    os.remove(write_toml)


def test_toml_write(TestToml, write_toml):
    test_toml = TestToml(**test_toml_dict)
    test_toml.to_toml(write_toml)

    test_toml_read = TestToml.from_toml(write_toml)
    assert test_toml_read.model_dump() == test_toml_dict
