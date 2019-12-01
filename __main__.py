import json
import items
import urllib3
import sys
import logging.config

log_conf = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}
try:
    with open("log_config.json", "r") as f:
        log_conf = json.load(f)
except IOError:
    pass
logging.config.dictConfig(log_conf)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"
with open(config_file, "r") as f:
    config = json.load(f)

item_list = [items.LoggingItem(spec) for spec in config.get("items", [])]

logging.info("start processing items")

for item in item_list:
    item.download_new_elements()

logging.info("done.")
