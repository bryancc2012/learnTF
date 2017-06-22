

# read the gamedata from website 

from selenium import webdriver
import csv
import sys


def main():
    gamelink=[]
    oldgamedata=[]
    
    gamedata=[]
    #gamedatahead=("gameid","score1","score2","asias1","asias2","asiash","asiae1","asiae2","asiaeh","eurosw","eurosd","eurosl","euroew","euroed","euroel","euroswd","eurosdd","eurosld","euroewd","euroedd","euroeld")
    #gamedata.append(gamedatahead)
    
    oldasiaurl="http://odds.500.com/fenxi/yazhi-"
    oldeurourl="http://odds.500.com/fenxi/ouzhi-"
    
    #open csv and read
    with open("alink_1.csv", "r") as f:
        f_csv=csv.reader(f)
        for row in f_csv:
            gamelink.append(row)
            
    print("==========华丽的分割线=============")
    
    with open("gamedata.csv", "r") as f:
        f_csv=csv.reader(f)
        for row in f_csv:
            oldgamedata.append(row)
    
    i=len(oldgamedata)
    
    
    #count=0
    while i < len(gamelink):
        try:
        
            #if count>=2: 
            #    break
            #else:
            #    count+=1
            print (str(int(gamelink[i][0])))
            if int(gamelink[i][0]) < 13000 : 
                print ("=====已读完13年以前的数据=====")
                break
            
            url=gamelink[i][2]
            print(url)
            driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
            driver.get(url)
            elem = driver.find_element_by_class_name("odds_hd_bf")
            score=elem.text.split(":")
            print(score,len(score))
            if len(score)>1:
                score1=score[0]       #比分1
                score2=score[1]         #比分2
            else:
                score1=""
                score2=""
                print ("no score data")
                pass
            
            driver.close()

            url=oldasiaurl+gamelink[i][1]+"-show-2"  # 全部公司数据
            driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
            driver.get(url)
            
            elem = driver.find_element_by_id("avgfs1")
            asias1=elem.text
            elem = driver.find_element_by_id("avgfs2")
            asias2=elem.text
            elem = driver.find_element_by_id("avgfh")
            asiash=elem.text
            
            elem = driver.find_element_by_id("avges1")
            asiae1=elem.text
            elem = driver.find_element_by_id("avges2")
            asiae2=elem.text
            elem = driver.find_element_by_id("avgeh")
            asiaeh=elem.text

            driver.close()
            
            url=oldeurourl+gamelink[i][1]+"-show-2"  # 全部公司数据
            driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
            driver.get(url) 
            
            elem = driver.find_element_by_id("avwinc1")
            eurosw=elem.text
            elem = driver.find_element_by_id("avdrawc1")
            eurosd=elem.text
            elem = driver.find_element_by_id("avlostc1")
            eurosl=elem.text
            elem = driver.find_element_by_id("avwinj1")
            euroew=elem.text
            elem = driver.find_element_by_id("avdrawj1")
            euroed=elem.text
            elem = driver.find_element_by_id("avlostj1")
            euroel=elem.text
            elem = driver.find_element_by_id("lswc1")
            euroswd=elem.text
            elem = driver.find_element_by_id("lsdc1")
            eurosdd=elem.text
            elem = driver.find_element_by_id("lslc1")
            eurosld=elem.text
            elem = driver.find_element_by_id("lswj1")
            euroewd=elem.text
            elem = driver.find_element_by_id("lsdj1")
            euroedd=elem.text
            elem = driver.find_element_by_id("lslj1")
            euroeld=elem.text

            driver.close()
            
            gameid=gamelink[i][1]
            gamedatatem=[gameid,score1,score2,asias1,asias2,asiash,asiae1,asiae2,asiaeh,eurosw,eurosd,eurosl,euroew,euroed,euroel,euroswd,eurosdd,eurosld,euroewd,euroedd,euroeld]
            gamedata.append(gamedatatem)
            i+=1
        except:
            print (sys.exc_info())
            break
        
    with open("gamedata.csv", "a") as f:
        f_csv = csv.writer(f)
        f_csv.writerows(gamedata)
    
    print("i=", i, ", done!")
    return

j=0
while j<10:
    print("J=",j)
    main()
    j+=1
