import datetime
import logging
import azure.functions as func
import json
import requests
import pathlib
import threading

from typing import List
from configuration_manager.reader import reader
from .crawler import company_info
from .stock import stock_cvm_code

SETTINGS_FILE_PATH = pathlib.Path(
    __file__).parent.parent.__str__() + "//local.settings.json"

def main(SosiFunc0001CompanyInfo: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    try:
        config_obj: reader = reader(SETTINGS_FILE_PATH, 'Values')
        list_cvm_code: [] = None
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
        logging.info("{} acquired from service...".format(len(list_cvm_code)))


        if list_cvm or len(list_cvm) == 0:
            logging.warning("No CVM code to process!")
        else:
            # Crawling
            logging.info("Getting stock list. It may take a while...")  
            
            for cvm in list_cvm:
                obj = company_info().get_info(cvm)
                comp_json_obj: str = json.dumps(obj)

                logging.info("Company information acquired for '{}'".format(cvm.cvm_code))

                threading.Thread(target=invoke_url, args=(cvm.cvm_code, service_url_post_company_info, comp_json_obj)).start()
            pass

        logging.info("Timer job is done. Waiting for the next execution time")
        pass
    except Exception as ex:
        error_log = '{} -> {}'
        logging.exception(error_log.format(utc_timestamp, str(ex)))
        pass
    pass

def invoke_url(cvm_code, url, json):
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    requests.request("POST", url, data=json, headers=headers)
    logging.info("'{}' posted to domain micro service".format(cvm_code))
    pass