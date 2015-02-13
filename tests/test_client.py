import json

import requests
import unittest2 as unittest
from flexmock import flexmock

from compass import CompassClient, CompassClientException
from tests import mocked_response


class TestClient(unittest.TestCase):
    def make_client(self, method, resource, params=None, data=None, headers=None, endpoint='compass', result=None, **kwargs):
        """
        Makes a new test client
        """
        client = CompassClient('my_token')
        (flexmock(client)
            .should_receive('_check_for_errors')
            .once())

        if headers:
            headers = dict(headers)
            headers.update(client.default_headers)
        else:
            headers = client.default_headers

        if isinstance(data, dict):
            data = json.dumps(data)

        (flexmock(requests)
            .should_receive('request')
            .with_args(method,
                       'https://%s.cosential.com/api/%s' % (endpoint, resource),
                       params=params,
                       data=data,
                       headers=headers,
                       **kwargs)
            .and_return(mocked_response(result))
            .once())

        return client

    def test_handle_error(self):
        client = CompassClient('my_token')

        with self.assertRaises(CompassClientException) as expected_exception:
            client._check_for_errors(mocked_response('something terrible', status_code=599, reason='because'))
        self.assertEqual(599, expected_exception.exception.status_code)
        self.assertEqual('something terrible', expected_exception.exception.message)
        self.assertEqual('because', expected_exception.exception.reason)

    def test_get(self):
        client = self.make_client('get', 'foo', params={'arg': 'value'}, bar=1)
        client._request('get', 'foo', {'arg': 'value'}, bar=1)

    def test_post_dict(self):
        expected_data = {'arg': 'value'}
        client = self.make_client('post', 'foo', result='result', data=expected_data, bar=1)
        actual_response = client._request('post', 'foo', data=expected_data, bar=1)
        self.assertEqual('result', actual_response.text)

    def test_post_data(self):
        expected_data = 'mooooo'
        client = self.make_client('post', 'foo', result='result', data=expected_data, bar=1)
        actual_response = client._request('post', 'foo', data=expected_data, bar=1)
        self.assertEqual('result', actual_response.text)

    def test_put_dict(self):
        expected_data = {'arg': 'value'}
        client = self.make_client('put', 'foo', result='result', data=expected_data, bar=1)
        actual_response = client._request('put', 'foo', data=expected_data, bar=1)
        self.assertEqual('result', actual_response.text)

    def test_put_data(self):
        expected_data = 'mooooo'
        client = self.make_client('put', 'foo', result='response', data=expected_data, bar=1)
        actual_response = client._request('put', 'foo', data=expected_data, bar=1)
        self.assertEqual(actual_response.text, 'response')

    def test_delete(self):
        custom_headers = {'hello': 'world'}

        client = self.make_client('delete', 'foo', result='response', headers=custom_headers, bar=1)
        actual_response = client._request('delete', 'foo', headers=custom_headers, bar=1)
        self.assertEqual(actual_response.text, 'response')

        # verify headers were not modified
        self.assertDictEqual(custom_headers, {'hello': 'world'})


if __name__ == '__main__':
    unittest.main()
