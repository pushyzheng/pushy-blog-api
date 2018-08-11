# encoding:utf-8
import requests

headers = {
    'Content-Type': 'text/plain'
}
content = "## Hello World"
resp = requests.post("https://api.github.com/markdown/raw", content, headers=headers).text