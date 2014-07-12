from flask import Flask, jsonify, make_response, request
import os

app = Flask(__name__)
app.config.from_pyfile('testserver.cfg')

test_server = os.environ.get('TEST_SERVER', None)
if test_server:
    app.config['SERVER_NAME'] = test_server.split('://')[-1]


@app.route('/behave-http', methods=['HEAD', 'GET'])
def test_i_am_a_testserver():
    return ''


@app.route('/test/head', methods=['HEAD'])
def test_head():
    return ''


@app.route('/test/get', methods=['GET'])
def test_get():
    return make_response(jsonify({}))


@app.route('/test/post', methods=['POST'])
def test_post():
    return make_response('', 204)


@app.route('/test/post/mirror/json', methods=['POST'])
def test_post_json_mirror():
    return make_response(jsonify(request.get_json()), 201)


@app.route('/test/options', methods=['OPTIONS'])
def test_options():
    resp = make_response('', 200)
    resp.headers['Allow'] = 'HEAD, GET, OPTIONS'
    return resp


@app.route('/test/put/json', methods=['PUT'])
def test_put_json():
    return make_response(jsonify(request.get_json()), 200)


@app.route('/test/patch/json', methods=['PATCH'])
def test_patch_json():
    return make_response(jsonify(request.get_json()), 200)


@app.route('/test/delete', methods=['DELETE'])
def test_delete():
    return make_response('', 204)


@app.route('/test/trace', methods=['TRACE'])
def test_trace():
    body = '\n'.join(
        ['{0}: {1}'.format(h, v) for h, v in request.headers.items()])
    resp = make_response(body, 200)
    resp.headers['Content-Type'] = 'message/http'
    return resp


@app.route('/test/get/args-to-json', methods=['GET'])
def test_get_args_to_json():
    resp = make_response(jsonify(request.args.to_dict(flat=True)))
    return resp


_poll_counter = 3
@app.route('/test/get/poll', methods=['GET'])
def test_get_poll():
    global _poll_counter
    if not _poll_counter > 0:
        _poll_counter = 3
    else:
        _poll_counter -= 1
    resp = dict(counter=_poll_counter)
    return make_response(jsonify(resp))


if __name__ == '__main__':
    app.run()
