import requests


def get_standard_xml():
    with open("tests/data/providers/rss/sample.xml", "rb") as f:
        xml = f.read()
    response = requests.Response()
    response._content = xml
    return response


def get_standard_html():
    with open("tests/data/providers/html/sample.html", "rb") as f:
        html = f.read()
    response = requests.Response()
    response._content = html
    return response


def get_binary_file(*args, **kwargs):
    with open("tests/data/downloaders/sample_binary_data.zip", "rb") as f:
        data = f.read()
    response = requests.Response()
    response._content = data
    return response
