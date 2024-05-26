people_url = "http://www.people.com"
planets_url = "http://www.planets.com"
# mock_request_data = []
#
#
# for n in range(0, 10):
#     mock_request_data.append([
#         (people_url, {"name": f"test_run{n}", "height": 1+n*10}),
#         (planets_url, {"name": f"test_run{n}", "terrain": "test_data"})
#     ])
mock_request_data = [[(people_url, {"name": f"test_run{n}", "height": 1 + n * 10}),
                      (planets_url, {"name": f"test_run{n}", "terrain": "test_data"})]
                     for n in range(0, 10)]

mock_yaml_data = {"people": [{"name": f"test_run{n}", "height": 1 + n * 10} for n in range(0, 10)],
                  "planets": [{"name": f"test_run{n}", "terrain": "test_data"} for n in range(0, 10)]}
