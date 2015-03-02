import json
import logging
from itertools import count

import requests
from requests.auth import HTTPBasicAuth

DEFAULT_LIMIT = 50
BATCH_SIZE = 250


class CompassClient(object):

    def __init__(self, compass_token=None, endpoint='compass', debug=False):
        """
        Args:
            - compass_token: an access_token string
        """
        self.endpoint = endpoint
        self.compass_token = compass_token
        if debug:
            # These two lines enable debugging at httplib level (requests->urllib3->http.client)
            # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
            # The only thing missing will be the response.body which is not logged.
            try:
                import http.client as http_client
            except ImportError:
                # Python 2
                import httplib as http_client
            http_client.HTTPConnection.debuglevel = 1

            # You must initialize logging, otherwise you'll not see debug output.
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger('requests.packages.urllib3')
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def _check_for_errors(self, response):
        if not response.ok:
            raise CompassClientException(response)

    @property
    def default_headers(self):
        return {
            'Content-Type': 'application/json',
            'x-compass-token': '{0}'.format(self.compass_token)
        }

    def _request(self, method, resource, params=None, data=None, headers=None, **kwargs):
        """
        Performs a HTTP request to Compass.
        This method adds authentication headers, and performs error checking on the response.
        It also automatically tries to refresh tokens, if possible.
        Args:
            - method: The type of HTTP method, f.ex. get or post
            - resource: The resource to request (without shared prefix)
            - params: Any query parameters to send
            - data: Any data to send. If data is a dict, it will be encoded as json.
            - headers: Any ional headers
            - auth: Authentication
            - **kwargs: Any additional arguments to pass to the request
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        if headers:
            headers = dict(headers)
            headers.update(self.default_headers)
        else:
            headers = self.default_headers
        url = 'https://%s.cosential.com/api/%s' % (self.endpoint, resource)
        response = requests.request(method, url, params=params, data=data, headers=headers, **kwargs)
        self._check_for_errors(response)
        return response

    # User methods
    def get_user(self):
        return self._request('get', 'user/').json()

    def get_user_token(self, username=None, password=None, firm_id=None, api_key=None):
        auth = HTTPBasicAuth(username, password)
        headers = {
            'x-compass-firm-id': firm_id,
            'x-compass-api-key': api_key,
        }
        response = self._request('get', 'user/', auth=auth, headers=headers)
        if not response.ok:
            return None
        return response.json()[0].get('UserToken')

    # Company methods
    def get_company_schema(self):
        return self._request('get', 'companies/schema/').json()

    def get_company(self, company_id=0):
        return self._request('get', 'companies/{0}'.format(company_id)).json()

    def get_company_list(self, limit=DEFAULT_LIMIT, offset=0):
        """
        Returns companies.
        Args:
            - limit: number of users to return. (default=50, max=250). Optional.
            - offset: The record at which to start. Optional.
        """
        params = {
            'size': limit,
            'from': offset,
        }
        return self._request('get', 'companies/', params).json()

    def get_company_iterator(self):
        for page in count(0):
            page = self.get_company_list(limit=BATCH_SIZE, offset=page*BATCH_SIZE)
            for item in page:
                yield item
            if not page:
                break

    def search_companies(self, query=''):
        """
        Search companies
        Args:
            - query: SEE: https://compass.cosential.com/documentation#search
        """
        return self._request('get', 'companies/search?q={0}'.format(query)).json()

    def get_company_addresses(self, company_id=0):
        return self._request('get', 'companies/{0}/addresses/'.format(company_id)).json()

    def get_company_contacts(self, company_id=0):
        return self._request('get', 'companies/{0}/contacts/'.format(company_id)).json()

    def get_company_divisions(self, company_id=0):
        return self._request('get', 'companies/{0}/divisions/'.format(company_id)).json()

    def get_company_offices(self, company_id=0):
        return self._request('get', 'companies/{0}/offices/'.format(company_id)).json()

    def get_company_practice_areas(self, company_id=0):
        return self._request('get', 'companies/{0}/practiceareas/'.format(company_id)).json()

    def get_company_primary_prequalifications(self, company_id=0):
        return self._request('get', 'companies/{0}/prequalifications/'.format(company_id)).json()

    def get_company_primary_categories(self, company_id=0):
        return self._request('get', 'companies/{0}/primarycategories/'.format(company_id)).json()

    def get_company_studios(self, company_id=0):
        return self._request('get', 'companies/{0}/studios/'.format(company_id)).json()

    def get_company_territories(self, company_id=0):
        return self._request('get', 'companies/{0}/territories/'.format(company_id)).json()

    def get_company_types(self, company_id=0):
        return self._request('get', 'companies/{0}/companytypes/'.format(company_id)).json()

    def get_company_users(self, company_id=0):
        return self._request('get', 'companies/{0}/users/'.format(company_id)).json()

    def update_company(self, company):
        return self._request('put', 'companies/{0}/'.format(company.get('CompanyId')), data=company).json()

    def create_company(self, company):
        return self._request('post', 'companies/', data=json.dumps([company])).json()

    # Company methods
    def get_contact_schema(self):
        return self._request('get', 'contacts/schema/').json()

    def get_contact(self, contact_id=0):
        return self._request('get', 'contacts/{0}'.format(contact_id)).json()

    def get_contact_list(self, limit=DEFAULT_LIMIT, offset=0):
        """
        Returns contacts.
        Args:
            - limit: number of users to return. (default=50, max=250). Optional.
            - offset: The record at which to start. Optional.
        """
        params = {
            'size': limit,
            'from': offset,
        }
        return self._request('get', 'contacts/', params).json()

    def search_contacts(self, query=''):
        """
        Search contact
        Args:
            - query: SEE: https://compass.cosential.com/documentation#search
        """
        return self._request('get', 'contacts/search?q={0}'.format(query)).json()

    def get_contact_iterator(self):
        for page in count(0):
            page = self.get_contact_list(limit=BATCH_SIZE, offset=page*BATCH_SIZE)
            for item in page:
                yield item
            if not page:
                break

    def get_contact_company(self, contact_id=0):
        return self._request('get', 'contacts/{0}/company/'.format(contact_id)).json()

    def get_contact_category(self, contact_id=0):
        return self._request('get', 'contacts/{0}/contact_category/'.format(contact_id)).json()

    def get_contact_divisions(self, contact_id=0):
        return self._request('get', 'contacts/{0}/divisions/'.format(contact_id)).json()

    def get_contact_offices(self, contact_id=0):
        return self._request('get', 'contacts/{0}/offices/'.format(contact_id)).json()

    def update_contact(self, contact):
        return self._request('put', 'contacts/{0}/'.format(contact.get('ContactId')), data=contact).json()

    def create_contact(self, contact):
        return self._request('post', 'contacts/', data=json.dumps([contact])).json()

    # Project methods
    def get_project_schema(self):
        return self._request('get', 'projects/schema/').json()

    def get_project(self, project_id=0):
        return self._request('get', 'projects/{0}'.format(project_id)).json()

    def get_project_list(self, limit=DEFAULT_LIMIT, offset=0):
        """
        Returns projects.
        Args:
            - limit: number of users to return. (default=50, max=250). Optional.
            - offset: The record at which to start. Optional.
        """
        params = {
            'size': limit,
            'from': offset,
        }
        return self._request('get', 'projects/', params).json()

    def search_project(self, query=''):
        """
        Search contact
        Args:
            - query: SEE: https://compass.cosential.com/documentation#search
        """
        return self._request('get', 'projects/search?q={0}'.format(query)).json()

    def get_project_iterator(self):
        for page in count(0):
            page = self.get_project_list(limit=BATCH_SIZE, offset=page*BATCH_SIZE)
            for item in page:
                yield item
            if not page:
                break

    def update_project(self, project):
        return self._request('put', 'projects/{0}/'.format(project.get('ProjectId')), data=project).json()

    def create_project(self, project):
        return self._request('post', 'projects/', data=json.dumps([project])).json()

    # Company methods
    def get_opportunity_schema(self):
        return self._request('get', 'opportunities/schema/').json()

    def get_opportunity(self, project_id=0):
        return self._request('get', 'opportunities/{0}'.format(project_id)).json()

    def get_opportunity_list(self, limit=DEFAULT_LIMIT, offset=0):
        """
        Returns opportunities.
        Args:
            - limit: number of users to return. (default=50, max=250). Optional.
            - offset: The record at which to start. Optional.
        """
        params = {
            'size': limit,
            'from': offset,
        }
        return self._request('get', 'opportunities/', params).json()

    def get_opportunity_iterator(self):
        for page in count(0):
            page = self.get_opportunity_list(limit=BATCH_SIZE, offset=page*BATCH_SIZE)
            for item in page:
                yield item
            if not page:
                break

    def update_opportunity(self, project):
        return self._request('put', 'opportunities/{0}/'.format(project.get('OpportunityId')), data=project).json()

    def create_opportunity(self, project):
        return self._request('post', 'opportunities/', data=project).json()


class CompassClientException(Exception):

    def __init__(self, response, **kwargs):
        super(CompassClientException, self).__init__(response.text)
        self.response = response
        self.reason = response.reason
        self.status_code = response.status_code
        self.text = response.text
        self.__dict__.update(kwargs)

    def __str__(self):
        if self.text:
            return "{0}: {1} - {2}".format(self.status_code, self.reason, self.text)
        return "{0}: {1}".format(self.status_code, self.reason)
