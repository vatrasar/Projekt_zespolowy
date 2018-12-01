import pytest
from Scheduler import Scheduler
from Sensor import Sensor
from Point import Point
from Target import Target

def build_scheduler(sen,tar):
    sen1 = Sensor(2, 2, Point(0, 0))
    sen2 = Sensor(2, 2, Point(1, 0))
    tar1 = Target(Point(1, 1))
    tar4 = Target(Point(0, 1))
    tar2 = Target(Point(2.5, 0))
    tar3 = Target(Point(8, 8))
    target_list = [tar1, tar2, tar3, tar4]
    sensor_list = [sen1, sen2]
    for sensor in sen:
        sensor_list.append(sensor)
    for target in tar:
        sensor_list.append(target)
    a = Scheduler(sensor_list, target_list, 2, 2)
    return a

def test_build_fields_list():

    sen1 = Sensor(2, 2, Point(0, 0))
    sen2 = Sensor(2, 2, Point(1, 0))
    tar1 = Target(Point(1, 1))
    tar4 = Target(Point(0, 1))
    tar2 = Target(Point(2.5, 0))
    tar3 = Target(Point(8, 8))
    target_list = [tar1, tar2, tar3, tar4]
    sensor_list = [sen1, sen2]
    a = Scheduler(sensor_list, target_list, 2, 2)
    assert len(a.fields_list)==2
    assert len(sen1.fields)==1
    assert len(sen2.fields)==2
    assert len(sen1.fields[0].targets)==2

def test_get_avaiable_targets():

    sen=Sensor(2, 2, Point(-1, 0))
    a=build_scheduler(sen=[sen],tar=[])
    targets=a.get_avaiable_targets(a.sensor_list)
    assert len(targets)==3
    assert len(a.target_list[3].covering_sensors)==3
    sen1 = Sensor(2, 2, Point(0, 0))
    sen2 = Sensor(2, 2, Point(1, 0))
    sensor_list = [sen1, sen2]
    a.compute_sensors_targets(sensor_list)
    assert len(a.target_list[3].covering_sensors) == 2
def test_goal_achieved():
    a=build_scheduler([],[])
    assert a.goal_achieved(a.sensor_list)
def test_get_critical_field():
    sen=Sensor(2, 2, Point(8, 7))
    a = build_scheduler(sen=[Sensor(2, 2, Point(3, 0)),sen], tar=[])
    field=a.get_critical_field(a.fields_list)
    assert field==sen.fields[0]

def test_sensors_from_cover_number():
    sen3 = Sensor(2, 2, Point(8, 1))
    a=build_scheduler([sen3],[])
    sen1=a.sensor_list[0]
    sen2=a.sensor_list[1]

    number=a.sensors_from_cover_number(a.fields_list[0],[sen1,sen2,sen3])
    assert number==2
def test_get_best_sensor():
    a = build_scheduler([], [])
    sensor=a.get_best_sensor(a.fields_list[0],a.sensor_list,[],a.fields_list)
    assert sensor==Sensor(2, 2, Point(1, 0))
def test_get_covers_list():
    sen1=Sensor(2, 2, Point(8, 9))
    a=build_scheduler([sen1],[])
    covers=a.get_covers_list()
    assert len(covers)==2
def test_get_cover_procent():
    a=build_scheduler([],[])
    assert a.get_cover_procent([a.sensor_list[0]])==50






