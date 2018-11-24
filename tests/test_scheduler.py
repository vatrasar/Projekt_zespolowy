import pytest
from Scheduler import Scheduler
from Sensor import Sensor
from Point import Point
from Target import Target


def test_compute_sensors_targets():
    sen1=Sensor(2,2,Point(0,0))
    tar1=Target(Point(1,1))
    tar2=Target(Point(4,4))
    sensor_list=[sen1]
    targest_list=[tar1,tar2]
    a=Scheduler(sensor_list,targest_list,2,2)
    assert len(a.sensor_list[0].covering_targets)==1


def test_set_sensor_state():
    sen1 = Sensor(2, 2, Point(0, 0))
    sen2 = Sensor(2, 2, Point(8, 5))
    sen2.active=False
    tar1 = Target(Point(1, 1))
    tar2 = Target(Point(4, 4))
    sensor_list = [sen1,sen2]
    targest_list = [tar1, tar2]
    a = Scheduler(sensor_list, targest_list, 2, 2)
    a.set_sensor_state(sen2,True)
    assert a.sensor_list[1].active==True
