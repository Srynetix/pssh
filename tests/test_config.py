# pylama:ignore=D103

"""Tests."""

import pytest

from pssh.exceptions import BadKeyNameError

from pssh.config import (
    load_configuration_content,
    extract_machine_hierarchy,
    fetch_default_values_for_name,
    apply_default_configurations
)


def test_empty_defaults():
    str_content = """
defaults:
machines:
"""

    configuration = load_configuration_content(str_content)
    hierarchy = extract_machine_hierarchy(configuration)

    assert len(hierarchy["default_values"].keys()) == 0


def test_not_empty_defaults():
    str_content = """
machines:
defaults:
    values:
        user: pouet
    one:
        two:
            values:
                user: pouet
                port: 5555
            five:
                values:
                    port: 5566
        values:
            port: 4455
    three:
        values:
    four:
"""

    configuration = load_configuration_content(str_content)
    hierarchy = extract_machine_hierarchy(configuration)

    default_values = hierarchy["default_values"]
    assert "" in default_values
    assert "one" in default_values
    assert "three" in default_values
    assert "one:two" in default_values
    assert "one:two:five" in default_values
    assert "four" not in default_values


def test_defaults_error():
    str_content = """
machines:
defaults:
    values:
        user: pouet
    one:pouet:
        values:
            user: hello
"""

    configuration = load_configuration_content(str_content)
    with pytest.raises(BadKeyNameError):
        extract_machine_hierarchy(configuration)


def test_defaults_values():
    values = {
        "": {"user": "hello", "port": 22},
        "coucou": {"port": 23},
        "coucou:hello": {"port": 24}
    }

    defs = fetch_default_values_for_name(values, "coucou")
    assert defs["user"] == "hello"
    assert defs["port"] == 22

    defs = fetch_default_values_for_name(values, "coucou:pouet")
    assert defs["user"] == "hello"
    assert defs["port"] == 23

    defs = fetch_default_values_for_name(values, "coucou:hello")
    assert defs["user"] == "hello"
    assert defs["port"] == 23

    defs = fetch_default_values_for_name(values, "coucou:hello:one")
    assert defs["user"] == "hello"
    assert defs["port"] == 24


def test_machine_configurations():
    defaults = {
        "": {"user": "hello"},
        "coucou": {"port": 23}
    }

    machines = {
        "coucou": {"port": 22},
        "coucou:hello": {"ip": "127.0.0.1"}
    }

    configured_machines = apply_default_configurations(machines, defaults)
    assert configured_machines["coucou"].get("port") == 22
    assert configured_machines["coucou"].get("user") == "hello"
    assert configured_machines["coucou:hello"].get("user") == "hello"
    assert configured_machines["coucou:hello"].get("port") == 23
    assert configured_machines["coucou:hello"].get("ip") == "127.0.0.1"
