import pytest

people_url = "http://www.people.com"
planets_url = "http://www.planets.com"
mock_script_run_data = []


for n in range(0, 10):
    mock_script_run_data.append([
        (planets_url, {"name": f"test_run{n}", "terrain": "test_data"}),
        (people_url, {"name": f"test_run{n}", "height": "test_data"})
    ])
