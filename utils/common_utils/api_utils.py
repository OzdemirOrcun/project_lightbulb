from flask import jsonify


def bad_request(message):
    """ Returns a json response for bad requests """
    response = jsonify({"message": message})
    response.status_code = 400
    return response


def check_key(dict_, key):
    """ Checks dict key, if not exits return None """
    try:
        return dict_[key]
    except KeyError as e:
        return None
