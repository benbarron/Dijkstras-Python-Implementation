import time
import pandas as pd
import numpy as np

class Network:
	def __init__(self):
		self.nodes = []
	
	def add_node(self, id=None):
		if id is None: 
			raise Exception('An id for the node is required')
		self.nodes.append(Node(id))

	def add_route(self, origin_id=None, destination_id=None, cost=None):
		if origin_id is None or destination_id is None:
			raise Exception('origin_id and destination_id is required')
		if cost is None:
			cost = 0
		origin_node = None
		destination_node = None
		for i in range(len(self.nodes)):
			if self.nodes[i].id == origin_id:
				origin_node = self.nodes[i]
			if self.nodes[i].id == destination_id:
				destination_node = self.nodes[i]
		if origin_node is None or destination_node is None: 
			raise Exception('Could not find both origin and destination nodes')
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
 
class DijkstrasShortestPath: 
	def __init__(self, network):
		perm_nodes = []
		temp_nodes = network.nodes.copy()
		temp_nodes[0].distance = 0
		self.temp_nodes = temp_nodes
		self.perm_nodes = perm_nodes
		self.run_time = 0
		self.run_finished = False

	def run(self):
		start_time = time.time()
		while len(self.temp_nodes) > 0:
			d = [n.distance for n in self.temp_nodes] ## find distances of nodes
			m = self.temp_nodes[d.index(min(d))] ## get node with min distance
			for i in range(len(m.routes)):
				if m.routes[i].destination.distance > m.routes[i].via.distance + m.routes[i].cost: 
					m.routes[i].destination.distance = m.routes[i].via.distance + m.routes[i].cost
					m.routes[i].destination.pred = m.routes[i].via
			self.perm_nodes.append(m)
			self.temp_nodes.pop(self.temp_nodes.index(m))
		self.run_time = time.time() - start_time
		self.run_finished = True

	def print_summary(self):
		if not self.run_finished: 
			raise Exception('Run the algorithm before viewing the results.')

		output = f'Dijkstra Finished in {self.run_time}\n\n'	
		output += 'N = Node\nD = Total Cost/Distance\nV = Via/Pred\n\n'
		output += 'N\tD\tV\n'
		output += '-\t-\t-\n'
		
		for i in range(len(self.perm_nodes)):
			output += f'{self.perm_nodes[i].id}\t{self.perm_nodes[i].distance}\t'
			if self.perm_nodes[i].pred is not None:
				output += str(self.perm_nodes[i].pred.id)
			else: 
				output += 'None'
			output += '\n'
		print(output)

	def get_path_to(self, node=None, node_id=None):
		if not self.run_finished: 
			raise Exception('Run the algorithm before viewing the results.')
		if node is None and node_id is None:
			raise Exception('Either a node or node id is required')

		if node is None:
			ids = [node.id for node in self.perm_nodes] 
			temp = self.perm_nodes[ids.index(node_id)]
		else: 
			temp = node 
		
		path = ''
		while temp is not None: 
			path = str(temp.id) + path
			temp = temp.pred
		return '-'.join(list(path))
		
	def print_path_to(self, node=None, node_id=None):
		print(' -> '.join(self.get_path_to(node=node, node_id=node_id).split('-')))

def main():
	FILE_PATH = './src/data.csv'
	data = pd.read_csv(FILE_PATH)
	network = Network()

	for _id in pd.unique(np.append(data['origin_id'].values, data['destination_id'].values)):
		network.add_node(id=_id)

	for i in range(data.shape[0]):
		network.add_route(origin_id=data.iloc[i,0], destination_id=data.iloc[i,1], cost=data.iloc[i,2])

	dijkstra = DijkstrasShortestPath(network)
	dijkstra.run()                          
	dijkstra.print_summary()                
	dijkstra.print_path_to(node_id='e')       
	
if __name__ == '__main__':
	main()


