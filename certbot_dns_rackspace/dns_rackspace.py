"""DNS Authenticator for Rackspace"""
import logging
import re

import requests
import zope.interface

from certbot import errors, interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)

ACCOUNT_URL = 'https://account.rackspace.com/users'

@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Rackspace

    This Authenticator uses the Rackspace Cloud DNS API to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using a DNS TXT record (if you are using Rackspace Cloud DNS).')
    ttl = 300

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None
        self.zone = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='Rackspace credentials INI file.')
        add('zone', help='Domain/zone under which to add TXT record (defaults to domain as typed).')

    def more_info(self):
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using the Rackspace Cloud DNS API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Rackspace credentials INI file',
            {
                'username': 'username associated with Rackspace account',
                'api-key': 'API key for Rackspace account, obtained from {0}'.format(ACCOUNT_URL)
            }
        )
        self._configure('zone', 'domain/zone under which to add TXT record (enter "@" to use the domain as typed)')

    def _perform(self, domain, validation_name, validation):
        zone = self.conf('zone')
        if not zone or zone == '@':
            zone = domain

        client = self._rackspace_client_setup()
        zone_id = client.get('/domains', params={'name': zone})['domains'][0]['id']
        logger.info('challenge: resolved zone {0} to id {1}'.format(zone, zone_id))

        res = client.post('/domains/{0}/records'.format(zone_id), json={
            'records': [
                {
                    'name': validation_name,
                    'type': 'TXT',
                    'data': validation,
                    'ttl': self.ttl
                }
            ]
        })

        print(res)

    def _cleanup(self, domain, validation_name, validation):
        zone = self.conf('zone')
        if not zone or zone == '@':
            zone = domain

        client = self._rackspace_client_setup()
        zone_id = client.get('/domains', params={'name': zone})['domains'][0]['id']
        logger.info('cleanup: resolved zone {0} to id {1}'.format(zone, zone_id))

        record_id = client.get('/domains/{0}/records'.format(zone_id), params={
            'type': 'TXT',
            'name': validation_name
        })['records'][0]['id']

        client.delete('/domains/{0}/records'.format(zone_id), params={'id': record_id})

    def _rackspace_client_setup(self):
        username = self.credentials.conf('username')
        api_key = self.credentials.conf('api-key')

        return RackspaceClient(username, api_key)

RE_HTTP = re.compile('^https?://')

class SessionWithBaseUrl(requests.Session):
    """A requests session that automatically prefixes the given base URL on all non-absolute requests.

    Usage::

        >>> s = SessionWithBaseUrl('https://example.com/api')
        >>> s.get('/hello')
        <GET https://example.com/api/hello>
        >>> s.post('https://test.dev/hi')
        <POST https://test.dev/hi>
    """

    def __init__(self, base_url, *args, **kwargs):
        super(SessionWithBaseUrl, self).__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        if not RE_HTTP.match(url):
            url = self.base_url + url
        return super(SessionWithBaseUrl, self).request(method, url, *args, **kwargs)

class RackspaceClient:
    """Rackspace Cloud API Client"""

    def __init__(self, username, api_key):
        res = requests.post('https://identity.api.rackspacecloud.com/v2.0/tokens', json={
            'auth': {
                'RAX-KSKEY:apiKeyCredentials': {
                    'username': username,
                    'apiKey': api_key
                }
            }
        })

        res.raise_for_status()
        auth = res.json()['access']

        url = None
        for service in auth['serviceCatalog']:
            if service['type'] == 'rax:dns':
                url = service['endpoints'][0]['publicURL']

        if not url:
            raise RuntimeError('unable to find public URL for DNS service')

        self.session = SessionWithBaseUrl(url)
        self.session.headers['X-Auth-Token'] = auth['token']['id']

    def get(self, url, *args, **kwargs):
        """
        Performs a GET request. See :py:meth:`request` for more info.

        :return: Response object
        :rtype: requests.Response
        """
        return self.request('GET', url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        """
        Performs a POST request. See :py:meth:`request` for more info.

        :return: Response object
        :rtype: requests.Response
        """
        return self.request('POST', url, *args, **kwargs)

    def put(self, url, *args, **kwargs):
        """
        Performs a PUT request. See :py:meth:`request` for more info.

        :return: Response object
        :rtype: requests.Response
        """
        return self.request('PUT', url, *args, **kwargs)

    def patch(self, url, *args, **kwargs):
        """
        Performs a PATCH request. See :py:meth:`request` for more info.

        :return: Response object
        :rtype: requests.Response
        """
        return self.request('PATCH', url, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        """
        Performs a DELETE request. See :py:meth:`request` for more info.

        :return: Response object
        :rtype: requests.Response
        """
        return self.request('DELETE', url, *args, **kwargs)

    def request(self, method, url, *args, **kwargs):
        """
        executes the given request and parses the response as JSON if
        successful.

        :return: Response data
        :rtype: dict
        :raises: requests.HTTPError on non-successful response
        """
        res = self.session.request(method, url, *args, **kwargs)
        res.raise_for_status()
        return res.json()

