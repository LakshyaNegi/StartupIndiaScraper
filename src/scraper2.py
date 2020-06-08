#id
#company name
#industry
#sector
#stage
#state
#website
#team info
#address
#contact info
#notes

import time
import csv
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")


def goToPage(link):

    browser = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=options)
    
    try:
        browser.get(link)
        time.sleep(3)
        
        head_div = browser.find_elements_by_class_name("company-name")[0]
        
        
        try:
            cname = head_div.find_element_by_tag_name("p").text.replace(';',' ')
        except:
            cname = ""

        try:
            clink = head_div.find_element_by_tag_name("a").get_attribute("href")
        except:
            clink = ""

        try:
            cmail = head_div.find_element_by_class_name("mail").text.replace(';',' ')
        except:
            cmail = ""

            
        try:
            info = browser.find_elements_by_class_name("content")
            cstage = info[0].text.replace(';',' ')
            cindustry = info[1].text.replace(';',' ')
            csector = info[2].text.replace(';',' ')
            cservice = info[3].text.replace(';',' ')
            clocation = info[4].text.replace(';',' ')
            cyears = info[5].text.replace(';',' ')
        except Exception as e:
            print(e)
            info = ""
            cstage = ""
            cindustry = ""
            csector = ""
            cservice = ""
            clocation = ""
            cyears = ""
            print("error : info out of bound")

        try:
            ccity,cstate = clocation.split(',')
        except:
            ccity = ""
            try:
                cstate = clocation
            except:
                cstate = ""


        try:
            fdiv = browser.find_elements_by_class_name("member-info")[0]
            fname = fdiv.find_element_by_tag_name("h4").text.replace(';',' ')
            frole = fdiv.find_element_by_tag_name("span").text.replace(';',' ')
        except:
            fname=""
            frole=""

        #team = []
        #t = {}

        try:
            members = browser.find_elements_by_class_name("member")
        except:
            members = []

        memname = ["","","","",""]
        memrole = ["","","","",""]
        memlinkedin = ["","","","",""]

        #print(len(members))
        try:
            for m,member in enumerate(members):
                if(m>5):
                    break
                try:
                    mem = json.loads(member.get_attribute("data-member"))
                except:
                    mem ={}
                #print(json)
                try:
                    mname = mem['name'].replace(';',' ')
                except:
                    mname = ""
                        
                try:
                    mrole = mem['role'].replace(';',' ')
                except:
                    mrole = ""

                #print(m)

                memname[m] = mname
                memrole[m] = mrole
            
                    
                mlinkedin = ""
                #mtwitter = ""
                try:
                    socialInfo = mem['socialInfos']
                except:
                    socialInfo = []

                for social in socialInfo:
                    if(social['social'] == "Linkedin"):
                        try:
                            mlinkedin = social['url']
                        except:
                            pass
                        
                        #if(social['social'] == "Twitter"):
                        #   mtwitter = social['url']
                        #  break

                    #t["name"]=mname
                    #t["role"]=mrole
                    #t["linkedin"]=mlinkedin
                    #t["twitter"]=mtwitter

                memlinkedin[m] = mlinkedin

                    
                    #team.append(t)
        except:
            pass
    except Exception as e:
        print(e)
        print("link failed")
        browser.close()
        return []
    
    browser.close()

    return [cname,clink,cmail,fname,frole,cstage,cindustry,csector,cservice,ccity,cstate,cyears,memname[0],memrole[0],memlinkedin[0],memname[1],memrole[1],memlinkedin[1],memname[2],memrole[2],memlinkedin[2],memname[3],memrole[3],memlinkedin[3],memname[4],memrole[4],memlinkedin[4]] #, [{"company name" : cname, "website" : clink,"team":team}]



cardlinks = []

with open("textile2.csv",'r') as f:
    reader = csv.reader(f)
    for line in reader:
        cardlinks.append(line[0])


print(len(cardlinks))

with open(f"data_tx2.csv","a") as nf:
    fieldnames=["Company name","Website","Mail","Person","Role","Stage","Industry","Sector","Service","City","State","Years active",
                "M1 name","M1 role","M1 linkedin","M2 name","M2 role","M2 linkedin","M3 name","M3 role","M3 linkedin","M4 name","M4 role","M4 linkedin","M5 name","M5 role","M5 linkedin"]
    nwriter = csv.writer(nf)
    nwriter.writerow(fieldnames)
    
for j,alink in enumerate(cardlinks):
    print(f"link {j+1} : {alink}")
    li = goToPage(alink)
    if(len(li)==0):
        print("here")
        try:
            with open(f"failed_tx2.csv","a") as tf:
                twriter = csv.writer(tf)
                twriter.writerow([alink])
            print("saved")
        except:
            print("not saved")
        continue
    with open(f"data_tx2.csv","a") as nf:
        nwriter = csv.writer(nf)
        nwriter.writerow(li)

