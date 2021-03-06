import datetime
import logging
import azure.functions as func
import json
import requests
import pathlib
import threading

from multiprocessing.pool import ThreadPool
from typing import List
from configuration_manager.reader import reader
from .crawler import company_info
from .stock import stock_cvm_code
from .models.company_info import Company
from .models.cvm import CVM

SETTINGS_FILE_PATH = pathlib.Path(
    __file__).parent.parent.__str__() + "//local.settings.json"

def main(SosiFunc0001CompanyInfo: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    try:
        config_obj: reader = reader(SETTINGS_FILE_PATH, 'Values')
        list_cvm: List[CVM] = []
        service_url_cvm_code: str = config_obj.get_value("service_url_cvm_code")
        service_url_post_company_info: str = config_obj.get_value("service_url_post_company_info")

        if service_url_cvm_code == "":
            logging.error("Cannot run timer job because there is no URL set to retrieve CMV code list")
            return
            
        if service_url_post_company_info == "":
            logging.error("Cannot run timer job because there is no URL set to post acquired company info")
            return

        logging.info("'sosi_func0001_company_info' has begun")
        logging.info("Getting list of CVM codes")

        list_cvm = stock_cvm_code(service_url_cvm_code).get_list()
        logging.info("Async processing {} companies got from service. This will take a while".format(len(list_cvm)))

        if len(list_cvm) == 0:
            logging.warning("No CVM code to process!")
        else:            
            pool = ThreadPool(5)

            for cvm in list_cvm:            
                pool.apply_async(func=execute_crawling_asyc, args=(cvm, service_url_post_company_info,))

            pool.close()
            pool.join()        

        logging.info("Timer job is done. Waiting for the next execution time")
        pass
    except Exception as ex:
        error_log = '{} -> {}'
        logging.exception(error_log.format(utc_timestamp, str(ex)))
        pass
    pass

def execute_crawling_asyc(cvm: CVM, service_url_post_company_info: str):
    logging.info("Acquiring details for {}".format(cvm.cvm_code)) 
    
    obj: Company = company_info().get_info(cvm)
    if not obj: 
        return

    comp_json_obj: str = json.dumps(obj.__dict__)

    logging.info("Posting details for '{}'".format(cvm.cvm_code))
    threading.Thread(target=invoke_url_async, args=(cvm.cvm_code, service_url_post_company_info, comp_json_obj)).start()
    pass

def invoke_url_async(cvm_code, url, json):
    if url == "":
        return
    
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    requests.request("POST", url, data=json, headers=headers)
    logging.info("'{}' posted to domain micro service".format(cvm_code))
    pass