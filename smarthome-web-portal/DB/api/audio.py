# -*- coding: utf-8 -*-
"""
CRUD operation for environment model
"""
from DB.api import database
from DB import exception
from DB.models import Audio
from DB.api import dbutils as utils


RESP_FIELDS = ['id', 'resource', 'resource_id', 'mute', 'volume', 'created_at']
SRC_EXISTED_FIELD = {'id': 'id',
                     'resource_id': 'resource_id',
                     'mute': 'mute',
                     'volume': 'volume',
                     'created_at': 'created_at'
                     }


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)
def new(session, src_dic, content={}):
    for k, v in SRC_EXISTED_FIELD.items():
        content[k] = src_dic.get(v, None)
    return utils.add_db_object(session, Audio, **content)


def _get_audio(session, resource_id, order_by=[], limit=None, **kwargs):
    if isinstance(resource_id, int):
        resource_ids = {'eq': resource_id}
    elif isinstance(resource_id, list):
        resource_ids = {'in': resource_id}
    else:
        raise exception.InvalidParameter('parameter resource id format are not supported.')
    return \
        utils.list_db_objects(session, Audio, order_by=order_by, limit=limit,
                              resource_id=resource_ids, **kwargs)


@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)  # wrap the raw DB object into dict
def get_audio_by_gateway_uuid(session, resource_id):
    return _get_audio(session, resource_id)


# get the latest data if exists
@database.run_in_session()
@utils.wrap_to_dict(RESP_FIELDS)      # wrap the raw DB object into dict
def get_latest_by_gateway_uuid(session, resource_id, ):
    audio = _get_audio(session, resource_id, order_by=[('id', True)], limit=1)
    return audio[0] if len(audio) else None