import json
import items
import urllib3
import logging.config
import argparse
import utils
import jsonschema


def build_item_list(config, filters):
    if filters:
        return [items.LoggingItem(spec) for spec in config.get("items", []) if spec["name"] in filters]
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
    schema = utils.load_json_schema("schemas/main.json")
    with open(config_file, "r") as f:
        config = json.load(f)
    jsonschema.validate(instance=config, schema=schema)
    return config


def download_all(item_list, skip=False):
    for item in item_list:
        item.download_new_elements(skip)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Simple downloader script. Check any source and download any new "
                    "item found")
    parser.add_argument("--logConfig", default="log_config.json",
                        help="Specify the logging configuration file")
    parser.add_argument("--config", default="config.json",
                        help="Specify the downloader config file to use")
    parser.add_argument("-n", "--noDownload", action="store_true",
                        help="Skip the download step for any new content found, "
                             "but still update the caches. This is useful to re-align "
                             "the caches in case all the new items have been "
                             "downloaded manually")
    parser.add_argument("-f", "--filter", default=[], action="append",
                        help="Only run the script for the items having the specified "
                             "name. This option can be provided multiple times to "
                             "filter by more than one item name")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    load_log_config(args.logConfig)
    config = load_config(args.config)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    item_list = build_item_list(config, args.filter)
    logging.info("start processing items")

    if args.noDownload:
        logging.warning("option --noDownload active: downloaders will not actually "
                        "download anything, but caches will be updated as usual")

    download_all(item_list, skip=args.noDownload)

    logging.info("done.")
