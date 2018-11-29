import pytest
from Scheduler import Scheduler
from Sensor import Sensor
from Point import Point
from Target import Target


def test_build_fields_list():
    sen1=Sensor(2,2,Point(0,0))
    sen2=Sensor(2,2,Point(1,0))
    tar1=Target(Point(1,1))
    tar4=Target(Point(0,1))
    tar2 = Target(Point(2.5, 0))
    tar3=Target(Point(8,8))
    target_list=[tar1,tar2,tar3,tar4]
    sensor_list=[sen1,sen2]
    a=Scheduler(sensor_list,target_list,2,2)
    assert len(a.fields_list)==2
    assert len(sen1.fields)==1
    assert len(sen2.fields)==2
    assert len(sen1.fields[0].targets)==2







