import pytest
from Scheduler import Scheduler
from Sensor import Sensor
from Point import Point
from Target import Target
import numpy as np
from scipy.spatial import distance

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

    sen=Sensor(2, 2, Point(8, 9))
    a=build_scheduler(sen=[sen],tar=[])
    targets=a.get_avaiable_targets()
    assert len(targets)==4
    assert len(a.get_avaiable_targets())==4
    sen.active=False
    assert len(a.get_avaiable_targets()) == 3

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
    assert len(covers)==1
def test_get_cover_procent():
    a=build_scheduler([],[])
    assert a.get_cover_procent([a.sensor_list[0]])==50


def points_to_numpy(nodes):
    points_list = []
    for node in nodes:
        points_list.append(node.as_tuple())
    numpy_array=np.array(points_list)
    return numpy_array


def test_distance():
   point1=Point(0,0)
   point2=Point(4,5)
   point3=Point(23,15)
   # nodes=[point2,point3]
   # points=points_to_numpy(nodes)
   # result=[point1.distance_to(point2),point1.distance_to(point3)]
   a=[point3,point2,point1]
   b=[point1,point2]
   a[2].y=10
   assert b[0].y==10





def get_indexs_of(pt_1, ):
    pt_1 = np.array((pt_1[0], pt_1[1]))










