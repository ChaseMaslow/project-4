"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

from acp_times import open_time, close_time
import arrow

import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def test_open():
    start_time = arrow.now()
    assert open_time(60, 200, start_time) == start_time.shift(hours=+1, minutes=+46)


def test_close():
    start_time = arrow.now()
    assert close_time(60, 200, start_time) == start_time.shift(hours=+4)


def test_600():
    """
    Test based on example 2 at: https://rusa.org/pages/acp-brevet-control-times-calculator
    600km brevet, check controls at 100km, 200km, 350km, and 550km
    """
    brevet_distance = 600
    control_distances = [100, 200, 350, 550, 600]
    fmt = 'YYYY-MM-DD HH:mm:ss'
    start_time = arrow.get('2022-02-03 09:00:00', fmt)
    expected_times = [  ( start_time.replace(hour=11, minute=56) , 
                        start_time.replace(hour=15, minute=40) ) ,
                        ( start_time.replace(hour=14, minute=53) , 
                        start_time.replace(hour=22, minute=20) ) ,
                        ( start_time.replace(hour=19, minute=34) , 
                        start_time.replace(day = 4, hour=8, minute=20) ) ,
                        ( start_time.replace(day = 4, hour=2, minute=8) , 
                        start_time.replace(day = 4, hour=21, minute=40) ) ,
                        ( start_time.replace(day = 4, hour=3, minute=48) , 
                        start_time.replace(day = 5, hour=1, minute=0) )
    ]
    
    for c in range(len(control_distances)):
        ot = open_time(control_distances[c], brevet_distance, start_time)
        ct = close_time(control_distances[c], brevet_distance, start_time)
        log.debug(f"Expected {expected_times[c][0]}, got {ot}")
        assert ot == expected_times[c][0]
        log.debug(f"Expected {expected_times[c][1]}, got {ct}")
        assert ct == expected_times[c][1]


def test_relaxed_close():
    start_time = arrow.now()
    ct = close_time(20, 200, start_time)
    log.debug(f"Expected {start_time.shift(hours=+2)}, got {ct}")
    assert ct == start_time.shift(hours=+2)


def test_truncate():
    start_time = arrow.get('2022-02-03 09:00:00', 'YYYY-MM-DD HH:mm:ss')
    ot = open_time(38.624256, 200, start_time)
    ct = close_time(38.624256, 200, start_time)
    assert ot == start_time.shift(hours=+1, minutes=+7)
    assert ct == start_time.shift(hours=+2, minutes=+54)