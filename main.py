import json
import items
import urllib3
import logging.config
import argparse


def build_item_list(config):
    return [items.LoggingItem(spec) for spec in config.get("items", [])]


def load_log_config(log_conf_file):
    default_log_conf = {
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
        with open(log_conf_file, "r") as f:
            log_conf = json.load(f)
            logging.config.dictConfig(log_conf)
    except IOError:
        logging.config.dictConfig(default_log_conf)
        logging.warning("unable to load log config from '{}'".format(log_conf_file))


def load_config(config_file="config.json"):
    with open(config_file, "r") as f:
        return json.load(f)


def download_all(item_list, skip=False):
    for item in item_list:
        item.download_new_elements(skip)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--logConfig", default="log_config.json")
    parser.add_argument("--config", default="config.json")
    parser.add_argument("-n", "--noDownload", action="store_true")

    args = parser.parse_args()

    load_log_config(args.logConfig)
    config = load_config(args.config)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    item_list = build_item_list(config)
    logging.info("start processing items")

    if args.noDownload:
        logging.warning("option --noDownload active: downloaders will not actually download anything, but caches "
                        "will be updated as usual")

    download_all(item_list, skip=args.noDownload)

    logging.info("done.")
