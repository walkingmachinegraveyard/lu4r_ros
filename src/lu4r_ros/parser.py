#!/usr/bin/env python
# encoding=utf8

import roslib; roslib.load_manifest('lu4r_ros')
import rospy
from lu4r_ros.srv import *
from lu4r_ros.msg import *
import socket
import sys
import requests
import json


reload(sys)
sys.setdefaultencoding('utf8')
semantic_map = {}
HEADERS = {'content-type': 'application/json'}


def parse_goal_server():
    global semantic_map
    rospy.init_node('lu4r_goal_parser')
    s = rospy.Service('parse_goal', parse_goal, handle_goal)
    rospy.logout("Service parse_goal_server called")
    rospy.spin()


def handle_goal(req):
    lu4r_ip = rospy.get_param("~lu4r_ip", '127.0.0.1')
    lu4r_port = rospy.get_param('~lu4r_port', '1000')
    lu4r_url = 'http://' + lu4r_ip + ':' + str(lu4r_port) + '/service/nlu'

    lu4r_json(req.sentence, lu4r_url)


def lu4r_json(sentence, url):
    to_send = {'hypo': "Go get the book on the shelf", 'entities': [{"atom":"book1","type":"book","preferredLexicalReference":"book","alternativeLexicalReferences":["volume","manual","dictionary","text"],"coordinate":{"x":"13.0","y":"0.0","z":"0.0","angle":"0"}},{"atom":"table1","type":"table","preferredLexicalReference":"table","alternativeLexicalReferences":["counter","desk"],"coordinate":{"x":"16.0","y":"0.0","z":"0.0","angle":"0.671"}},{"atom":"glass1","type":"glass","preferredLexicalReference":"glass","alternativeLexicalReferences":["cup","decanter","chalice"],"coordinate":{"x":"5.0","y":"8.0","z":"0.0","angle":"0"}},{"atom":"bedroom1","type":"bedroom","preferredLexicalReference":"bedroom","alternativeLexicalReferences":["chamber","cubicle","bedchamber"],"coordinate":{"x":"11.0","y":"6.0","z":"0.0","angle":"0"}},{"atom":"studio1","type":"studio","preferredLexicalReference":"studio","alternativeLexicalReferences":["library","office"],"coordinate":{"x":"9.0","y":"14.0","z":"0.0","angle":"0"}},{"atom":"person1","type":"person","preferredLexicalReference":"person","alternativeLexicalReferences":["body","character","guy","man","woman"],"coordinate":{"x":"2.0","y":"2.0","z":"0.0","angle":"0"}}]}
    r = requests.post(url, to_send, headers=HEADERS)
    print r


if __name__ == '__main__':
    parse_goal_server()
