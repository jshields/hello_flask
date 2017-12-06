"""
example flask module
"""
from flask import Flask, render_template, json, jsonify  # flask itsdangerous Werkzeug Jinja2 click MarkupSafe

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
    return "Hello World!", 200


@app.route('/hello_template/')
@app.route('/hello_template/<name>')
def hello_name(name='Flask'):
    """templates/ dir is the template root for flask"""
    kwargs = {'name': name}
    return render_template('hello.html', **kwargs), 200


#@app.route('/<name>')
#def hello_template(name):
#    """templates/ dir is the template root for flask"""
#    filename = _html_file_ext(name)
#    try:
#        resp = render_template(filename), 200
#    except TemplateNotFound:
#        resp = page_not_found(NotFound())
#    return resp


@app.route('/hello_json')
def hello_json():
    """JSON response.
    jsonify: turns the JSON output into a
    Response object with application/json
    """
    payload = {
        'thing': {
            'foo': 'cat',
            'bar': 2,
            'baz': True
        },
        'other_thing': {
            'banana': False,
            'strength': 5.623
        }
    }
    return jsonify(payload)


@app.route('/macrotest')
def macro_test():
    """test Jinja macros"""
    filename = 'macro_test.html'

    # name, label, value
    btn_args = ['test-name', 'test-label', 'test-value']
    # order='primary', type='button', icon=None, classes=None, data=None
    btn_kwargs = {
        'icon': 'check',
        'classes': ['fantastic', 'great', 'yes'],
        'data': {
            'target': 'Jupiter',
            # dump to a JavaScript friendly format,
            # since data attrs are used by JavaScript
            'dog': json.dumps({"name": "Rover", "age": 5, "canine": True})
        }
    }

    kwargs = {
        'btn_args': btn_args,
        'btn_kwargs': btn_kwargs
    }

    return render_template(filename, **kwargs), 200


@app.route('/xsstest')
def xss_test():
    """test autoescape"""
    filename = 'xss_test.html'

    pretend_unsafe_input = "<script>alert('JavaScript executed... Gotcha!')</script>"

    kwargs = {
        'unsafe_value': pretend_unsafe_input
    }

    return render_template(filename, **kwargs), 200


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
