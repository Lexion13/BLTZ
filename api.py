import json
import requests

COINS_LIST_GET_URL = "https://min-api.cryptocompare.com/data/all/coinlist"
COINS_DETAIL_GET_URL = "https://min-api.cryptocompare.com/data/pricemultifull"


def get_list_all():
    coins_list_json = json.loads(requests.get(COINS_LIST_GET_URL).text)
    if coins_list_json['Response'] == 'Error':
        return False
    else:
        return coins_list_json


def get_details(fsyms, tsyms):
    details_api = COINS_DETAIL_GET_URL+"?fsyms={fsyms}&tsyms={tsyms}"
    details_url = details_api.format(fsyms=fsyms, tsyms=tsyms)
    details_data = json.loads(requests.get(details_url).text)
    for key in details_data:
        if key == 'Response':
            if details_data['Response'] == 'Error':
                return False

    return details_data['DISPLAY']


