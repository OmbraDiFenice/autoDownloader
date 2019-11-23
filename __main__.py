import json
import items
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"
with open(config_file, "r") as f:
    config = json.load(f)

item_list = [items.Item(spec) for spec in config.get("items", [])]

for item in item_list:
    item.download_new_elements()
