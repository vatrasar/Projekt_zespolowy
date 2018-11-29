import time
from Statistics import Statistic
from Sensor import Sensor
from Target import Target
from Field import Field
import copy



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
		self.target_list = target_list #type: list[Target]
		self.duration = 0
		self.paint = paint
		self.percent_observed_targets = 0
		self.sensor_range = sensor_range
		self.compute_sensors_targets()
		self.statistics = Statistic(target_list,sensors_list) #type: Statistic
		self.fields_list=[] #type:list[Field]
		self.build_fields_list()



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




	def build_fields_list(self):
		for target in self.target_list:

			field_exist=False
			#jeśli pole dla targeta istnieje to dodaj target
			for field in self.fields_list:
				if field.sensors==target.covering_sensors:
					field.targets.append(target)
					field_exist=True
			#jeśli pole dla targeta nie istnieje to utwórz nowe
			if not field_exist:
				self.add_field_for_target(target)

	def add_field_for_target(self, target):
		if len(target.covering_sensors)==0:
			return

		field = Field(target)
		self.fields_list.append(field)
		for sensor in self.sensor_list:
			if sensor in field.sensors:
				sensor.fields.append(field)


	def activate_covers_sensors(self, cover)->list:
		pass
	def disable_cover(selfs,cover):
		pass

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





	def get_critical_field(self, G):
		pass





	def get_covers_list(self)->list:
		pass



	def get_best_cover(self, G, y1, y2,targets,sensor_list,orginal_sensors_list):
		pass

	def get_one_sensor_targets(self):
		"""
		zwraca targety pokryte przez tylko jeden sensor
		:param sensor_list_test:
		"""
		return list(filter(lambda x:len(x.covering_sensors)==1 and x.covering_sensors[0].battery>0,self.target_list))


	def get_avaiable_targets(self,sensor_list):
		pass

