from __future__ import unicode_literals, division, absolute_import
from builtins import *  # pylint: disable=unused-import, redefined-builtin

import json
import os

import pytest

from flexget import __version__
from flexget.api.app import __version__ as __api_version__, base_message
from flexget.api.core.server import ObjectsContainer as OC
from flexget.manager import Manager
from flexget.tests.conftest import MockManager
from flexget.utils.tools import get_latest_flexget_version_number
from mock import patch


class TestServerAPI(object):
    config = """
        tasks:
          test:
            rss:
              url: http://test/rss
            mock:
              - title: entry 1
        """

    def test_pid(self, api_client, schema_match):
        rsp = api_client.get('/server/pid/', headers={})
        assert rsp.status_code == 200
        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(OC.pid_object, data)
        assert not errors
        assert data['pid'] == os.getpid()

    @patch.object(MockManager, 'load_config')
    def test_reload(self, mocked_load_config, api_client, schema_match):
        rsp = api_client.get('/server/reload/')
        assert rsp.status_code == 200
        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(base_message, data)
        assert not errors
        assert mocked_load_config.called

    @patch.object(Manager, 'shutdown')
    def test_shutdown(self, mocked_shutdown, api_client, schema_match):
        rsp = api_client.get('/server/shutdown/')
        assert rsp.status_code == 200
        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(base_message, data)
        assert not errors
        assert mocked_shutdown.called

    def test_get_config(self, api_client, schema_match):
        rsp = api_client.get('/server/config/')
        assert rsp.status_code == 200
        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match({'type': 'object'}, data)
        assert not errors
        assert data == {
            'tasks': {
                'test': {
                    'mock': [{'title': 'entry 1'}],
                    'rss': {
                        'url': u'http://test/rss',
                        'group_links': False,
                        'ascii': False,
                        'silent': False,
                        'all_entries': True
                    }
                }
            }
        }

    @pytest.mark.online
    def test_version(self, api_client, schema_match):
        latest = get_latest_flexget_version_number()

        rsp = api_client.get('/server/version/')
        assert rsp.status_code == 200
        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(OC.version_object, data)
        assert not errors
        assert data == {'flexget_version': __version__,
                        'api_version': __api_version__,
                        'latest_version': latest}
