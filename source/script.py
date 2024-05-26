import asyncio
import aiohttp
from typing import Any
import logging
import random

import yaml

from source.exceptions import IncorrectURLException, MissingDataTypeException, ZeroCountException
from config import config_data, PLANET_RANGE, PERSON_RANGE, OUTPUT_PATH, COUNT_OF_PEOPLE_AND_PLANET

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()])


async def load_url(data_type: str, session: aiohttp.ClientSession) -> Any:
    if data_type == "planets":
        random_number = random.randint(1, PLANET_RANGE)
    elif data_type == "people":
        random_number = random.randint(1, PERSON_RANGE)
    try:
        return await session.get(f"http://swapi.dev/api/{data_type}/{random_number}/")
    except NameError:
        raise MissingDataTypeException("Provided data type does not exist")


async def load_async_tasks(session: aiohttp.ClientSession) -> list[tuple[str, dict]]:
    tasks = []
    for data_type in ["people", "planets"]:
        tasks.append(asyncio.create_task(load_url(data_type, session)))
    responses = await asyncio.gather(*tasks)
    return [(str(response.url), await response.json()) for response in responses]


def load_data_from_response(response_data: dict, data_type: str):
    if data_type == "height":
        return 0 if not response_data.get(data_type) or response_data.get(data_type) == "unknown" else int(
            response_data.get(data_type))
    return response_data.get(data_type) if response_data.get(data_type) else "unknown"


def load_data_from_request(url: str, response_data: dict) -> dict:
    if "planets" in url:
        return {"name": load_data_from_response(response_data, "name"),
                "terrain": load_data_from_response(response_data, "terrain")}
    elif "people" in url:
        return {"name": load_data_from_response(response_data, "name"),
                "height": load_data_from_response(response_data, "height")}
    raise IncorrectURLException("Incorrect URL address")


def load_yaml_data() -> dict:
    with open(OUTPUT_PATH, 'r') as outfile:
        return yaml.safe_load(outfile)


def yaml_data_lengths(data_type: str) -> int:
    return len(load_yaml_data()[data_type])


def update_data(data_type: str, data: dict) -> None:
    cur_yaml = load_yaml_data()
    for item in cur_yaml[data_type]:
        if item["name"] == data["name"]:
            logging.warning(f"{data_type} object already in output file: {data}")
            return
    cur_yaml[data_type].append(data)
    logging.info(f"Adding type: {data_type} to output file: {data}")

    if cur_yaml:
        try:
            with open(OUTPUT_PATH, 'w') as outfile:
                yaml.safe_dump(cur_yaml, outfile, sort_keys=False)
        except FileNotFoundError as e:
            logging.error(e)


async def add_data(session: aiohttp.ClientSession, first_iteration: bool = False) -> None:
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


async def start_script(interval_time_value: int) -> None:
    logging.info(f"CONFIGURATION VARIABLES: {config_data}")
    if COUNT_OF_PEOPLE_AND_PLANET > 0:
        async with aiohttp.ClientSession() as session:
            await add_data(first_iteration=True, session=session)

            while not (yaml_data_lengths("planets") == COUNT_OF_PEOPLE_AND_PLANET and yaml_data_lengths(
                    "people") == COUNT_OF_PEOPLE_AND_PLANET):
                await add_data(session=session)
                await asyncio.sleep(interval_time_value)
            logging.info("Script finished")
    else:
        raise ZeroCountException("Count of people and planets is lower than 1")
