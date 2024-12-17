"""
Module providing functions anc classes for parsing configuration ini files
"""
import configparser
from dataclasses import dataclass
from typing import List

CONFIGURATION_NAME = 'configurations.ini'
FUSION_LEVELS = 'fusion_levels'
XYZ_RANKS = 'xyz_ranks'
INPUT = 'INPUT'

@dataclass
class InputConfiguration:
    """
    Class representing the parsing result of configurations
    """
    fusion_levels = List[int]
    xyz_ranks = List[int]
    banished_fusion_levels = List[int]
    banished_xyz_ranks = List[int]


def read_config(config_file_location=CONFIGURATION_NAME):
    """
    Function for reading configuration file
    """
    res = InputConfiguration()
    config = configparser.ConfigParser()
    with open(config_file_location, 'r', encoding="utf-8") as file:
        config.read_string(file.read())

    fusion_levels = list[int](map(int, config[INPUT][FUSION_LEVELS].split()))
    xyz_ranks = list[int](map(int, config[INPUT][XYZ_RANKS].split()))
    extra_deck_size = len(fusion_levels) + len(xyz_ranks) * 2

    assert extra_deck_size <= 15, \
        f"Extra Deck Size is {extra_deck_size}. It should be <= 15"
    res.fusion_levels = fusion_levels
    res.xyz_ranks = xyz_ranks
    return res


def write_config(input_configuration: InputConfiguration, config_file_location = CONFIGURATION_NAME):
    """
    Funtion to write configuration file
    """
    config = configparser.ConfigParser()
    config.add_section(INPUT)
    config.set(INPUT, FUSION_LEVELS, ' '.join(map(str, input_configuration.fusion_levels)))
    config.set(INPUT, XYZ_RANKS, ' '.join(map(str, input_configuration.xyz_ranks)))


    with open(file=config_file_location, mode='w', encoding='utf-8') as configfile:    # save
        config.write(configfile)
