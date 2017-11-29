"""pssh config loading."""

import os

import yaml
import six

from pssh.exceptions import BadKeyNameError, MissingKeyError

if six.PY2:
    from io import open


def get_user_configuration_path():
    """
    Get the config path for the current user.

    :rtype: Path to the config file (str)
    """
    return os.path.normpath(os.path.expanduser("~/.pssh/config.yml"))


def load_configuration_file(path_to_file):
    """
    Load a pssh configuration file.

    :param path_to_file     Path to file (str)
    :return Configuration data (dict)
    """
    if not os.path.isfile(path_to_file):
        raise RuntimeError("File `{0}` does not exist.".format(path_to_file))

    with open(path_to_file, mode="rt", encoding="utf-8") as handle:
        file_content = handle.read()

    return load_configuration_content(file_content)


def load_configuration_content(file_content):
    """
    Load a pssh configuration content.

    :param file_content     File content (str)
    :return Configuration data (dict)
    """
    try:
        dict_content = yaml.load(file_content)
    except Exception:
        raise RuntimeError("Bad YAML file.")

    return dict_content


def extract_machine_hierarchy(config_dict):
    """
    Extract machines from configuration dict.

    :param config_dict  Configuration dict (dict)
    :return Machine hierarchy (dict)
    """
    default_values = _extract_default_configurations(config_dict)
    machines = _extract_machine_configurations(config_dict)
    configured_machines = apply_default_configurations(machines, default_values)

    return {
        "default_values": default_values,
        "machines": configured_machines
    }


def fetch_default_values_for_name(default_values, config_name):
    """
    Fetch the default values for a config name.

    :param default_values   Default values (dict)
    :param config_name      Configuration name (str)
    """
    default_keys = default_values.keys()
    split_parent_names = config_name.split(":")[:-1]

    current_values = {}
    current_parent = ""

    # Fetch global defaults
    if "" in default_keys:
        current_values = default_values[""]

    # Check for each namespaces
    for parent in split_parent_names:
        # Compute parent name
        if current_parent == "":
            current_parent = parent
        else:
            current_parent = ":".join((current_parent, parent))

        if current_parent in default_keys:
            values = default_values[current_parent]
            current_values.update(values)

    return current_values


def apply_default_configurations(machines, default_values):
    """
    Apply default configurations to machines.

    :param machines         Machine configurations (dict)
    :param default_values   Default values (dict)
    :return New machine configurations (dict)
    """
    new_machines = {}

    for config_name in machines:
        new_machine_config = {}
        default_config = fetch_default_values_for_name(default_values, config_name)
        current_machine_config = machines[config_name]

        new_machine_config.update(default_config)
        new_machine_config.update(current_machine_config)
        new_machines[config_name] = new_machine_config

    return new_machines


def _extract_machine_configurations(config_dict):
    if "machines" not in config_dict:
        raise MissingKeyError("Missing 'machines' key in configuration.")

    machines = config_dict["machines"]
    return dict(_extract_definition_keys("", machines))


def _extract_default_configurations(config_dict):
    if "defaults" not in config_dict:
        return {}

    defaults = config_dict["defaults"]
    return dict(_extract_definition_keys("", defaults))


def _extract_definition_keys(parent_key, current_dict):
    keys = current_dict.keys() if current_dict else []
    extract = []

    if len(keys) > 0:
        # Values
        if "_values" in keys:
            values = current_dict["_values"]
            extract.append((parent_key, values))

        # Child keys
        for key in [k for k in keys if k != "_values"]:
            if ":" in key:
                raise BadKeyNameError("Character ':' not allowed.")

            current_key_name = key
            if parent_key != "":
                current_key_name = ":".join((parent_key, key))

            results = _extract_definition_keys(current_key_name, current_dict[key])
            for result in results:
                extract.append(result)

    return extract
