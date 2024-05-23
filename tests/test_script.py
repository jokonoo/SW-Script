import os

import pytest

from source.script import start_script, load_data, OUTPUT_PATH
import unittest.mock as mock

from source.exceptions import ZeroCountException
from tests.conftest import mock_script_run_data as mock_data_values


class TestScript:

    def teardown_method(self):
        if os.path.exists(OUTPUT_PATH):
            os.remove(OUTPUT_PATH)

    @mock.patch("source.script.load_data", side_effect=mock_data_values)
    def test_start_script(self, load_data_mock):
        interval_time_value = 0
        start_script(interval_time_value)

    @mock.patch("source.script.COUNT_OF_PEOPLE_AND_PLANET", 0)
    def test_start_script_with_0_count(self):
        interval_time_value = 0
        with pytest.raises(ZeroCountException):
            start_script(interval_time_value)

    @mock.patch("requests.get")
    def test_load_data_planet(self, api_response_mock):
        return_data = {"name": "test_planet", "terrain": "test_terrain"}
        api_response_mock.return_value.json.return_value = return_data
        assert load_data("planet") == return_data

    @mock.patch("requests.get")
    def test_load_data_person(self, api_response_mock):
        return_data = {"name": "test_person", "height": 160}
        api_response_mock.return_value.json.return_value = return_data
        assert load_data("person") == return_data



