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
        url = "http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoEmpresaPrincipal.aspx?codigoCvm={}&idioma=pt-br"

        req = urllib3.PoolManager()
        res = req.request('GET', url.format(cvm.cvm_code))
        soup = BeautifulSoup(res.data, 'html.parser')

        return return_obj
        pass
    pass