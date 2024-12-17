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

""" def __main__():

    input_configuration = InputConfiguration()
    input_configuration.xyz_rank = [2,3,4,5,6]
    input_configuration.fusion_level =  [2,3,4,5,6]
    write_config(input_configuration)
    print (read_config().fusion_level,read_config().xyz_rank)
__main__() 
"""