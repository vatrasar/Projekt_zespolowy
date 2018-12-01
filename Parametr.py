#!/usr/bin/python3
# -*- coding: utf-8 -*-f
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from Statistics import Statistic
import sys
import Scheduler
import Sensor
import Point
import Target
import math
from random import randrange
from PyQt5.QtGui import QPainter, QColor, QPaintEvent
from PyQt5.QtCore import QRect
import pygame
import os
from pygame import gfxdraw
import time

class Parametr(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.window_parametr()

	def window_parametr(self):
		label_amount_of_sensors = QLabel("Liczba sensorów", self)
		label_amount_of_targets = QLabel("Liczba celów", self)
		label_range_of_sensor = QLabel("Zasięg sensora", self)
		label_range_unit = QLabel("m", self)
		label_capacity = QLabel("Pojemność baterii", self)
		label_capacity_unit = QLabel("mAh", self)
		label_high = QLabel("Wysokość obszaru", self)
		label_high_unit = QLabel("m", self)
		label_width = QLabel("Szerokość obszaru", self)
		label_width_unit = QLabel("m", self)

		layoutT = QGridLayout()
		layoutT.addWidget(label_amount_of_sensors, 0, 0)
		layoutT.addWidget(label_amount_of_targets, 1, 0)
		layoutT.addWidget(label_range_of_sensor, 2, 0)
		layoutT.addWidget(label_range_unit, 2, 3)
		layoutT.addWidget(label_capacity, 3, 0)
		layoutT.addWidget(label_capacity_unit, 3, 3)
		layoutT.addWidget(label_high, 4, 0)
		layoutT.addWidget(label_high_unit, 4, 3)
		layoutT.addWidget(label_width, 5, 0)
		layoutT.addWidget(label_width_unit, 5, 3)

		self.amount_of_sensors = QLineEdit()
		self.amount_of_targets = QLineEdit()
		self.range_of_sensor = QLineEdit()
		self.capacity = QLineEdit()
		self.map_high = QLineEdit()
		self.map_width = QLineEdit()

		layoutT.addWidget(self.amount_of_sensors, 0, 1)
		layoutT.addWidget(self.amount_of_targets, 1, 1)
		layoutT.addWidget(self.range_of_sensor, 2, 1)
		layoutT.addWidget(self.capacity, 3, 1)
		layoutT.addWidget(self.map_high, 4, 1)
		layoutT.addWidget(self.map_width, 5, 1)

		symulateBtn = QPushButton("&Symuluj", self)
		closeBtn = QPushButton("&Koniec", self)
		closeBtn.resize(closeBtn.sizeHint())

		layoutT.addWidget(symulateBtn, 6, 0, 1, 3)
		layoutT.addWidget(closeBtn, 7, 0, 1, 3)

		self.setLayout(layoutT)

		closeBtn.clicked.connect(self.close)
		symulateBtn.clicked.connect(self.verification)

		self.amount_of_sensors.setFocus()
		self.setGeometry(100, 100, 300, 100)
		self.setWindowTitle("Symulacja")
		self.show()


	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.close()

	def symulate(self):
		self.close()
		pygame.init()
		pygame.font.init()
		self.font_path = pygame.font.match_font('avantgarde md bt')
		self.MAP_SIZE_H = 700
		self.MAP_SIZE_W = 1000
		self.MENU_W = 400
		if self.map_high > self.map_width or (self.MAP_SIZE_W / self.map_width) * self.map_high > self.MAP_SIZE_H:
			self.scaled = (float)(self.MAP_SIZE_H / self.map_high)
		else:
			self.scaled = (float)(self.MAP_SIZE_W / self.map_width)
		self.area = pygame.display.set_mode(((int)(self.map_width * self.scaled + self.MENU_W), (int)(self.map_high * self.scaled)), 0, 32)
		pygame.display.set_caption('Symulacja')
		scheduler = Scheduler.Scheduler(self.sensor_list, self.target_list, self.range_of_sensor, self)
		scheduler.run()
		self.duration = scheduler.duration
		self.statistics()


	def statistics(self):
		x = 100
		y = 100
		WIDTH = 300
		HIGH = 300
		self.font_path = pygame.font.match_font('arial', True)
		screen = pygame.display.set_mode((WIDTH, HIGH))
		pygame.display.set_caption('Statystyki')
		self.font = pygame.font.Font(self.font_path, 15)
		self.draw_text(screen, "Statystyki", WIDTH/2, 10)
		self.font = pygame.font.Font(self.font_path, 13)
		self.draw_text(screen, "Liczba aktywnych sensorów "+str(self.amount_of_active_sensors), WIDTH/2, self.MENU_H*2)
		self.draw_text(screen, "Liczba nieaktywnych sensorów "+str(self.amount_of_disactive_sensors), WIDTH/2, self.MENU_H*3)
		self.draw_text(screen, "Liczba naładowanych sensorów "+str(self.amount_of_charged_sensors), WIDTH/2, self.MENU_H*4)
		self.draw_text(screen, "Liczba rozładowanych sensorów "+str(self.amount_of_discharged_sensors), WIDTH/2, self.MENU_H*5)
		self.draw_text(screen, "Czas życia sieci sensorowej "+str(self.scheduler.statistics.get_simulation_time()), WIDTH/2, self.MENU_H*6)

		pygame.display.update()

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

	def draw_text(self, surface,  text, x, y):
		text = self.font.render(text, True, (255, 255, 255))
		rect = text.get_rect()
		rect.center = x, y
		surface.blit(text, rect)
        
	def verification(self):
		try:
			self.UPPER_RANGE_BOUND = 100
			self.UPPER_CAPACITY_BOUND = 10
			self.UPPER_HIGH_BOUND = 1000
			self.UPPER_WIDTH_BOUND = 1000
			amount_of_sensors = int(self.amount_of_sensors.text())
			amount_of_targets = int(self.amount_of_targets.text())
			range_of_sensor = float(self.range_of_sensor.text())
			capacity = float(self.capacity.text())
			map_high = float(self.map_high.text())
			map_width = float(self.map_width.text())
			if amount_of_sensors <= 0 or amount_of_sensors > sys.float_info.max:
				QMessageBox.critical(self, "Błąd", "Podaj liczbę sensorów większą od 0.")
				return
			if amount_of_targets <= 0 or amount_of_targets > sys.float_info.max:
				QMessageBox.critical(self, "Błąd", "Podaj liczbę celów większą od 0.")
				return
			if range_of_sensor <= 0 or range_of_sensor > self.UPPER_RANGE_BOUND:
				QMessageBox.critical(self, "Błąd", "Podaj zasięg sensora większy od 0 i mniejszą od "+str(self.UPPER_RANGE_BOUND))
				return
			if capacity <= 0 or capacity > self.UPPER_CAPACITY_BOUND:
				QMessageBox.critical(self, "Błąd", "Podaj pojemność baterii sensora większą od 0 i mniejszą lub równą "+str(self.UPPER_CAPACITY_BOUND))
				return
			if map_high <= 0 or map_high > self.UPPER_HIGH_BOUND:
				QMessageBox.critical(self, "Błąd", "Podaj pojemność baterii sensora większą od 0 i mniejszą lub równą "+str(self.UPPER_HIGH_BOUND))
				return
			if map_width <= 0 or map_width > self.UPPER_WIDTH_BOUND:
				QMessageBox.critical(self, "Błąd", "Podaj pojemność baterii sensora większą od 0 i mniejszą lub równą "+str(self.UPPER_WIDTH_BOUND))
				return
		except ValueError:
			QMessageBox.warning(self, "Błąd", "Błędne dane", QMessageBox.Ok)
		self.var_init(amount_of_sensors, amount_of_targets, range_of_sensor, capacity, map_high, map_width)
		self.symulate()
		return

	def var_init(self, amount_of_sensors, amount_of_targets, range_of_sensor, capacity, map_high, map_width):
		self.amount_of_sensors = amount_of_sensors
		self.amount_of_targets = amount_of_targets
		self.range_of_sensor = range_of_sensor
		self.capacity = capacity
		self.map_high = map_high
		self.map_width = map_width
		self.sensor_list = []
		self.target_list = []

		for x in range(0, amount_of_sensors):
			self.sensor_list.append(Sensor.Sensor(capacity, 
			range_of_sensor, Point.Point(randrange(range_of_sensor, 
			map_width-range_of_sensor),randrange(range_of_sensor, map_high-range_of_sensor))))
		for x in range(0, amount_of_targets):
			self.target_list.append(
				Target.Target(Point.Point(randrange(map_width - 2 * 0.1 * map_width) + 0.1 * map_width,randrange(map_high - 2 * 0.1 * map_high) + 0.1 * map_width)))

	def paint(self, scheduler):
		self.amount_of_active_sensors = 0
		self.amount_of_charged_sensors = 0
		self.scheduler = scheduler
		self.MENU_H = 15
		self.area.fill((0,0,0))
		for x in range(0, self.amount_of_sensors):
			if scheduler.sensor_list[x].active == True:
				self.amount_of_active_sensors += 1
				pygame.draw.circle(self.area, (0, 51, 51), (self.scheduler.sensor_list[x].localization.__mul__(self.scaled).integerize()), int(self.scheduler.sensor_range*self.scaled), 0)
			else:
				pygame.draw.circle(self.area, (30, 30, 47), (self.scheduler.sensor_list[x].localization.__mul__(self.scaled).integerize()), int(self.scheduler.sensor_range*self.scaled), 1)
			if scheduler.sensor_list[x].battery > 0:
				self.amount_of_charged_sensors +=1
		for x in range(0, self.amount_of_sensors):
			if self.scheduler.sensor_list[x].active == True:
				pygame.draw.circle(self.area, (204, 255, 238), (self.scheduler.sensor_list[x].localization.__mul__(self.scaled).integerize()), int(self.scheduler.sensor_range*self.scaled), 1)
		for x in range(0, self.amount_of_targets):
			gfxdraw.pixel(self.area, int(self.scheduler.target_list[x].localization.return_x()*self.scaled), int(self.scheduler.target_list[x].localization.return_y()*self.scaled), (255, 51, 51))

		self.amount_of_disactive_sensors = self.amount_of_sensors - self.amount_of_active_sensors
		self.amount_of_discharged_sensors = self.amount_of_sensors - self.amount_of_charged_sensors
		self.font = pygame.font.Font(self.font_path, 20)
		self.draw_text(self.area, "Symulacja", self.map_width*self.scaled+int(self.MENU_W/2), self.MENU_H)
		self.font = pygame.font.Font(self.font_path, 18)
		self.draw_text(self.area, "Liczba aktywnych sensorów "+str(self.amount_of_active_sensors), self.map_width*self.scaled+int(self.MENU_W/2), self.MENU_H*2)
		self.draw_text(self.area, "Liczba nieaktywnych sensorów "+str(self.amount_of_disactive_sensors), self.map_width*self.scaled+int(self.MENU_W/2), self.MENU_H*3)
		self.draw_text(self.area, "Liczba naładowanych sensorów "+str(self.amount_of_charged_sensors), self.map_width*self.scaled+int(self.MENU_W/2), self.MENU_H*4)
		self.draw_text(self.area, "Liczba rozładowanych sensorów "+str(self.amount_of_discharged_sensors), self.map_width*self.scaled+int(self.MENU_W/2), self.MENU_H*5)
		self.draw_text(self.area, "Obserwowane cele "+str(self.scheduler.get_percent_observed_targets())+"%", self.map_width*self.scaled+int(self.MENU_W/2), self.MENU_H*6)

		pygame.display.update()



if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	getting_parametrs = Parametr()
	sys.exit(app.exec_())
