#!/usr/bin/env python

import roslib; roslib.load_manifest('lu4r_ros')
import rospy
from lu4r_ros.srv import *

# host = ''
# port = 9009
# HEADERS = {'content-type': 'application/json'}


def parse_goal_server():
    rospy.init_node('lu4r_goal_parser')
    s = rospy.Service('parse_goal', parse_goal, handle_goal)
    rospy.logout("Service parse_goal_server called")
    rospy.spin()


def handle_goal(req):
    print(lu4r_json(req.sentence))


def lu4r_json(sentence):
    return sentence


if __name__ == '__main__':
    parse_goal_server()
