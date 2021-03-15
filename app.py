from flask import Flask, request
import json


app = Flask(__name__)  # Create an instance of the Flask class


def merit_order(data):
  # Payload
  load = data['load']                # Amount of energy in MWh
  fuels = data['fuels']              # Dictionary of fuels
  powerplants = data['powerplants']  # List of dictionaries of powerplants

  # Production metrics of fuels
  gas = fuels['gas(euro/MWh)']            # Euro/MWh
  kerosine = fuels['kerosine(euro/MWh)']  # Euro/MWh
  CO2 = fuels['co2(euro/ton)']            # Euro/ton
  wind = fuels['wind(%)']                 # % (percentage)

  # Powerplants based on production efficiency
  stations = []
  for powerstation in powerplants:
    name = powerstation['name']
    efficiency = powerstation['efficiency']
    pmin = powerstation['pmin']
    pmax = powerstation['pmax']
    if powerstation['type'] in ['gasfired', 'turbojet']:
      min_production = pmin * efficiency
      max_production = pmax * efficiency
    elif powerstation['type'] is 'windturbine':
      min_production = pmin * efficiency * wind
      max_production = pmax * efficiency * wind
    station = {'name': name, 'eff_pmin': min_production, 'eff_pmax': max_production}
    stations.append(station)

  print('--- --- --- --- --- --- --- --- --- ---')
  print('Load to equal:', load)
  print('FIND LINEAR EQUATION EQUAL TO LOAD.')
  print('--- --- --- --- --- --- --- --- --- ---')

  result = json.dumps(stations, indent=2)
  return result


@app.route('/')
def index():
  return 'Base URL'


@app.route('/productionplan', methods=['POST'])
def productionplan_response():
  if request.method == 'POST':
    if request.is_json:
      data = request.get_json()  # Dictionary of JSON data
      result = merit_order(data)
      return result, 200
    else:
      return 'Error: POST is not JSON.'
  else:
    return 'Error: Method is not POST.'


#@app.errorhandler(405)
#def internal_error(error):
#    return render_template('405.html'),405

#@app.errorhandler(500)
#def internal_error(error):
#    return render_template('500.html'),500


if __name__ == '__main__':
  app.run(debug=True, host="127.0.0.1", port=8888)