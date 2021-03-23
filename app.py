from flask import Flask, request
import json


app = Flask(__name__)  # Create an instance of the Flask class


def production_range(powerplants, wind):
  for i in range(len(powerplants)):
    efficiency = powerplants[i]['efficiency']
    pmin = powerplants[i]['pmin']
    pmax = powerplants[i]['pmax']
    # production based on efficiency
    min_production = pmin * efficiency
    max_production = pmax * efficiency
    if powerplants[i]['type'] in 'windturbine':
      # production based on available wind
      min_production *= wind / 100
      max_production *= wind / 100
    # add production range
    powerplants[i].update({'prange': [round(min_production, 1), \
                                      round(max_production, 1)]})
  return powerplants


def calculate_production(load, powerplants, wind):
  # Implementation of how to calculate production.
  # Solving a multi-dimensional root problem.

  # WORK IN PROGRESS!!!
  # The simple naive solution (hierarchy based)
  # 1. Wind power (because of cost and efficiency)
  # 2. Gas (because of cost)
  # 3. Kerosine (because of cost)

  # Hierarchy based on cost ['windturbine', 'gasfired', 'turbojet']
  sorted_powerplants = sorted(powerplants, key=lambda k: \
                              (k['type'] == 'windturbine', \
                               k['type'] == 'gasfired', \
                               k['type'] == 'turbojet', \
                               k['pmax']), reverse=True)

  print('SORTED:\n', json.dumps(sorted_powerplants, indent=2))

  powerplant_production = []
  total_production = 0

  for powerstation in sorted_powerplants:
    name = powerstation['name']
    p = 0
    efficiency = powerstation['efficiency']
    min_production, max_production = powerstation['prange']

    #### TEST if adding more power is more than load.
    #### If so, add min power - or check how much power and check if it is
    #### between min and max power for powerplant

    if load == total_production:
      print('LOAD achieved!')
    elif load > total_production + max_production:
      total_production += max_production
      p = max_production
    elif total_production + min_production < load < total_production + max_production:
      rest = load - total_production
      total_production += rest
      p = rest
    else:
      print('Special case....')
      print('L:', load, ' p_tot:', total_production)

    if total_production < load:
      print('Load NOT achieved! Need more power!')

    power_production = {'name': name, 'p': round(p/efficiency, 1)}
    powerplant_production.append(power_production)

  return powerplant_production


def merit_order(data):
  # Payload
  load = data['load']                # Amount of energy in MWh
  fuels = data['fuels']              # Dictionary of fuels
  powerplants = data['powerplants']  # List of dictionaries of powerplants

  # Production metrics of fuels
  gas = fuels['gas(euro/MWh)']            # Euro/MWh
  kerosine = fuels['kerosine(euro/MWh)']  # Euro/MWh
  CO2 = fuels['co2(euro/ton)']            # Euro/ton
  wind = fuels['wind(%)']                 # % (percent)

  # Powerplants based on production efficiency
  powerstations = production_range(powerplants, wind)


  print('--- --- --- --- --- --- --- --- --- ---')
  #print('POWERPLANTS:\n', powerplants) #-------------------------------------#
  print('Powerstations:\n', powerstations)
  print('Payload load to equal:', load)
  print('SOLVE LINEAR EQUATION EQUAL TO LOAD.')
  result = calculate_production(load, powerstations, wind)
  #result = 0
  # Constraints on first powerplant (for testing)
  #print(stations[0]['eff_pmin'], stations[0]['eff_pmax'])
  print('--- --- --- --- --- --- --- --- --- ---')

  # TODO: SORT POWER STATIONS BASED ON PRODUCTION BEFORE SENDING THE RESPONSE?

  return json.dumps(result, indent=2)


@app.route('/')
def index():
  return 'Base URL'


@app.route('/productionplan', methods=['POST'])
def productionplan_response():
  if request.method == 'POST':
    if request.is_json:
      data = request.get_json()  # Dictionary of JSON data

      # ----------------------------------------------------------------------#
      #print('PAYLOAD:\n', data)
      # ----------------------------------------------------------------------#

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