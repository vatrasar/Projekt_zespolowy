import time
from Statistics import Statistic
from Sensor import Sensor
from Target import Target
from graph import Node
import networkx as nx
import copy
import matplotlib.pyplot as plt



class Scheduler:

	def __init__(self,sensors_list,target_list,sensor_range, paint):
		"""
		:param sensors_list:lista obiektów typu Sensor
		:param sensing_range:
		:param targets_list:pytanie czy będziemy obserwować cele czy jakiś obszar
		jeśli obszar to parametr jest niepotrzebny
		:param duration: czas trwania symulacji (czas życia sieci sensorowej)
		:param paint: obiekt łączący z interfacem, uaktualnia ekran
		z symulacja, najlepiej użyj self.paint.paint(self)
		za każdym razem kiedy włączysz lub wyłączysz jakiś sensor,
		możesz też użyć tej funkcji np. w jakiejś głównej pętli symulacji
		:param percent_observed_targets: procent obserwowanych celów
		"""
		self.sensor_list=sensors_list #type: list[Sensor]
		self.target_list = target_list
		self.duration = 0
		self.paint = paint
		self.percent_observed_targets = 0
		self.sensor_range = sensor_range
		self.compute_sensors_targets()
		self.statistics = Statistic(target_list,sensors_list) #type: Statistic
		self.min_Flow=None
		self.m=0

	def get_sensor_list(self):
		pass
	def run(self):


		#Tu algorytm symulacji
		
		#Przykładowy kod prezentujący interface, musisz podać co najmniej
		#1000 sensorów. Przykładowe dane do przetestowania tego kodu
		#1000 sensorów, 1000 targetów, 10 zasięg, 10 bateria, 
		#1000 wysokość, 1000 szerokość


		# i=0
		# while i < 1000:
		# 	self.paint.paint(self)
		# 	self.sensor_list[i].set_sensor_state(False)
		# 	i+=1
		covers=self.get_covers_list()
		base_battery_level=self.sensor_list[0].battery
		for cover in covers:
			cover=self.activate_covers_sensors(cover)
			cover_time_start=time.time()
			while(time.time()-cover_time_start<base_battery_level):
				self.paint.paint(self)
				for sensor in cover:
					sensor.battery=sensor.battery-1
			self.disable_cover(cover)




	def activate_covers_sensors(self, cover)->list:
		result_cover=[] #w zmiennej cover są ukryte sensory które są innymi obiektami niż te w sensor_list
		#w result_cover chce mieć sensory które są w sensor_list
		for sensor in self.sensor_list:
			if sensor in cover:
				sensor.active = True
				result_cover.append(sensor)
		return result_cover
	def disable_cover(selfs,cover):
		for sensor in cover:
			sensor.active=False

	def compute_sensors_targets(self):
		"""
		oblicza które sensory pokrywają które targety. j
		"""
		for	sensor in self.sensor_list:
			target: Target
			for target in self.target_list:
				if target.localization.distance_to(sensor.localization) <= sensor.sensing_range:
					sensor.covering_targets.append(target)
					target.covering_sensors.append(sensor)

	def get_percent_observed_targets(self):
		return self.statistics.get_percent_observed_targets()



	def build_flow_graph(self):
		G=self.build_G_graph()
		k=self.get_critical_number(G)
		G_list=self.make_k_copies_of_G(k,G)
		flow_graph=self.join_G_list(G_list)
		self.add_Y_nodes(flow_graph)

		

	def build_G_graph(self):
		G=nx.DiGraph()
		# G.add_nodes_from(self.sensor_list,type="sensor")
		G.m=0 #maksymalna liczba targetów które mogą byc pokryte
		added_targets=set()
		G.ed =[]
		for sensor in self.sensor_list:
			sensor.active=False
			if len(sensor.covering_targets)!=0:
				G.add_node(sensor, type="sensor")
			for target in sensor.covering_targets:
				set_size=len(added_targets)
				added_targets.add(target)
				if set_size!=len(added_targets): #żeby nie dodać dwa razy tego samego targeta
					G.add_node(target,type="target")
					self.m=self.m+1
				G.add_edge(sensor,target,weight=1,active=False)
				G.ed.append((sensor,target))
		return G


	def make_k_copies_of_G(self,k,G):
		pass

	def get_critical_number(self, G):
		"""

		:param G: podstawowy graf składający się z Targetów sensorów oraz węzła X
		:return: k. zwraca liczbe sensorów która pokrywa najmniej pokryty sensor
		"""
		target_nodes_list = list(filter(lambda x: x[1] == "target", G.nodes(data='type')))
		min=None
		for target_node in target_nodes_list:
			degree= G.in_degree(target_node[0])
			if min==None:
				min=degree
			if degree<min:
				min=degree
		return min

	def join_G_list(self, G_list):
		pass

	def add_Y_nodes(self, G:nx.DiGraph):
		y1=Node(1)
		y2=Node(2)
		G.add_node(y1, type="Y1")
		G.add_node(y2, type="Y2")
		for target in self.target_list:
			if G.has_node(target):
				G.add_edge(target,y1,weight=0,active=True)
				G.add_edge(target,y2,weight=0,active=True)
		return y1, y2
	def compute_flow_value(self,G:nx.DiGraph,node):
		predecessors_list = G.predecessors(node)
		flow_value=0
		# labels = {node:"y"}
		# nx.draw(G, with_labels=True, labels=labels)
		# plt.show()
		if G.node[node]["type"]=="Y1":
			predecessors_list = G.predecessors(node)
			for predecessor in predecessors_list:
				flow=self.compute_flow_value(G, predecessor)
				if flow==0:
					continue
				flow_value=flow_value+self.compute_flow_value(G,predecessor)-1

		elif G.node[node]["type"]=="Y2":
			predecessors_list = G.predecessors(node)
			for predecessor in predecessors_list:
				if self.compute_flow_value(G,predecessor)!=0:
					flow_value =flow_value+1
		else:
			for predecessor in predecessors_list:
				edge=G.get_edge_data(predecessor, node)
				if edge['active']==True:
					flow_value=flow_value+edge['weight']

		return flow_value


	def get_covers_list(self)->list:

		G=self.build_G_graph()
		y1,y2=self.add_Y_nodes(G)

		covers=[]
		sensor_list=copy.deepcopy(self.sensor_list) #type: list(Sensor)

		#usuwamy z tymczasowej listy sensory które niczego nie pokrywają
		sensor_list=list(filter(lambda x: x.is_covering_any_target(), sensor_list))

		while(True):
			targets=self.get_avaiable_targets(sensor_list)
			new_cover=self.get_best_cover(G,y1,y2,targets,sensor_list,sensor_list) #type: list
			if len(new_cover)==0:
				break
			covers.append(new_cover)
			#usuwamy z listy sensory które są już w jakimś pokryciu
			sensor_list=list(filter(lambda x: x not in new_cover, sensor_list))
			if len(sensor_list)==0:
				break
			self.min_Flow=None
			print(str(self.m) + " m")
			# self.m=self.m_future


		return covers




	def change_sensor_state(self,G:nx.DiGraph,sensor:Sensor,new_state:bool):
		sensor.set_sensor_state(new_state)
		for target in sensor.covering_targets:
			atributes=G.get_edge_data(sensor,target)
			atributes['active']=new_state

	def get_best_cover(self, G, y1, y2,targets,sensor_list,orginal_sensors_list):

		G_test = copy.deepcopy(G)
		sensor_list=copy.deepcopy(sensor_list)
		best_cover=None
		targets=list(targets)
		if len(targets)!=0:
			for sensor in targets[0].covering_sensors:
				if sensor in sensor_list:
					self.change_sensor_state(G_test,sensor,True)
					flow_value = self.compute_flow_value(G_test, y1)
					if self.min_Flow!=None and self.min_Flow<=flow_value:
							continue
					sensor_list.remove(sensor)
					new_targets=targets[1:]
					cover=self.get_best_cover(G_test,y1,y2,new_targets,sensor_list,orginal_sensors_list)

					if len(cover)!=0:
						best_cover=cover
			if best_cover==None:
				return []
			else:
				return best_cover
		flow_value=self.compute_flow_value(G_test,y1)

		if self.min_Flow==None:
			self.min_Flow=flow_value
		if self.min_Flow<flow_value:
			return []
		return list(filter(lambda x: x not in sensor_list, orginal_sensors_list))





	def is_goal_achieved(self, G_test, y2):
		return self.compute_flow_value(G_test, y2) == self.m

	def get_one_sensor_targets(self):
		"""
		zwraca targety pokryte przez tylko jeden sensor
		:param sensor_list_test:
		"""
		return list(filter(lambda x:len(x.covering_sensors)==1 and x.covering_sensors[0].battery>0,self.target_list))

	def draw_graph(self,G, sensor_list):
		labels = {}
		for sensor in sensor_list:
			if len(sensor.covering_targets)!=0:
				labels[sensor] = "sensor " + str(sensor.localization)
				for target in sensor.covering_targets:
					labels[target] = "target " + str(target.localization)
		G=copy.deepcopy(G)

		colors = [G[u][v]['active'] for u, v in G.edges()]
		print(colors)
		colors = list(map(lambda x: self.transalte(x), colors))
		nx.draw(G, edges=G.edges, edge_color=colors, with_labels=True, labels=labels)
		plt.show()

	def transalte(self,arg):
		if arg:
			return 'g'
		else:
			return 'r'

	def get_avaiable_targets(self,sensor_list):
		targets=set()
		for sensor in sensor_list:
			for target in sensor.covering_targets:
				targets.add(target)

		return targets

# def get_same_cover_sensors(self, sensor_list):
	# 	"""
	# 	zwraca sensory które pokrywają dokładnie te same targety
	# 	:param sensor_list_test:
	# 	"""
	#
	# 	#stworzenie listy targetów które pokrywają sensory z listy
	# 	sensors_targets=set()
	# 	for sensor in sensor_list:
	# 		sensors_targets.update(sensor.covering_targets)
	# 	same_cover_sensors={}
	# 	for target in sensors_targets:
	# 		covering_sensors=copy.deepcopy(target.covering_sensors) #type:list[Sensor]
	# 		for i, sensor in enumerate(covering_sensors):
	# 			for p,sen in enumerate(covering_sensors):
	# 				if covering_sensors[i].covering_targets==covering_sensors[p].covering_targets:
	# 					same_cover_sensors[covering_sensors[i].covering_targets]=same_cover_sensors.get(covering_sensors[i].covering_targets,set()).add(covering_sensors[p])
	# 					same_cover_sensors[covering_sensors[i].covering_targets] = same_cover_sensors.get(covering_sensors[i].covering_targets, set()).add(covering_sensors[i])
	#
	# 	a=filter(labda,same_cover_sensors.values())
	# 	return list(same_cover_sensors.values())