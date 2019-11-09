"""You are welcome to use any part of the Python Standard Library in addition to Flask."""
from flask import Flask, render_template, abort, request, make_response
import base64
from http.cookies import SimpleCookie
import sys
sys.path.append("..")
import grader

TARGET_SERVER_ENDPOINT = 'http://localhost:1337'
#TARGET_SERVER_ENDPOINT = 'http://35.223.68.134:80'

app = Flask(__name__)

@app.route('/csrf_target/<msg>')
def forge(msg):
	# Modify the content for different levels
    content = '<h3>csrf</h3>'
    return render_template('csrf.html', body=content)




# NOTE: You are free to add additional routes/endpoints to the attacker server to mount any attack of your choosing.
if __name__ == '__main__':
    app.run(port=1338)
    # app.run(host="0.0.0.0", port=80)