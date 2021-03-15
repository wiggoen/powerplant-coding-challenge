from flask import Flask, request
import json


app = Flask(__name__)  # Create an instance of the Flask class

'''
# Tried the bisection method for a simple problem.
# Found out that it was a bad choice.
def bisection(f, a, b, eps):
  fa = f(a)
  if fa*f(b) > 0:
    return None, 0

  i = 0  # Iteration counter
  while b-a > eps:
    i += 1
    m = (a+b)/2
    fm = f(m)
    if fa*fm <= 0:
      b = m  # root is in left half of [a,b]
    else:
      a = m  # root is in right half of [a,b]
      fa = fm
  return m, i

def f(x):
  return 2*x - 3

a=0 #stations[0]['eff_pmin']
b=10 #stations[0]['eff_pmax']
x, i = bisection(f, a, b, eps=1E-5)
print(x, iter)
if x is None:
  print('f(x) does not change sign in [%g, %g]' % (a, b))
else:
  print('The root is', x, 'found in', i, 'iterations')
  print('f(%g)=%g' % (x, f(x)))
'''

def calculate_production(load, stations):
  # Implementation of how to calculate production.
  # Solving a multi-dimensional root problem.

  production = []

  for powerstations in stations:
    name = powerstations['name']

    # Calculate power production p for each station
    p = 0

    power_production = {'name': name, 'p': p}
    production.append(power_production)

  return production


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
  print('Payload load to equal:', load)
  print('SOLVE LINEAR EQUATION EQUAL TO LOAD.')
  result = calculate_production(load, stations)
  # Constraints on first powerplant (for testing)
  #print(stations[0]['eff_pmin'], stations[0]['eff_pmax'])
  print('--- --- --- --- --- --- --- --- --- ---')

  return json.dumps(result, indent=2)


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