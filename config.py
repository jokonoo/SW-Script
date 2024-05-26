import json
import os

from source.exceptions import NarrowRangeException, TooHighCountException

with open('config.json') as config_file:
    config_data = json.load(config_file)

OUTPUT_PATH = config_data['output_path']
if not os.path.exists(OUTPUT_PATH):
    OUTPUT_PATH = os.getcwd()

OUTPUT_PATH: str = os.path.join(OUTPUT_PATH, 'data.yaml')
PLANET_RANGE: int = config_data["max_planets"]
PERSON_RANGE: int = config_data["max_person"]
COUNT_OF_PEOPLE_AND_PLANET: int = config_data["count_of_people_and_planet"]

if COUNT_OF_PEOPLE_AND_PLANET > PLANET_RANGE or COUNT_OF_PEOPLE_AND_PLANET > PERSON_RANGE:
    raise NarrowRangeException(
        "RANGES OF PLANET (1-60) AND PERSON (1-82) NEEDS TO BE HIGHER THAN COUNT OF PEOPLE AND PLANET VARIABLE")

elif COUNT_OF_PEOPLE_AND_PLANET > 60:
    raise TooHighCountException("VALUE COUNT_OF_PEOPLE_AND_PLANET CANT BE HIGHER THAN 60")
