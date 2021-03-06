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


def get_binary_file(name_in_header=True, filename="test_file.zip"):
    def inner_get_binary_file(url, *args, **kwargs):
        with open("tests/data/downloaders/sample_binary_data.zip", "rb") as f:
            data = f.read()
        response = requests.Response()
        if name_in_header:
            response.headers["Content-disposition"] = "filename={}".format(filename)
        response.request = requests.PreparedRequest()
        response.request.url = url
        response._content = data
        response.raw = open("tests/data/downloaders/sample_binary_data.zip", "rb")
        response.close = lambda: response.raw.close()
        return response
    return inner_get_binary_file

