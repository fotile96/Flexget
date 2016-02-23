from __future__ import unicode_literals, division, absolute_import

import logging

from flask import jsonify

from flexget.api import api, APIResource
from flexget.plugins.list import movie_list as ml

log = logging.getLogger('movie_list')

movie_list_api = api.namespace('movie_list', description='Movie List operations')

default_error_schema = {
    'type': 'object',
    'properties': {
        'status': {'type': 'string'},
        'message': {'type': 'string'}
    }
}

default_error_schema = api.schema('default_error_schema', default_error_schema)

input_movie_entry = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'url': {'type': 'string'},
        'movie_name': {'type': 'string'},
        'movie_year': {'type': 'integer'}
    },
    'additionalProperties': True,
    'required': ['url'],
    'anyOf': [
        {'required': ['title']},
        {'required': ['movie_name', 'movie_year']}
    ]
}

movie_list_id_object = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'id_name': {'type': 'string'},
        'id_value': {'type': 'string'},
        'movie_id': {'type': 'integer'}
    }
}

movie_object = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'year': {'type': 'integer'},
        'list_id': {'type': 'integer'},
        'movie_list_ids': {
            'type': 'array',
            'items': movie_list_id_object
        },
    }
}

list_object = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'name': {'type': 'string'},
        'movies': {
            'type': 'array',
            'items': movie_object
        },
        'number_of_movies': {'type': 'integer'}

    }
}

return_lists = {'type': 'array', 'items': list_object}

input_movie_entry_schema = api.schema('input_movie_entry', input_movie_entry)
movie_list_id_object_schema = api.schema('movie_list_id_object', movie_list_id_object)
movie_object_schema = api.schema('movie_object', movie_object)
list_object_schema = api.schema('list_object', list_object)
return_lists_schema = api.schema('return_lists', return_lists)


@movie_list_api.route('/')
class MovieListAPI(APIResource):
    @api.response(200, model=return_lists_schema)
    def get(self, session=None):
        ''' Gets all movies lists '''
        movie_lists = [movie_list.to_dict() for movie_list in ml.get_all_lists(session=session)]
        return jsonify({'movie_lists': movie_lists})
