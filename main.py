## requires >= python3.8.0 
import time
import sys
import pandas as pd
import numpy as np


class Network:
	def __init__(self):
		self.nodes = []

	def find_nodes(self, origin_id, destination_id):
		origin_node, destination_node = None, None

		for i in range(len(self.nodes)):
			if self.nodes[i].id == origin_id:
				origin_node = self.nodes[i]
			if self.nodes[i].id == destination_id:
				destination_node = self.nodes[i]

		if origin_node is None or destination_node is None:
			raise Exception('Could not find origin or destination node')

		return origin_node, destination_node

	def add_node(self, id=None):
		self.nodes.append(Node(id))

	def add_route(self, origin_id=None, destination_id=None, cost=0):
		if origin_id is None or destination_id is None:
			raise Exception('origin_id and destination_id is required')
		origin_node, destination_node = self.find_nodes(origin_id, destination_id)
		origin_node.add_route(destination_node, cost)

class Node:
	def __init__(self, id):
		self.routes = []
		self.id = id
		self.distance = float('inf')
		self.pred = None

	def __repr__(self):
		return f'Node(Id: {self.id}, Distance: {self.distance}, Pred: {self.pred})'

	def add_route(self, destination, cost):
		self.routes.append(Route(self, destination, cost))


class Route:
	def __init__(self, via, destination, cost):
		self.via = via
		self.destination = destination
		self.cost = cost

	def __repr__(self):
		return f'Route(From: {str(self.via.id)}, To: {str(self.destination.id)}, Cost: {str(self.cost)})'

class Algorithm:
	def __init__(self, network):
		self.run_time = 0
		self.run_finished = False
		self.perm_nodes = []
		self.temp_nodes = network.nodes.copy()

	def find_node(self, node_id):
		ids = [node.id for node in self.perm_nodes]
		return self.perm_nodes[ids.index(node_id)]

	def get_path_to(self, node_id):
		if not self.run_finished:
			raise Exception('Run the algorithm before viewing the results.')

		temp, path = self.find_node(node_id), ''

		while temp is not None:
			path = str(temp.id) + path
			temp = temp.pred

		return '-'.join(list(path))

	def print_path_to(self, node_id):
		print('Path: ' + ' -> '.join(self.get_path_to(node_id).split('-')))

	def print_distance_to(self, node_id):
		if not self.run_finished:
			raise Exception('Run the algorithm before viewing the results.')

		if (node := self.find_node(node_id)) is None:
			raise Exception(f'Node with id {node_id} not found')

		print(f'Distance: {node.distance}')

	def print_summary(self):
		if not self.run_finished:
			raise Exception('Run the algorithm before viewing the results.')

		output = f'\nDijkstra finished in {self.run_time} seconds\n\n' 
		output += 'N = Node\nD = Total Cost/Distance\nV = Via/Pred\n\n' 
		output += 'N\tD\tV\n-\t-\t-\n'

		for i in range(len(self.perm_nodes)):
			output += f'{self.perm_nodes[i].id}\t{self.perm_nodes[i].distance}\t'
			if self.perm_nodes[i].pred is not None:
				output += str(self.perm_nodes[i].pred.id)
			else:
				output += 'None'
			output += '\n'
		print(output)
	
	def prompt(self):
		while 1:
			if (a := input("Enter id of node to display shortest path to or 'quit' to exit: ").lower()) == 'quit':
				break
			try:
				self.print_path_to(a)
				self.print_distance_to(a)
			except Exception as e:
				print(e)

class DijkstrasShortestPath(Algorithm):
	def __init__(self, network):
		Algorithm.__init__(self, network)
		self.temp_nodes[0].distance = 0

	def run(self, verbose=False):
		start_time = time.time()
		while len(self.temp_nodes) > 0:
			d = [n.distance for n in self.temp_nodes]
			m = self.temp_nodes[d.index(min(d))]
			for i in range(len(m.routes)):
				if m.routes[i].destination.distance > m.routes[i].via.distance + m.routes[i].cost:
					m.routes[i].destination.distance = m.routes[i].via.distance + m.routes[i].cost
					m.routes[i].destination.pred = m.routes[i].via
			self.perm_nodes.append(m)
			self.temp_nodes.remove(m)
			if verbose:
				print(f'Node with id \'{m.id}\' became permanent.')
		self.run_time = time.time() - start_time
		self.run_finished = True

class AStar(Algorithm):
	def __init__(self, network):
		Algorithm.__init__(self, network)
		## todo

def check_file_input(file_path):
	path_arr = list(file_path)
	for i in range(len(path_arr)):
		if path_arr[i] == "'":
			path_arr[i] = ""
	return ''.join(path_arr).strip()

def main():
	if len(sys.argv) < 2:
		FILE_PATH = input('Please enter a file path for your data: ')
	else: 
		FILE_PATH = sys.argv[1]

	data = pd.read_csv(check_file_input(FILE_PATH))
	network = Network()

	for _id in pd.unique(np.append(data['origin_id'].values, data['destination_id'].values)):
		network.add_node(id=str(_id))

	for i in range(data.shape[0]):
		network.add_route(origin_id=str(data.iloc[i, 0]), destination_id=str(data.iloc[i, 1]), cost=data.iloc[i, 2])

	dijkstra = DijkstrasShortestPath(network)
	dijkstra.run(verbose=True)
	dijkstra.print_summary()
	dijkstra.prompt()

if __name__ == '__main__':
	main()
