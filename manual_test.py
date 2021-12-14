from requests import post
from json import dumps

url = "http://127.0.0.1:5000/"

valid_grid = [
    ["R","R","B","-","B","B","B","-"],
    ["B","R","B","B","B","B","-","-"],
    ["B","R","B","B","R","R","-","B"],
    ["R","R","R","-","-","R","R","R"],
    ["B","B","B","R","-","-","-","B"],
    ["-","R","B","B","B","B","-","B"],
    ["R","B","-","B","R","B","-","R"],
    ["B","R","-","R","B","-","-","-"]
]

invalid_grid = [
    ["B","R","B","B","B","B","-","-"],
    ["B","R","B","B","R","R","-","B"],
    ["R","R","R","-","-","R","R","R"],
    ["B","B","B","R","-","-","-","B"],
    ["-","R","B","B","B","B","-","B"],
    ["R","B","-","B","R","B","-","R"],
    ["B","R","-","R","B","-","-","-"]
]

invalid_json = '{ "test": "0", this: "that" }'

print("==================================================")
print("Posting valid JSON to API:")
valid_grid_test = post(url=url, data=dumps(valid_grid))

if valid_grid_test.status_code == 200:
    print("Test successful! Results from API:")
    for result in valid_grid_test.json():
        print(result)
else:
    print("Test failed with unexpected result:")
    print(valid_grid_test.status_code,valid_grid_test.text)

print("==================================================")
print("Posting invalid JSON to API:")
invalid_json_test = post(url=url, data=invalid_json)
if invalid_json_test.status_code == 400:
    print("Test successful! Results from API:")
    print(invalid_json_test.json())
else:
    print("Test failed with unexpected result:")
    print(invalid_json_test.status_code,invalid_json_test.text)

print("==================================================")
print("Posting invalid grid to API:")
invalid_grid_test = post(url=url, data=dumps(invalid_grid))

if invalid_grid_test.status_code == 400:
    print("Test successful! Results from API:")
    print(invalid_grid_test.json())
else:
    print("Test failed with unexpected result:")
    print(invalid_grid_test.status_code,invalid_grid_test.text)

print("==================================================")
