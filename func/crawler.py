import urllib3
import datetime
import requests

from typing import List
from .models.cvm import CVM
from .models.company_info import Company
from bs4 import (BeautifulSoup, Tag)

class company_info():
    def __init__(self):
        pass
    
    def get_info(self, cvm: CVM) -> Company:
        return_obj: Company = Company()

        url_bmf_bovespa = "http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoEmpresaPrincipal.aspx"
        url_bfm_bovespa_domain = "http://bvmf.bmfbovespa.com.br"

        headers = {
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'cache-control': "no-cache",
            'postman-token': "146ba02b-dc25-fb1a-9fbc-a8df1248db26"
        }

        querystring = { 
            "codigoCvm":"{}".format(cvm.cvm_code),
            "idioma":"pt-br"
        }

        res = requests.get(url_bmf_bovespa, headers=headers, params=querystring)
        soup = BeautifulSoup(res.content)

        name_aux: Tag = soup.select_one("h2>span")
        iframe_det: Tag = soup.find_all("iframe")[1]
        
        if not iframe_det:
            return None

        if not iframe_det.has_attr("src"):
            return None

        ## New request for details
        company_det_destination = str(iframe_det["src"]).replace("../", "")
        new_url_bfm_bovespa = url_bfm_bovespa_domain + "/" + company_det_destination
        res = requests.get(new_url_bfm_bovespa, headers=headers)
        soup = BeautifulSoup(res.content)
        
        cnpj_aux: Tag = soup.find("td", text="CNPJ:").find_next_sibling()
        maj_act_aux: Tag = soup.find("td", text="Atividade Principal:").find_next_sibling()
        site_aux: Tag = soup.find("td", text="Site:").find_next_sibling()
        sector_category_aux: Tag = soup.find("td", text="Classificação Setorial:").find_next_sibling()
        
        return_obj.name = name_aux.text if name_aux else ""
        return_obj.cnpj = cnpj_aux.text.replace(".", "").replace("-", "").replace("/", "") if cnpj_aux else ""
        return_obj.major_activity = maj_act_aux.text if maj_act_aux else ""
        return_obj.web_site = site_aux.text if site_aux else ""
        return_obj.sector = sector_category_aux.text if sector_category_aux else ""
        return_obj.cvm_code = cvm.cvm_code

        return return_obj
    pass