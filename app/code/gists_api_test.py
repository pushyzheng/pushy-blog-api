# encoding:utf-8
import requests
import json

resp = requests.get('https://api.github.com/users/PushyZqin/gists')

for item in json.loads(resp.text):
    script_base_url = 'https://gist.github.com/PushyZqin/{}.js'
    url = script_base_url.format(item.get('id'))
    print(url)
    print(requests.get(url).text)

    break






