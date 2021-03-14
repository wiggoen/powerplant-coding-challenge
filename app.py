from flask import Flask, request
import json


app = Flask(__name__)  # Create an instance of the Flask class


def productionplan_response(data):
  data = data
  result = '--- Formatted dictionary ---\n'
  return result


@app.route('/')
def index():
  return 'Base URL'


@app.route('/productionplan', methods=['POST'])
def test():
  if request.method == 'POST':
    if request.is_json:
      data = request.get_json()

      # DO SOMETHING WITH THE DATA!!
      print(data)
      result = productionplan_response(data)

      return result, 200
    else:
      return 'POST is not JSON.'
  else:
    return 'Error: Method is not POST.'

@app.errorhandler(405)
def internal_error(error):
    return render_template('405.html'),405

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500



if __name__ == '__main__':
  app.run(debug=True, host="127.0.0.1", port=8888)