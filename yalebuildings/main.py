import requests


class Building(_base):
    def __init__(self, raw):
        self.raw = raw



class YaleBuildings:
    API_TARGET = 'https://gw.its.yale.edu/soa-gateway/buildings/feed'
    data = None

    def __init__(self, api_key: str):
        self.api_key = api_key

