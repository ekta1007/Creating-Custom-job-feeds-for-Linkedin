#building list of urls to build custom job feed to pass into the TF-IDF NLTK file
# To do error handling for urls not found and similar jobs etc..
# Explore & compare the similar logic with linkedin's REST API

# Author : Ekta Grover, ekta1007@gmail.com

import os
import nltk, re
import socket
import matplotlib
#from urllib import urlopen
import csv
import urllib2
import urllib

#os.environ['http_proxy']=''
list_url=[]
m=0
company_name=[]
Title_Position=[]
posted_date=[]
Functions=[]
Industries=[]

#Y1=range(1000000:2000000)
#Y2=range(6000000:6999999)
    #temp="http://www.linkedin.com/jobs?viewJob=&jobId="+str(Y2[k])+"&trk=rj_jshp"

url1=["http://www.linkedin.com/jobs?jobId=6836724&viewJob=&trk=rj_jshp", "http://www.linkedin.com/jobs?viewJob=&jobId=6175979&trk=rj_jshp", "http://www.linkedin.com/jobs?viewJob=&jobId=6723434&trk=rj_jshp" , "http://www.linkedin.com/jobs?viewJob=&jobId=6052768&trk=rj_jshp","http://www.linkedin.com/jobs?viewJob=&jobId=69999&trk=rj_jshp","http://www.linkedin.com/jobs?viewJob=&jobId=6&trk=rj_jshp"]

#for k in range(0,len(Y2)):
    #temp="http://www.linkedin.com/jobs?viewJob=&jobId="+str(Y2[k])+"&trk=rj_jshp"
for k1 in range(0,len(url1)):
    html = urllib.urlopen(url1[k1]).read()
    raw = nltk.clean_html(html)
    if (raw.find("The job you&#8217;re looking for is no longer active")>=1 or raw.find("We can&#8217;t find the job you&#8217;re looking for")>=1):
        pass
    elif (raw.find("Bangalore")!=-1 or raw.find("Bengaluru")!=-1):
        print 'going here'
        # appending only "local" jobs and job posted in August
        # not filtering by "recency" which can be had from "Posted" field, since if the job does not display "no longer active" means, it must be active
        list_url.append(url1[k1])
        Title_Position.append(raw.split("\n")[0].strip())
        index_begin=Title_Position[m].find(" at ")
        index_end=Title_Position[m].find(" in ")
        #index bewteen at and in else "N/A"
        if index_begin !=-1 and index_end !=-1 :
            company_name.append(Title_Position[m][index_begin+4:index_end].strip())
        else :
            company_name.append("NA")    
        #index bewteen at and in else "N/A"
        #finding posted on - pattern  Posted: \n  August 2, 2013 \n\n  Type
        index_begin=raw.find("Posted: ")
        index_end=raw.find("Type:")
        if index_begin !=-1 and index_end !=-1 :
            posted_date.append(raw[index_begin+8:index_end].replace("\n","").strip())
        else :
            posted_date.append("NA") 
        #Functions & Industries
        index_begin=raw.find("Functions: ")
        index_end=raw.find("Industries:")
        if index_begin !=-1 and index_end !=-1 :
            Functions.append(raw[index_begin+11:index_end].replace("\n","").strip())
        else :
            Functions.append("NA") 
        #industries
        index_begin=raw.find("Industries:")
        index_end=raw.find("Job ID:")
        if index_begin !=-1 and index_end !=-1 :
            Industries.append(raw[index_begin+11:index_end].replace("\n","").strip())
        else :
            Industries.append("NA")
                    #similar jobs
            """index_begin=raw.find("Similar Jobs")
        index_end=raw.find("Sign in to view similar jobs")
            if index_begin !=-1 and index_end !=-1 :
                Industries.append(raw(index_begin+12:index_end).replace("\n","").strip())
            else :
                Industries.append("NA") """
    m=m+1
if len(list_url)<1:
    print "no Active job in this list"
#else print the list of active jobs in a csv file
else :
    mywriter = csv.writer(open("C:\Users\ekta\Desktop\LinkedinCustomJobFeed.csv", "wb"))
    head = ("Company Name","Title of Position", "Job Posting Url", "Posted on","Functions","Industry")
    mywriter.writerow(head)
    for i in range(0,len(list_url)):
        mywriter.writerow([company_name[i],Title_Position[i],list_url[i],posted_date[i],Functions[i],Industries[i]])
    print ' Finished writing the csv file '



    
