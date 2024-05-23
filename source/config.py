import json

with open('../config.json') as config_file:
    config_data = json.load(config_file)

OUTPUT_PATH = f"{config_data['output_path']}\\data.yaml"
PLANET_RANGE = config_data["max_person"]
PERSON_RANGE = config_data["max_planets"]
COUNT_OF_PEOPLE_AND_PLANET = config_data["count_of_people_and_planet"]