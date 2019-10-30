import json
import requests
from typing import List
from .models.cvm import CVM


class stock_cvm_code():
    service_url: str = ""

    def __init__(self, url):
        self.service_url = url
        pass

    def get_list(self) -> List[CVM]:
        
        return_lst: List[CVM] = []
        aux_list = []
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

            try:
                if aux_list.index(cvm_obj.cvm_code) > 0:
                    pass
                pass
            except ValueError:
                return_lst.append(cvm_obj)
                aux_list.append(cvm_obj.cvm_code)
                pass               

        return return_lst
    pass