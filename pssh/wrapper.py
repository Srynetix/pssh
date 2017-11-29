"""pssh utility wrappers."""

from pssh.exceptions import MissingKeyError

from pssh.config import (
    load_configuration_file,
    extract_machine_hierarchy,
    get_user_configuration_path
)


def list_machines(path_to_file):
    """
    List machines.

    :param path_to_file     Path to file (str?)
    :return Machine names (iterable)
    """
    if not path_to_file:
        path_to_file = get_user_configuration_path()

    config = load_configuration_file(path_to_file)
    hierarchy = extract_machine_hierarchy(config)

    return hierarchy["machines"].keys()


def get_machine_configuration(path_to_file, config_name):
    """
    Get machine configuration.

    :param path_to_file     Path to file (str?)
    :param config_name      Config name (str):
    :return Machine configuration (dict)
    """
    if not path_to_file:
        path_to_file = get_user_configuration_path()

    config = load_configuration_file(path_to_file)
    hierarchy = extract_machine_hierarchy(config)

    if config_name not in hierarchy["machines"]:
        raise MissingKeyError(
            "Missing `{0}` name in machines configuration.".format(config_name))

    return hierarchy["machines"][config_name]
