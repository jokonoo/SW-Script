import pytest

people_url = "http://www.people.com"
planets_url = "http://www.planets.com"
mock_request_data = []


for n in range(0, 10):
    mock_request_data.append([
        (people_url, {"name": f"test_run{n}", "height": "test_data"}),
        (planets_url, {"name": f"test_run{n}", "terrain": "test_data"})
    ])

mock_yaml_data = {"people": [{"name": f"test_run{n}", "height": "test_data"} for n in range(0, 10)],
                  "planets": [{"name": f"test_run{n}", "terrain": "test_data"} for n in range(0, 10)]}
