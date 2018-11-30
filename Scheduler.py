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
		self.build_fields_list(self.target_list)



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




	def build_fields_list(self,target_list):
		#czyszczenie
		self.field_list=[]

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





	def get_critical_field(self):
		min=len(self.fields_list[0].sensors)
		critical_field=self.fields_list[0]
		for field in self.fields_list:
			if len(field.sensors)<min:
				critical_field=field
				min=len(field.sensors)
		return critical_field








	def get_covers_list(self)->list:
		covers=[]
		sensors=copy.deepcopy(self.sensor_list)
		while(len(sensors)!=0):
			self.build_fields_list(self.get_avaiable_targets(sensors))
			cover=self.get_best_cover(sensors)
			covers.append(cover)
			sensors=list(filter(lambda x:x not in cover,sensors))



	def get_best_cover(self,sensors):
		cover=[]
		while(not(self.goal_achieved(cover))):
			critical_field=self.get_critical_field()
			fields_list=copy.deepcopy(self.fields_list)
			sensor_list=copy.deepcopy(sensors)
			while len(fields_list)!=0:
				max=None
				best_sensor=self.get_best_sensor()






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

	def get_best_sensor(self,critical_field,sensors):
		for sensor in list(filter(lambda x: critical_field in x.fields, sensors)):
			sensor_value=self.get_sensor_value()

	def get_sensor_value(self,sensor,sensors,uncovered_fields,critical_field,cover):
		value=0
		for field in sensor.fields:
			if field!=critical_field:
				if(field in uncovered_fields):
					value=value+len(field.targets)- (len(field.sensors)-1)
				else:
					sensors_from_cover_number=self.sensors_from_cover_number(field,cover)
					value=value-len(field.targets)-sensors_from_cover_number+len(field.sensors)

	def sensors_from_cover_number(self, field,cover):
		number=0
		for sensor in cover:
			if field in sensor.fields:
				number=number+1
		return number





			



