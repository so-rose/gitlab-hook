from flask import Flask, request
import json
import sys

app = Flask(__name__)

@app.route('/',methods=['POST'])
def foo():
   data = json.loads(request.data)
   print("New commit by: {}".format(data['commits'][0]['author']['name']), file=sys.stderr)
   return "OK"

if __name__ == '__main__':
   app.run(port=7080)
