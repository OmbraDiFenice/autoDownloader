import requests


def get_standard_xml():
    with open("tests/data/providers/rss/sample.xml", "rb") as f:
        xml = f.read()
    response = requests.Response()
    response._content = xml
    return response
