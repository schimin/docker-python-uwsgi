
from flask import Flask, request
#from flask_ngrok import run_with_ngrok
import json
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
#run_with_ngrok(app)   
app.config['SECRET_KEY'] = 'GDM @pi Roteirization Google Tools '
api = Api(app)
#jwt = JWTManager(app)

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

TOKEN = 'IUSJDKBDASBSADS776&@SAAAWAQ'

@app.route("/", methods=['POST'])
def home():
  #print(request.json)
  #print(request.headers)

  if not request.headers:
    return json.dumps({'message' : 'Token é obrigatório !!'}), 401
  else:
    dados = request.headers

  if 'Authorization' in dados:
    auth = dados['Authorization']
    bearer = auth.replace("Bearer", "")
    token = bearer.strip()
    #print(token)
  
    if str(token) != str(TOKEN):
      return json.dumps({'message' : 'Token é invalido !!'}), 401
  
  def create_data_model():
      """Stores the data for the problem."""
      data = {}
       
      ### data['distance_matrix'] = [
      ### [139.77,0,2386.19,9913.68], 
      ### [2381.59,2333.65,0,7550.65],
      ### [0,140.85,2434.72,9962.2],
      ### [10106.75,10058.81,7727.69,0]
      ### ]
      
      data['distance_matrix'] = request.json
      data['num_vehicles'] = 1
      data['depot'] = 0
      return data
      

  def print_lista(data, manager, routing, solution):
    cont = int(1)
    for vehicle_id in range(data['num_vehicles']):
      index = routing.Start(vehicle_id)
      plan_output = ''
      lista = []
      cont = 0
      #plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
      route_distance = 0
      
      while not routing.IsEnd(index):
          #lista.append({'id': cont, 'ordem': manager.IndexToNode(index)})
          lista.append({ 'ordem': cont, 'value': manager.IndexToNode(index) })
          #plan_output += ' {} ->'.format(manager.IndexToNode(index))
          previous_index = index
          index = solution.Value(routing.NextVar(index))
          route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
          cont = cont + int(1)
      #plan_output += ' {}\n'.format(manager.IndexToNode(index))
      #lista.append({'id': cont, 'ordem':manager.IndexToNode(index)})
      #plan_output += 'Distance of the route: {}m\n'.format(route_distance)
      return lista


    # [START solution_printer]
  def print_solution(data, manager, routing, solution):
      """Prints solution on console."""
      print(f'Objective: {solution.ObjectiveValue()}')
      total_distance = 0
      for vehicle_id in range(data['num_vehicles']):
          index = routing.Start(vehicle_id)
          plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
          route_distance = 0
          while not routing.IsEnd(index):
              plan_output += ' {} ->'.format(manager.IndexToNode(index))
              previous_index = index
              index = solution.Value(routing.NextVar(index))
              route_distance += routing.GetArcCostForVehicle(
                  previous_index, index, vehicle_id)
          plan_output += ' {}\n'.format(manager.IndexToNode(index))
          plan_output += 'Distance of the route: {}m\n'.format(route_distance)
          #print(plan_output)
          total_distance += route_distance
      print('Total Distance of all routes: {}m'.format(total_distance))

    # [END solution_printer]


  """Entry point of the program."""
  # Instantiate the data problem.
  # [START data]
  data = create_data_model()
  # [END data]

  # Create the routing index manager.
  # [START index_manager]
  manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
  # [END index_manager]

  # Create Routing Model.
  # [START routing_model]
  routing = pywrapcp.RoutingModel(manager)

  # [END routing_model]

  # Create and register a transit callback.
  # [START transit_callback]
  def distance_callback(from_index, to_index):
      """Returns the distance between the two nodes."""
      # Convert from routing variable Index to distance matrix NodeIndex.
      from_node = manager.IndexToNode(from_index)
      to_node = manager.IndexToNode(to_index)
      return data['distance_matrix'][from_node][to_node]

  transit_callback_index = routing.RegisterTransitCallback(distance_callback)
  # [END transit_callback]

  # Define cost of each arc.
  # [START arc_cost]
  routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
  # [END arc_cost]

  # Setting first solution heuristic.
  # [START parameters]
  search_parameters = pywrapcp.DefaultRoutingSearchParameters()
  search_parameters.first_solution_strategy = (
      routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
  # [END parameters]

  # Solve the problem.
  # [START solve]
  solution = routing.SolveWithParameters(search_parameters)
  # [END solve]

  if solution:
      #print(print_solution(data, manager, routing, solution))
      #print(print_lista(data, manager, routing, solution))
      listagem = print_lista(data, manager, routing, solution)
      
      return json.dumps(listagem)
  else:
      print('No solution found !')
    

    
if __name__ == '__main__': 
  app.run(host='0.0.0.0')