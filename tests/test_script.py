import os

import aiohttp
import pytest

from source.script import start_script, load_data_from_request, load_url, OUTPUT_PATH
import unittest.mock as mock

from source.exceptions import IncorrectURLException, MissingDataTypeException, ZeroCountException
from tests.conftest import mock_script_run_data as mock_data_values


class TestScript:

    def teardown_method(self):
        if os.path.exists(OUTPUT_PATH):
            os.remove(OUTPUT_PATH)

    @mock.patch("source.script.load_async_tasks", side_effect=mock_data_values)
    @pytest.mark.asyncio
    async def test_start_script(self, load_data_mock):
        interval_time_value = 0
        await start_script(interval_time_value)

    @mock.patch("source.script.COUNT_OF_PEOPLE_AND_PLANET", 0)
    @pytest.mark.asyncio
    async def test_start_script_with_0_count(self):
        interval_time_value = 0
        with pytest.raises(ZeroCountException):
            await start_script(interval_time_value)

    def test_load_data_from_request_planet(self):
        planet_data = mock_data_values[0][0]
        assert load_data_from_request(*planet_data) == planet_data[1]

    def test_load_data_from_request_people(self):
        people_data = mock_data_values[0][1]
        assert load_data_from_request(*people_data) == people_data[1]

    def test_load_data_from_request_incorrect_url(self):
        incorrect_data = ["http://wrongaddress.com", {"wrong": "data"}]
        with pytest.raises(IncorrectURLException):
            load_data_from_request(*incorrect_data)

    @pytest.mark.asyncio
    async def test_load_url_wrong_data_type(self):
        async with aiohttp.ClientSession() as session:
            with pytest.raises(MissingDataTypeException):
                await load_url("wrong_data_type", session)


    # @mock.patch("requests.get")
    # def test_load_data_person(self, api_response_mock):
    #     return_data = {"name": "test_person", "height": 160}
    #     api_response_mock.return_value.json.return_value = return_data
    #     assert load_data("person") == return_data



