import time
from Statistics import Statistic
from Sensor import Sensor
import networkx as nx



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
		self.compute_sensors_targets()
		self.sensor_range = sensor_range
		self.statistics = Statistic(target_list,sensors_list) #type: Statistic

	def get_sensor_list(self):
		pass
	def run(self):



		#Tu algorytm symulacji
		
		#Przykładowy kod prezentujący interface, musisz podać co najmniej
		#1000 sensorów. Przykładowe dane do przetestowania tego kodu
		#1000 sensorów, 1000 targetów, 10 zasięg, 10 bateria, 
		#1000 wysokość, 1000 szerokość


		i=0
		while i < 1000:
			self.paint.paint(self)
			self.sensor_list[i].set_sensor_state(False)
			i+=1


	def compute_sensors_targets(self):
		for	sensor in self.sensor_list:
			for target in self.target_list:
				if target.localization.distance_to(sensor.localization) <= sensor.sensing_range:
					sensor.covering_targets.append(target)

	def get_percent_observed_targets(self):
		return self.statistics.get_percent_observed_targets()



	def build_flow_graph(self):
		G=self.build_G_graph()
		k=self.get_critical_number(G)
		G_list=self.make_k_copies_of_G(k,G)
		flow_graph=self.join_G_list(G_list)
		flow_graph=self.add_Y_nodes(flow_graph)

		

	def build_G_graph(self):
		pass


	def make_k_copies_of_G(self,k,G):
		pass

	def get_critical_number(self, G):
		pass

	def join_G_list(self, G_list):
		pass

	def add_Y_nodes(self, flow_graph):
		pass

