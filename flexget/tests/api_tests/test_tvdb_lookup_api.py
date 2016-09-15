# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, absolute_import
from builtins import *  # pylint: disable=unused-import, redefined-builtin

import pytest

from flexget.api.plugins.tvdb_lookup import ObjectsContainer as OC
from flexget.utils import json


@pytest.mark.online
class TestTVDBSeriesLookupAPI(object):
    config = 'tasks: {}'

    def test_tvdb_series_lookup(self, api_client, schema_match):
        values = {
            'tvdb_id': 77398,
            'imdb_id': 'tt0106179',
            'language': 'en',
            'series_name': 'The X-Files',
            'zap2it_id': 'EP00080955'
        }

        rsp = api_client.get('/tvdb/series/The X-Files/')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(OC.tvdb_series_object, data)
        assert not errors

        for field, value in values.items():
            assert data.get(field) == value


@pytest.mark.online
class TestTVDBSeriesActorsLookupAPI(object):
    config = 'tasks: {}'

    def test_tvdb_series_lookup_with_actors(self, api_client, schema_match):
        values = {
            'tvdb_id': 77398,
            'imdb_id': 'tt0106179',
            'language': 'en',
            'series_name': 'The X-Files',
            'zap2it_id': 'EP00080955'
        }

        rsp = api_client.get('/tvdb/series/The X-Files/?include_actors=true')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(OC.tvdb_series_object, data)
        assert not errors

        for field, value in values.items():
            assert data.get(field) == value


@pytest.mark.online
class TestTVDBEpisodeLookupAPI(object):
    config = 'tasks: {}'

    def test_tvdb_episode_lookup_season_and_ep_number(self, api_client, schema_match):
        rsp = api_client.get('/tvdb/episode/77398/')
        assert rsp.status_code == 400, 'Response code is %s' % rsp.status_code

        values = {
            'episode_number': 6,
            'id': 5313345,
            'season_number': 10,
            'series_id': 77398,
            'absolute_number': None
        }

        rsp = api_client.get('/tvdb/episode/77398/?season_number=10&ep_number=6')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.episode_object, data)
        assert not errors

        for field, value in values.items():
            assert data.get(field) == value


@pytest.mark.online
class TestTVDBEpisodeABSLookupAPI(object):
    config = 'tasks: {}'

    def test_tvdb_episode_lookup_by_absolute_number(self, api_client, schema_match):
        values = {
            'episode_number': 23,
            'id': 5598674,
            'season_number': 2,
            'series_id': 279121,
            'absolute_number': 46
        }

        rsp = api_client.get('/tvdb/episode/279121/?absolute_number=46')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.episode_object, data)
        assert not errors

        for field, value in values.items():
            assert data.get(field) == value


@pytest.mark.online
class TestTVDSearchNameLookupAPI(object):
    config = 'tasks: {}'

    def test_tvdb_search_results_by_name(self, api_client, schema_match):
        rsp = api_client.get('/tvdb/search/?search_name=supernatural')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))

        errors = schema_match(OC.search_results_object, data)
        assert not errors

        values = {
            'series_name': "Supernatural",
            'tvdb_id': 78901
        }

        for field, value in values.items():
            assert data[0].get(field) == value


@pytest.mark.online
class TestTVDSearchIMDBLookupAPI(object):
    config = 'tasks: {}'

    def test_tvdb_search_results_by_imdb_id(self, api_client, schema_match):
        rsp = api_client.get('/tvdb/search/?imdb_id=tt0944947')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.search_results_object, data)
        assert not errors

        values = {
            'series_name': "Game of Thrones",
            'tvdb_id': 121361
        }

        for field, value in values.items():
            assert data[0].get(field) == value


@pytest.mark.online
class TestTVDSearchZAP2ITLookupAPI(object):
    config = 'tasks: {}'

    def test_tvdb_search_results_by_zap2it_id(self, api_client, schema_match):
        rsp = api_client.get('/tvdb/search/?zap2it_id=EP01922936')
        assert rsp.status_code == 200, 'Response code is %s' % rsp.status_code

        data = json.loads(rsp.get_data(as_text=True))
        errors = schema_match(OC.search_results_object, data)
        assert not errors

        values = {
            'series_name': "The Flash (2014)",
            'tvdb_id': 279121
        }

        for field, value in values.items():
            assert data[0].get(field) == value
