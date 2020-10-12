import os
import requests
import logging
import json
from urllib.parse import urlencode


accessToken = ""

baseUrl ="https://api.netatmo.com/api/"

def getAccessToken():
    logging.info("Getting access token")
    payload={}
    payload["grant_type"]="password"
    payload["username"]="EMAIL"
    payload["password"]="PASS"
    payload["client_id"]="CLIENT"
    payload["client_secret"]="SECRET"
    payload["scope"]="read_station"

    try:
        response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
        response.raise_for_status()
        logging.debug("token response.json(): %s", response.text)
        accessToken = response.text
        print(response.text)

    except requests.exceptions.HTTPError as error:
        print(error.response.status_code, error.response.text)
        print(payload)
        logging.error(error.response.status_code, error.response.text)
        logging.error(payload)


def post(command, data=None):
    headers = {'Authorization': 'Bearer ' +  accessToken }

    try:     
        response = requests.post(baseUrl+command,  headers=headers, data=data)       
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as error:
        print(error.response.status_code, error.response.text)            
        logging.error(error.response.status_code)
        logging.error(error.response.text)
        raise

def get(command, data=None):              
    headers = {'Authorization': 'Bearer ' +  accessToken }
    params = urlencode(data);
    try:     
        response = requests.get(baseUrl+command+"?"+params,  headers=headers)       
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as error:
        print(error.response.status_code, error.response.text)            
        logging.error(error.response.status_code)
        logging.error(error.response.text)
        raise

def getHomesData():

    response=post("homesdata")

    for currentHome in response.json()["body"]["homes"]:
        print(currentHome)


def getMeasureData(data=None):

    data = {"device_id":"70:ee:50:27:13:54","scale":"1day","type":"Temperature"}

    response=get("getmeasure",data)

    for currentHome in response.json()["body"]:
        print(currentHome)


getAccessToken()
getHomesData()
#getMeasureData()
