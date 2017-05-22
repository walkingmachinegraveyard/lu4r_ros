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
import re

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
    lu4r_port = rospy.get_param('~lu4r_port', '9001')
    lu4r_url = 'http://' + str(lu4r_ip) + ':' + str(lu4r_port) + '/service/nlu'

    r = lu4r_json(req.sentence, lu4r_url)
    lu4rList = []
    lu4rItem = Lu4r()
    lu4rList.append(lu4rItem)

    for line in r.iter_lines():
        if line:
            print line
            operation = re.compile('(\s*:op\d\s)?\([a-zA-Z0-9\-]+ / ([a-zA-Z\-]+)')
            m = operation.match(line)
            if m:
                if lu4rItem.action != "" and lu4rItem.action != 'and':
                    lu4rList.append(lu4rItem)
                lu4rItem = Lu4r()
                lu4rItem.action = m.group(2)
            else:
                action = re.compile('\s*:([a-zA-Z0-9]*) \([a-zA-Z0-9]* / ([a-zA-Z0-9]*)\)')
                n = action.match(line)
                if n:
                    lu4rItem.args.append((n.group(1), n.group(2)))

    if lu4rItem.action != "":
        lu4rList.append(lu4rItem)

    print lu4rList

    return lu4rList

def lu4r_json(sentence, url):
    HYPO = {'hypotheses':[{"transcription":sentence,"confidence":"0.9","rank":"1"}]}
    ENT = {'entities': [{"atom":"book1","type":"book","preferredLexicalReference":"book","alternativeLexicalReferences":["volume","manual","dictionary","text"],"coordinate":{"x":"13.0","y":"0.0","z":"0.0","angle":"0"}},{"atom":"table1","type":"table","preferredLexicalReference":"table","alternativeLexicalReferences":["counter","desk"],"coordinate":{"x":"16.0","y":"0.0","z":"0.0","angle":"0.671"}},{"atom":"glass1","type":"glass","preferredLexicalReference":"glass","alternativeLexicalReferences":["cup","decanter","chalice"],"coordinate":{"x":"5.0","y":"8.0","z":"0.0","angle":"0"}},{"atom":"bedroom1","type":"bedroom","preferredLexicalReference":"bedroom","alternativeLexicalReferences":["chamber","cubicle","bedchamber"],"coordinate":{"x":"11.0","y":"6.0","z":"0.0","angle":"0"}},{"atom":"studio1","type":"studio","preferredLexicalReference":"studio","alternativeLexicalReferences":["library","office"],"coordinate":{"x":"9.0","y":"14.0","z":"0.0","angle":"0"}},{"atom":"person1","type":"person","preferredLexicalReference":"person","alternativeLexicalReferences":["body","character","guy","man","woman"],"coordinate":{"x":"2.0","y":"2.0","z":"0.0","angle":"0"}}]}
    r = requests.post(url, data={'hypo':str(HYPO) , 'entities':str(ENT)}, headers=HEADERS)

    return r

if __name__ == '__main__':
    parse_goal_server()
