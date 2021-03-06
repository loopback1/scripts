# use your venv here
#
# wrap a playbook inside a flask restful api app..
import subprocess
import re
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

# flask restful returns json format, no need to use jsonify method
# just return dictionaries

ansi_escape = re.compile(r'\x1b[^m]*m')

# create flask app
app = Flask(__name__)

# wrap app into an api
api = Api(app)

# run playbook here
def run_clear_vpn():
    '''
    run my playbook from command line
    assumes that -i is a dynamic inventory
    '''
    p = subprocess.Popen('ansible-playbook -f 40 -i clear_vpn_inv.py clear__vpn.yml',
                        shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT
                )
    for line in p.stdout.readlines():
            print line,
            retval = p.wait()
    return

# create Item class and inherit Resource flask class
class Item(Resource):
    def post(self, name):
        data = request.get_json()
        if name == 'clear_vpn':
            job_output = run_clear_vpn()
            return {"message": "DONE!"}, 200
        return {"message": "something went wrong..."}, 200

# create API Resources
api.add_resource(Item, '/job=/<string:name>')

# port=5000 is default and does not need to be identified
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)

