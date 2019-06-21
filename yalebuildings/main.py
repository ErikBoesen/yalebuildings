import requests


class Building(_base):
    def __init__(self, raw):
        self.update(json)
        self.update(self.__dict__)

        self.site = raw['SITE']
        # Building number, unique identifier for the particular building.  Example:  0430
        self.id = raw['BUILDING']
        # Building abbreviation.  Example:  LFOP
        self.abbreviation = raw['BUILDING_ABBR']
        # Building description.  Example:  LEITNER OBSV &amp; PLANET.
        self.description = raw['DESCRIPTION']
        # Building usage description.  Example:  ACADEMIC
        self.category = raw.get('USAGE_DESCRIPTION')
        # TODO: use better names?
        # Building street address 1.  Example:  PROSPECT STREET, 355
        self.address_1 = raw['ADDRESS_1']
        self.street_address = self.address_1
        # Building city and state.  Example:  NEW HAVEN, CT
        self.address_2 = raw['ADDRESS_2']
        self.city, self.state = self.address_2.split(', ')
        # Building zip code.  Example:  06511
        self.address_3 = raw['ADDRESS_3']
        self.zip_code = self.address_3
        # Building status.  Example:  OPEN, CLOSED
        self.status = raw['STATUS']
        self.open = (self.status == 'OPEN')
        self.closed = not self.open
        # Building historical alias.  Example:  CIA CARPENTRY SHOP, UNDERGRAD OBSERVATORY
        self.historical_alias = raw['HISTORICAL_ALIAS']
        # Other building address.  Example:  355 PROSPECT STREET
        self.street_address_alias = raw['ADDR1_ALIAS']
        # Messaging alias.  Example:  PROSPECT ST, 355
        self.messaging_alias = raw['MSAG_ALIAS']
        self.latitude = float(raw['LATITUDE'])
        self.longitude = float(raw['LONGITUDE'])
        # Building historical name.  Example:  Roth Autitorium for Culinary Inst of America
        self.historical_name = raw['HISTORICAL NAME']
        self.prose = raw['BUILDING PROSE']


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
