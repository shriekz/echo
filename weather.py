import requests

ENDPOINT = 'https://query.yahooapis.com/v1/public/yql?q=select%20item.condition%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22chennai%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'

resp = requests.get(ENDPOINT)
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET Weather {}'.format(resp.status_code))
print('Check this')
print('Weather is {}'.format(resp.json()["query"]["results"]["channel"]["item"]["condition"]["text"]))

