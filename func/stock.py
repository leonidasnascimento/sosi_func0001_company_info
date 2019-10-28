import json
import requests
from .models.cvm import CVM

class stock_cvm_code():
    service_url: str = ""

    def __init__(self, url):
        self.service_url = url
        pass

    def get_list(self) -> []:
        
        return_lst = []
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

        resp: requests.Response = requests.request("GET", self.service_url, headers=headers)

        if not resp:
            return []
        
        json_resp_list = json.loads(resp.content)

        for item in json_resp_list:
            cvm_obj = CVM("", "")
            cvm_obj.__dict__ = item

            return_lst.append(cvm_obj)

        return return_lst
    pass