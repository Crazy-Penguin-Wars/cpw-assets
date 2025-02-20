import json

with open("test.lvl", "r") as file:
    data = json.load(file)

for i in data["elements"]:
    for j in i["points"]:
        j["x"] = j["x"] * 1.7561
        j["y"] = j["y"] * 1.7561

with open("test.lvl", "w") as file:
    json.dump(data, file, indent=4)