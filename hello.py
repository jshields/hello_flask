"""
example flask module
"""
from flask import Flask, render_template, jsonify  # flask itsdangerous Werkzeug Jinja2 click MarkupSafe

from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import NotFound

CONFIG_FILE = 'config.json'

app = Flask(__name__)


def _html_file_ext(name):
    """Suffix a name with the HTML file extension.
    Uses `.html`, not `.htm`.
    """
    return '%(name)s.html' % {'name': name}


@app.errorhandler(404)
def page_not_found(error):
    """404 Not Found custom page"""
    return render_template('page_not_found.html', error=error), 404


@app.route("/hello_string")
def hello_string():
    """flask Hello World"""
    # 200 OK is assumed but
    # I state it explicitly
    return "Hello World!", 200


@app.route('/hello_template/')
@app.route('/hello_template/<name>')
def hello_name(name='Flask'):
    """templates/ dir is the template root for flask"""
    kwargs = {'name': name}
    return render_template('hello.html', **kwargs), 200


@app.route('/<name>')
def hello_template(name):
    """templates/ dir is the template root for flask"""
    filename = _html_file_ext(name)
    try:
        resp = render_template(filename), 200
    except TemplateNotFound:
        resp = page_not_found(NotFound())
    return resp


@app.route('/<path:filename>')
def hello_path(filename):
    """
    Serves based on filename.
    Must only serve from the /templates dir as root!

    path: like the default but also accepts slashes
    """
    template = _html_file_ext(filename)
    return render_template(template)


@app.route('/hello_json')
def hello_json():
    """JSON response.
    jsonify: turns the JSON output into a
    Response object with application/json
    """
    payload = {
        'obj_guy': {
            'foo': 'cat',
            'bar': 2,
            'baz': True
        },
        'other_guy': {
            'banana': False,
            'strength': 5.623
        }
    }
    return jsonify(payload)


if __name__ == '__main__':
    # execute only if run in top-level scope
    app.config.from_json(CONFIG_FILE, silent=False)
    # To allow aptana to receive errors, set use_debugger=False
    use_debugger = False
    if app.debug:  # and not app.config.get('DEBUG_WITH_APTANA')
        use_debugger = True

    # this has to be called after the routes are setup
    app.run(use_debugger=use_debugger, debug=use_debugger,
            use_reloader=use_debugger, host='127.0.0.1')
