from celery.decorators import task
from celery.utils.log import get_task_logger
import os
import sys
import requests
from bs4 import BeautifulSoup
import csv
from django.shortcuts import render_to_response
from django.http import HttpResponse
import simplejson
#raw_url = raw_input("Enter the Url to find data:")
#read_url = requests.get('http://www.bseindia.com/corporates/ann.aspx?expandable=3')
import dateutil.parser
import pandas as pd
import numpy as np
import csv,string
#import urllib2
#import pdb;pdb.set_trace()
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="web_scrapping_data_from_url",
    ignore_result=True
)


@task(name="web_scrapping_data_from_url")
def web_scrapping_data_from_url(self):

    codes =[]
    names_data = []
    #import pdb;pdb.set_trace()
    """read the content from the url"""
    url = 'http://www.bseindia.com/corporates/ann.aspx?expandable=3'
    r = requests.get(url)
    #soup = BeautifulSoup(r.text, 'lxml')
    #inmates_links = []
    #for table_row in soup.select(".inmatesList tr"):
    #with open('/root/Desktop/abc.html', 'r') as file:
    #    content = file.read()
    data = r.text
    soup = BeautifulSoup(data,'lxml')
    links = soup.find_all("a")
    temp_data = []
    general_data = soup.find_all('td', {'class': 'TTHeadergrey'})
    for item in general_data:
        try:
            elements = item.contents[2].string
            temp_data.append(elements)
            #print (temp_data)
        except:
            pass
    for item1 in general_data:
        try:
            iteritem = item1.contents[0].string
            if len(iteritem) > 17:
                temp_data.append(iteritem)
               # print (temp_data)
            else:
                continue
        except:
            pass
    for data in temp_data:
        try:
            o_cont = data.split('- ')
            s_code = o_cont[1]
            s_name = o_cont[0]
            extra = o_cont[2]
            codes.append(s_code)
            names_data.append(s_name)
            #print (codes)
            #print (names)
        except:
            pass
    #result = codes+names
    #print result


    return render_to_response('data_show.html',{'codes':codes,'names':names_data})



