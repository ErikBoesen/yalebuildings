import requests


class Building(_base):
    def __init__(self, raw):
        self.raw = raw



class YaleBuildings:
    API_TARGET = 'https://gw.its.yale.edu/soa-gateway/buildings/feed'
    data = None

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get(self, params: dict = {}):
        """
        Make a GET request to the API.

        :param params: dictionary of custom params to add to request.
        """
        params.update({
            'apikey': self.api_key,
            'type': 'json',
        })
        request = requests.get(self.API_TARGET, params=params)
        if request.ok:
            return request.json()['ServiceResponse']['Buildings']
        else:
            # TODO: Can we be more helpful?
            raise Exception('API request failed. Data returned: ' + request.text)

    def retrieve(self):
        """
        Download and store building data.
        """
        if self.data is None:
            self.data = [Building(raw) for raw in self.get()]

    def buildings(self):
        """
        Fetch a list of all buildings on campus.
        """
        self.retrieve()
        return self.data

    def building(self, id: str) -> Building:
        """
        Generate a request to the API and fetch data within a given date range.

        :param building_id: ID of building to get data on. You may wish to use Yale's Building API to find an ID.
        :param start_date: date to start sampling from. Can be a string or datetime/date object, or year/month tuple.
        :param end_date: date to end sampling at. Formatting is the same as start_date. If not specified, today.
        """
        self.retrieve()
