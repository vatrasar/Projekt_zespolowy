import pytest
import matplotlib.pyplot as plt
from Scheduler import Scheduler
from Sensor import Sensor
from Point import Point
from Target import Target
from graph import Node
import networkx as nx




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
    a.sensor_list[1].set_sensor_state(True)
    assert a.sensor_list[1].active==True


def test_build_graph():
    a = build_scheduler()
    G = a.build_G_graph()
    assert G.nodes[a.sensor_list[0]]["type"]=="sensor"
    assert G.get_edge_data(a.sensor_list[0],a.sensor_list[0].covering_targets[0])["active"]==False
    draw_graph(G, a.sensor_list)
    assert Target(Point(1,1)).__hash__()==Target(Point(1,1)).__hash__()
    assert G.has_node(Target(Point(1, 1)))

def test_get_critical_number():
    a=build_scheduler()
    G = a.build_G_graph()
    assert a.get_critical_number(G)==1




def build_scheduler():
    sen1 = Sensor(2, 2, Point(0, 0))
    sen2 = Sensor(2, 2, Point(1, 0))
    tar1 = Target(Point(1, 1))
    tar2 = Target(Point(4, 4))
    tar4 = Target(Point(5, 5))
    tar3 = Target(Point(3, 0))
    tar5 = Target(Point(0, 1))
    tar6 = Target(Point(0, -1))
    tar7 = Target(Point(2, 1))
    sensor_list = [sen1, sen2]
    targest_list = [tar1, tar2, tar3, tar4, tar5, tar6, tar7]
    a = Scheduler(sensor_list, targest_list, 2, 2)
    return a

def build_scheduler2():
    sen1 = Sensor(2, 2, Point(0, 0))
    sen2 = Sensor(2, 2, Point(1, 0))
    sen3 = Sensor(2, 2, Point(4, 5))
    tar1 = Target(Point(1, 1))
    tar2 = Target(Point(4, 4))
    tar4 = Target(Point(5, 5))
    tar3 = Target(Point(3, 0))
    tar5 = Target(Point(0, 1))
    tar6 = Target(Point(0, -1))
    tar7 = Target(Point(2, 1))
    sensor_list = [sen1, sen2,sen3]
    targest_list = [tar1, tar2, tar3, tar4, tar5, tar6, tar7]
    a = Scheduler(sensor_list, targest_list, 2, 2)
    return a


def draw_graph(G, sensor_list):
    labels = {}
    for sensor in sensor_list:
        labels[sensor] = "sensor "+ str(sensor.localization)
        for target in sensor.covering_targets:
            labels[target]="target "+str(target.localization)
    nx.draw(G, with_labels=True,labels=labels)
    plt.show()

def test_compute_flow_value():
    a=build_scheduler()
    G=a.build_G_graph()
    # draw_graph(G,a.sensor_list)
    for sensor in a.sensor_list:
        a.change_sensor_state(G,sensor,True)
    for target in a.target_list:
        if G.has_node(target):
            print(str(target.localization)+":"+str(a.compute_flow_value(G,target)))
    y1,y2=a.add_Y_nodes(G)
    assert a.compute_flow_value(G,y1)==3
    assert a.compute_flow_value(G, y2) == 5
    assert G.node[y1]["type"] == "Y1"



def test_add_Y_nodes():
    a=build_scheduler()
    G=a.build_G_graph()
    y1,y2=a.add_Y_nodes(G)
    assert G.has_node(y1)
    assert (y1,y2)==(Node(1),Node(2))

def test_change_sensor_state():
    a = build_scheduler()
    G = a.build_G_graph()
    a.change_sensor_state(G,a.sensor_list[0],True)
    assert G.get_edge_data(a.sensor_list[0],a.sensor_list[0].covering_targets[0])["active"]==True
    a.change_sensor_state(G, a.sensor_list[0], False)
    assert G.get_edge_data(a.sensor_list[0], a.sensor_list[0].covering_targets[0])["active"] == False

def test_get_one_sensor_targets():
    sen1 = Sensor(2, 2, Point(0, 0))
    sen2 = Sensor(2, 2, Point(1, 0))
    sen3 = Sensor(2, 2, Point(5, 4))
    tar1 = Target(Point(1, 1))
    tar2 = Target(Point(4, 4))
    tar4 = Target(Point(5, 5))
    tar3 = Target(Point(3, 0))
    tar5 = Target(Point(0, 1))
    tar6 = Target(Point(0, -1))
    tar7 = Target(Point(2, 1))
    sensor_list = [sen1, sen2,sen3]
    targest_list = [tar1, tar2, tar3, tar4, tar5, tar6, tar7]
    a = Scheduler(sensor_list, targest_list, 2, 2)
    result=a.get_one_sensor_targets()[0]
    assert result==tar4 or result==tar2

def test_get_best_cover():
    lista1 = [1, 2, 3, 4]
    lista2 = [1, 4]
    lista3 = list(filter(lambda x: x not in lista2, lista1))
    assert len(lista3) == 2
    a=build_scheduler2()
    G=a.build_G_graph()
    y1,y2=a.add_Y_nodes(G)
    cover=a.get_best_cover(G,y1,y2,a.sensor_list)
    draw_graph(G,a.sensor_list)
    for sor in cover:
        print(sor.localization)
    assert cover[1]==Sensor(2, 2, Point(4, 5)) or cover[0]==Sensor(2, 2, Point(4, 5))
    assert len(cover)==2

