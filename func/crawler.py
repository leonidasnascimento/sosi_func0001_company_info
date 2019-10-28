import urllib3
import datetime

from typing import List
from .models.cvm import CVM
from .models.company_info import Company
from bs4 import (BeautifulSoup, ResultSet)

class company_info():
    def __init__(self):
        pass
    
    def get_info(self, cvm: CVM) -> Company:
        return_obj: Company = Company()
        url_bmf_bovespa = "http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoEmpresaPrincipal.aspx?codigoCvm={}&idioma=pt-br"
        url_yahoo = "https://br.financas.yahoo.com/quote/{}.SA/profile"

        req = urllib3.PoolManager()
        res = req.request('GET', url_bmf_bovespa.format(cvm.cvm_code))
        soup = BeautifulSoup(res.data, 'html.parser')

        name_aux = soup.find("td", text="CNPJ:")


        return return_obj
        pass
    pass