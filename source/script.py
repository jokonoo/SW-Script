import asyncio
import aiohttp
import logging
import random

import yaml

from source.exceptions import IncorrectURLException, MissingDataTypeException, ZeroCountException
from source.config import config_data, PLANET_RANGE, PERSON_RANGE, OUTPUT_PATH, COUNT_OF_PEOPLE_AND_PLANET

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()])


async def load_url(data_type, session):
    if data_type == "planets":
        random_number = random.randint(1, PLANET_RANGE)
    elif data_type == "people":
        random_number = random.randint(1, PERSON_RANGE)
    try:
        return await session.get(f"http://swapi.dev/api/{data_type}/{random_number}/")
    except NameError:
        raise MissingDataTypeException("Provided data type does not exist")


async def load_async_tasks(session):
    tasks = []
    for data_type in ["people", "planets"]:
        tasks.append(asyncio.create_task(load_url(data_type, session)))
    responses = await asyncio.gather(*tasks)
    return [(str(response.url), await response.json()) for response in responses]


def load_data_from_request(url, response_data):
    if "planets" in url:
        return {"name": response_data["name"], "terrain": response_data["terrain"]}
    elif "people" in url:
        return {"name": response_data["name"], "height": response_data["height"]}
    raise IncorrectURLException("Incorrect URL address")


def load_yaml_data():
    with open(OUTPUT_PATH, 'r') as outfile:
        return yaml.safe_load(outfile)


def yaml_data_lengths(data_type):
    return len(load_yaml_data()[data_type])


def update_data(data_type, data):
    cur_yaml = load_yaml_data()
    for item in cur_yaml[data_type]:
        if item["name"] == data["name"]:
            logging.info(f"{data_type} object already in output file: {data}")
            return
    cur_yaml[data_type].append(data)

    if cur_yaml:
        with open(OUTPUT_PATH, 'w') as outfile:
            yaml.safe_dump(cur_yaml, outfile, sort_keys=False)


async def add_data(session, first_iteration=False):
    new_person_request, new_planet_request = await load_async_tasks(session)
    new_person_data = load_data_from_request(*new_person_request)
    new_planet_data = load_data_from_request(*new_planet_request)
    if first_iteration:
        logging.info(f"OUTPUT PATH IS {OUTPUT_PATH}")
        with open(OUTPUT_PATH, 'w') as outfile:
            yaml.safe_dump({"people": [new_person_data], "planets": [new_planet_data]}, outfile, sort_keys=False)
        return
    cur_yaml = load_yaml_data()
    if len(cur_yaml["people"]) < COUNT_OF_PEOPLE_AND_PLANET:
        update_data("people", new_person_data)
    if len(cur_yaml["planets"]) < COUNT_OF_PEOPLE_AND_PLANET:
        update_data("planets", new_planet_data)


async def start_script(interval_time_value):
    logging.info(f"CONFIGURATION VARIABLES: {config_data}")
    if COUNT_OF_PEOPLE_AND_PLANET > 0:
        async with aiohttp.ClientSession() as session:
            await add_data(first_iteration=True, session=session)
            load_yaml_data()
            while not (yaml_data_lengths("planets") == COUNT_OF_PEOPLE_AND_PLANET and yaml_data_lengths(
                    "people") == COUNT_OF_PEOPLE_AND_PLANET):
                await add_data(session=session)
                await asyncio.sleep(interval_time_value)
            logging.info("Script finished")
    else:
        raise ZeroCountException("Count of people and planets is lower than 1")
