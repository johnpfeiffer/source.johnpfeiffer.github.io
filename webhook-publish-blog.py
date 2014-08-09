from flask import Flask
import os
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route('/jpblog', methods=['GET', 'POST'])
def john():
  try:
      # output = Popen(["pwd"], stdout=PIPE).communicate()[0]
      output = Popen(["./mypublish.sh"], stdout=PIPE).communicate()[0]
  except Exception as error:
      return str(error)
  return output


if __name__ == '__main__':
    app.run('0.0.0.0', 8084, use_reloader=True)
