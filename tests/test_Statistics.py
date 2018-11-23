import pytest
import Statistics
import Sensor



def test_get_active_sensors_number():
    a=Statistics.Statistic((1,2))
    a.sensors=[Sensor.Sensor(2,2,2),Sensor.Sensor(2,2,2),Sensor.Sensor(2,2,2)]
    a.sensors[1].active=False
    assert a.get_active_sensors_number()==2

def test_get_charged_sensors():
    a = Statistics.Statistic((1, 2))
    a.sensors = [Sensor.Sensor(0, 2, 2), Sensor.Sensor(2, 2, 2), Sensor.Sensor(2, 2, 2)]
    assert a.get_charged_sensors() == 2


