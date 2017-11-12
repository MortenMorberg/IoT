'''
Created on 9. nov. 2017

@author: Andersen
'''
import local.topic
import time
from local.topic import getid, getsize


my_topic = local.topic.gettopic(122, 0)
print(getid(my_topic))
print(getsize(my_topic))
time.sleep(1)
print(local.topic.gettimediff(my_topic, time.time()))
