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
		self.compute_sensors_targets(self.sensor_list)
		self.statistics = Statistic(target_list,sensors_list) #type: Statistic
		self.fields_list=[] #type:list[Field]
		self.build_fields_list(self.target_list,self.sensor_list)



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
		self.disable_cover(self.sensor_list)
		covers = self.get_covers_list()
		base_battery_level = self.sensor_list[0].battery
		for cover in covers:
			cover = self.activate_covers_sensors(cover)
			cover_time_start = time.time()
			while (time.time() - cover_time_start < base_battery_level):
				self.paint.paint(self)
				for sensor in cover:
					sensor.battery = sensor.battery - 1
			self.disable_cover(cover)




	def build_fields_list(self,target_list,sensors):
		#czyszczenie
		self.fields_list=[]

		for target in target_list:
			for sensor in target.covering_sensors:
				sensor.fields=[]

		for target in target_list:
			field_exist=False
			#jeśli pole dla targeta istnieje to dodaj target
			for field in self.fields_list:
				if field.sensors==target.covering_sensors:
					field.targets.append(target)
					field_exist=True
			#jeśli pole dla targeta nie istnieje to utwórz nowe
			if not field_exist:
				for sensor in target.covering_sensors:
					if sensor in sensors:
						self.add_field_for_target(target,sensors)
						break


	def add_field_for_target(self, target,sensors):
		if len(target.covering_sensors)==0:
			return

		field = Field(target)
		self.fields_list.append(field)
		for sensor in sensors:
			if sensor in field.sensors:
				sensor.fields.append(field)


	def activate_covers_sensors(self, cover)->list:
		cover=list(filter(lambda x:x in cover,self.sensor_list))
		for sensor in cover:
			sensor.active=True
		return cover
	def disable_cover(selfs,cover):
		for sensor in cover:
			sensor.active=False
		return cover

	def compute_sensors_targets(self,sensor_list):
		"""
		oblicza które sensory pokrywają które targety. j
		"""
		for sensor in sensor_list:
			sensor.covering_targets=[]
		for target in self.target_list:
			target.covering_sensors=[]
		for	sensor in sensor_list:
			target: Target
			for target in self.target_list:
				if target.localization.distance_to(sensor.localization) <= sensor.sensing_range:
					sensor.covering_targets.append(target)
					target.covering_sensors.append(sensor)

	def get_percent_observed_targets(self):
		return self.statistics.get_percent_observed_targets()





	def get_critical_field(self,fields_list):
		min=len(self.fields_list[0].sensors)
		critical_field=fields_list[0]
		for field in fields_list:
			if len(field.sensors)<min:
				critical_field=field
				min=len(field.sensors)
		return critical_field








	def get_covers_list(self)->list:
		covers=[]
		sensors=self.sensor_list
		while(len(sensors)!=0):
			self.build_fields_list(self.get_avaiable_targets(sensors),sensors)
			if len(self.fields_list)==0:
				break
			cover=self.get_best_cover(sensors)
			covers.append(cover)
			sensors=list(filter(lambda x:x not in cover,sensors))
		return covers


	def get_best_cover(self,sensors):
		cover=[]
		fields_list = copy.deepcopy(self.fields_list)
		sensor_list = copy.deepcopy(sensors)
		while(not(self.goal_achieved(cover))):
			critical_field=self.get_critical_field(fields_list)
			best_sensor=self.get_best_sensor(critical_field,sensor_list,cover,fields_list)
			self.best_sensor_to_cover(best_sensor, cover, fields_list, sensor_list)
		return cover


	def best_sensor_to_cover(self, best_sensor, cover, fields_list, sensor_list):
		"""
		dodaje najlepszy sensor do covera
		:param best_sensor:
		:param cover:
		:param fields_list:
		:param sensor_list:
		"""
		cover.append(best_sensor)
		for field in best_sensor.fields:
			if field in fields_list:
				fields_list.remove(field)
		sensor_list.remove(best_sensor)

	def get_one_sensor_targets(self):
		"""
		zwraca targety pokryte przez tylko jeden sensor
		:param sensor_list_test:
		"""
		return list(filter(lambda x:len(x.covering_sensors)==1 and x.covering_sensors[0].battery>0,self.target_list))


	def get_avaiable_targets(self,sensor_list):
		targets=[]
		self.compute_sensors_targets(sensor_list)
		for target in self.target_list:
			for sensor in target.covering_sensors:
				if sensor.battery>0 and sensor in sensor_list:
					targets.append(target)
					break
		return targets

	def goal_achieved(self,cover):
		covered_fields=set()
		for sensor in cover:
			for field in sensor.fields:
				covered_fields.add(field)
		return len(covered_fields)==len(self.fields_list)

	def get_best_sensor(self,critical_field,sensors,cover,uncovered_fields)->Sensor:

		available_sensors=list(filter(lambda x: critical_field in x.fields, sensors))

		max_value = self.get_sensor_value(available_sensors[0],sensors,uncovered_fields,critical_field,cover)
		max_sensor = available_sensors[0]
		available_sensors.remove(max_sensor)
		for sensor in available_sensors:
			sensor_value=self.get_sensor_value(sensor,sensors,uncovered_fields,critical_field,cover)
			if sensor_value>max_value:
				max_sensor=sensor
				max_value=sensor_value

		return max_sensor


	def get_sensor_value(self,sensor,sensors,uncovered_fields,critical_field,cover):
		value=0
		for field in sensor.fields:
			if field!=critical_field:
				if(field in uncovered_fields):
					value=value+len(field.targets)- (len(field.sensors)-1)
				else:
					sensors_from_cover_number=self.sensors_from_cover_number(field,cover)
					value=value-len(field.targets)-sensors_from_cover_number+len(field.sensors)
		return value

	def sensors_from_cover_number(self, field,cover):
		number=0
		for sensor in cover:
			if field in sensor.fields:
				number=number+1
		return number





			



