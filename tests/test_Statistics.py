import pytest
import Statistics
from Sensor import Sensor
from Point import Point
from Target import Target
from Scheduler import Scheduler

def test_get_active_sensors_number():
    a=Statistics.Statistic([1,2],[])
    a.sensors=[Sensor(2,2,2),Sensor(2,2,2),Sensor(2,2,2)]
    a.sensors[1].active=False
    assert a.get_active_sensors_number()==2

def test_get_charged_sensors():
    a = Statistics.Statistic([1, 2],[])
    a.sensors = [Sensor(0, 2, 2), Sensor(2, 2, 2), Sensor(2, 2, 2)]
    assert a.get_charged_sensors_count() == 2

def test_get_percent_observed_targets():
    sen1 = Sensor(2, 2, Point(0, 0))
    sen2 = Sensor(2, 2, Point(1, 0))
    tar1 = Target(Point(1, 1))
    tar2 = Target(Point(4, 4))
    tar4 = Target(Point(5, 5))
    tar3 = Target(Point(3, 0))
    sensor_list = [sen1,sen2]
    targest_list = [tar1, tar2,tar3,tar4]
    a = Scheduler(sensor_list, targest_list, 2, 2)
    assert a.get_percent_observed_targets() == 50

