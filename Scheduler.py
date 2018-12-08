import time
from Statistics import Statistic
from Sensor import Sensor
from Target import Target
from Field import Field
from Point import Point
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
		self.start=time.time()
		self.sensor_list=sensors_list #type: list[Sensor]
		self.target_list = target_list #type: list[Target]
		self.statistics = Statistic(target_list, sensors_list)  # type: Statistic
		self.duration = 0
		self.paint = paint
		self.percent_observed_targets = 0
		self.sensor_range = sensor_range
		self.compute_sensors_targets(self.sensor_list)
		self.fields_list=[] #type:list[Field]
		#zliczam targety zanim usunę z listy wszystkie te które nie są pokryte
		self.target_number=len(self.target_list)
		self.old_list=self.target_list.copy()
		self.target_list=list(filter(lambda x:len(x.covering_sensors)!=0,self.target_list))
		self.build_fields_list(self.target_list)

		self.q=90

	def run(self):


		#Tu algorytm symulacji
		
		#Przykładowy kod prezentujący interface, musisz podać co najmniej
		#Przykładowe dane do przetestowania tego kodu
		#400 sensorów, 100 targetów, 20 zasięg, 2 bateria,
		#100 wysokość, 100 szerokość


		# i=0
		# while i < 1000:
		# 	self.paint.paint(self)
		# 	self.sensor_list[i].set_sensor_state(False)
		# 	i+=1
		self.target_list=self.old_list
		covers = self.get_covers_list()
		if len(covers)==0:
			print("zbyt mało sensorów by osiągnąć 90% pokrycia tych celów")
			self.paint.paint(self)
		base_battery_level = self.sensor_list[0].battery
		self.disable_cover(self.sensor_list)
		for sensor in self.sensor_list:
			sensor.battery=base_battery_level
		print("czas obliczeń"+str(time.time()-self.start))
		self.statistics.start_time=time.time()
		for cover in covers:
			cover = self.activate_covers_sensors(cover)
			if self.statistics.get_percent_observed_targets()<self.q:
				break
			cover_time_start = time.time()
			while (time.time() - cover_time_start < base_battery_level):
				self.paint.paint(self)
			self.disable_cover(cover)
			for sensor in cover:
				sensor.battery=0

		self.statistics.stop_time()
		#pokazuje pozostałe naładowane sensory żeby było wiadomo że wypalone
		#zostrało wszystko co możliwe
		# for sensor in self.sensor_list:
		# 	if sensor.battery>0:
		# 		sensor.active=True
		# self.paint.paint(self)
		# time.sleep(10)




	def build_fields_list(self,target_list):
		#czyszczenie
		self.fields_list=[]
		for sensor in self.sensor_list:
			sensor.fields=[]

		for target in target_list:
			field_exist=False
			# target_sensors=list(filter(lambda x:x in self.sensor_list,target.covering_sensors))

			# if len(target_sensors)==0:
			# 	continue
			try:
				target_fields=self.get_target_fields(target)
			except Exception:
				continue

			# jeśli pole dla targeta istnieje to dodaj target
			field_exist = self.add_to_exist_field(target, target_fields)

			#jeśli pole dla targeta nie istnieje to utwórz nowe
			if not field_exist:
				self.add_to_new_field(target)

	def add_to_new_field(self, target):
		for sensor in target.covering_sensors:
			if sensor.active == True:
				self.add_field_for_target(target)
				break

	def add_to_exist_field(self, target, target_fields):
		field_exist=False
		for field in target_fields:
			if field.sensors == target.covering_sensors:
				field.targets.append(target)
				field_exist = True
		return field_exist

	def get_target_fields(self, target)->list:
		"""
		zwraca pola w których może sie znaleźć target
		:param target:
		"""
		for sensor in target.covering_sensors:
			if sensor.active == True:
				return sensor.fields
		raise Exception()

	def add_field_for_target(self, target):
		if len(target.covering_sensors)==0:
			return

		field = Field(target)
		self.fields_list.append(field)

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
		self.activate_covers_sensors(sensors)
		while(True):

			self.build_fields_list(self.get_avaiable_targets())
			if len(self.fields_list)==0:
				break
			cover=self.get_best_cover(sensors)
			#gdy skończa sie sensory to tak bedzie
			if len(cover)==0:
				break

			procent=self.get_cover_procent(cover)

			self.clean_cover(cover)

			print(str(procent)+" procent")
			if procent<self.q:
				return covers
			covers.append(cover)
			cover=list(filter(lambda x:x in cover,sensors))
			sensors=list(filter(lambda x:x not in cover,sensors))
			
			self.disable_cover(cover)

			print("cover "+str(len(covers)))

		return covers


	def get_best_cover(self,sensors):
		cover=[]
		fields_list =self.fields_list.copy()
		sensor_list = sensors.copy()
		while(len(fields_list)!=0):
			critical_field=self.get_critical_field(fields_list)
			best_sensor=self.get_best_sensor(critical_field,sensor_list,cover,fields_list)
			self.best_sensor_to_cover(best_sensor, cover, fields_list, sensor_list)
		self.optimization(cover)
		procent=self.get_cover_procent(cover)
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


	def get_avaiable_targets(self):
		targets=[]
		# self.compute_sensors_targets(sensor_list)
		for target in self.target_list:
			for sensor in target.covering_sensors:

				if sensor.active==True:
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

		available_sensors=[]
		for sensor in critical_field.sensors:
			if sensor.active == True:
				available_sensors.append(sensor)
		max_value = self.get_sensor_value(available_sensors[0],uncovered_fields,critical_field,cover)
		max_sensor = available_sensors[0]
		available_sensors.remove(max_sensor)
		for sensor in available_sensors:
			sensor_value=self.get_sensor_value(sensor,uncovered_fields,critical_field,cover)
			if sensor_value>max_value:
				max_sensor=sensor
				max_value=sensor_value

		return max_sensor


	def get_sensor_value(self,sensor,uncovered_fields,critical_field,cover):
		value=0
		for field in sensor.fields:
			if field!=critical_field:
				if(field in uncovered_fields):
					value=value+len(field.targets)- (len(field.sensors)-1)
				else:
					sensors_from_cover_number=self.sensors_from_cover_number(field,cover)
					value=value-len(self.sensor_list)-sensors_from_cover_number+len(field.sensors)
		return value

	def sensors_from_cover_number(self, field,cover):
		number=0
		for sensor in cover:
			if field in sensor.fields:
				number=number+1
		return number

	def optimization(self, cover):
		#usuwa sensory ktorych wyłączenie nie zmienia poziomu pokrycia
		# fields_list=set()
		# for sensor in cover:
		# 	fields_list.update(sensor.fields)
		# value=len(fields_list)
		# for sensor in cover:
		# 	fields_list = set()
		# 	for sensor2 in cover:
		# 		if sensor!=sensor2:
		# 			fields_list.update(sensor2.fields)
		# 	if value==len(fields_list):
		# 		cover.remove(sensor)
		#usuwamy maksymalną liczbe sensorów by procent pokrycia był większy od q

		while(self.get_cover_procent(cover)>self.q):
			max_value=0
			max_sensor=None
			for sensor in cover:
				test_cover = cover.copy()
				test_sensor=sensor
				test_cover.remove(sensor)
				value=self.get_cover_procent(test_cover)
				if value>max_value:
					max_value=value
					max_sensor=test_sensor
			if max_value>=self.q:
				cover.remove(max_sensor)

			else:
				break





	def get_cover_targets(self,cover):
		targets=set()
		for sensor in cover:
			targets.update(sensor.covering_targets)
		return list(targets)
	def get_cover_procent(self,cover):
		return len(self.get_cover_targets(cover))/self.target_number*100

	def clean_cover(self, cover):
		"""
		czysci liste pól sensora
		:param cover:
		"""
		for sensor in cover:
			sensor.fields=[]


