from flask import jsonify, make_response


def ok(status, values, message):
    res = {
        'status': status,
        'values': values,
        'message': message
    }

    return make_response(jsonify(res)), 200

def badRequest(values, message):
    res = {
        'values': values,
        'message': message
    }

    return make_response(jsonify(res)), 400