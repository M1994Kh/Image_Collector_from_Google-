def txt_f(st,fi):
    flag = 0
    for line in fi:   
        if st in line:  
            flag = 1
            break 
    return(flag)
def url_chk(st,banned_links):
    flag=0
    st1=st.split('/')[0]
    if 'http' in st1 and st not in banned_links:
        flag=1
    return(flag)
# from win32con import SW_HIDE
# import win32gui
# pid =win32gui.GetForegroundWindow()
# win32gui.ShowWindow(pid , SW_HIDE)
import os
import time
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
# option=webdriver.ChromeOptions()
# option.headless=True
# option.add_argument(f'user_agent={user_agent}')
# option.add_argument('--window-size=1920,1080')
# option.add_argument('--ignore-certificate-errors')
# option.add_argument('--allow-running-insecure-content')
# option.add_argument('--disable-extentions')
# option.add_argument('--start-maximized')
# option.add_argument('--disable-gpu')
# option.add_argument('--disable-dev-shm-usage')
# option.add_argument('--no-sandbox')
keyword=input()
k1=keyword.split(' ')
keyword=''
kw=''
for item in k1:
    kw=kw+item[0].lower()
    item=item[0].upper()+item[1:]
    keyword=keyword+item+' '
keyword=keyword.strip(' ')
address = os.path.join(os.path.dirname(os.path.abspath(__file__)) , 'chromedriver (3).exe')
driver = webdriver.Chrome(executable_path = address)#, options=option ) 
adre= os.path.join(os.path.dirname(os.path.abspath(__file__)) ,'Photos', keyword)
adr=os.path.join(adre,'links.txt')
if not os.path.exists(adre):
    os.makedirs(adre)
if not os.path.exists(adr):
    f1=open(adr , "w")
    f1.close()
driver.get('https://www.google.com/imghp?hl=en&authuser=0&ogbl')
time.sleep(10.5)
# driver.find_element_by_xpath('//*[@id="gb"]/div/div[1]/div/div[2]/a').click()
driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(keyword+Keys.ENTER)
time.sleep(0.5)
var1=0
var2=4
sizes=['Large','Medium','Icon','Larger than 400×300','Larger than 640×480','Larger than 800×600','Larger than 1024×768','Larger than 2 MP','Larger than 4 MP','Larger than 6 MP','Larger than 8 MP','Larger than 10 MP','Larger than 12 MP','Larger than 15 MP','Larger than 20 MP','Larger than 40 MP','Larger than 70 MP']
types=['Face','Photo','Clip art','Line drawing','Animated']
tx1="//*[contains(text(), '"+sizes[var1]+"')]"
tx2="//*[contains(text(), '"+types[var2]+"')]"
driver.find_element_by_xpath('//*[@id="kO001e"]/div[2]/div/div[2]/div[1]/div/div').click()
driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[2]/c-wiz/div[1]/div/div[1]/div[2]/div[1]/div/div[3]/a[2]').click()
# driver.find_element_by_xpath('//*[@id="imgsz_button"]').click()
# driver.find_element_by_xpath(tx1).click()
driver.find_element_by_xpath('//*[@id="imgtype_button"]').click()
driver.find_element_by_xpath(tx2).click()
driver.find_element_by_xpath('//*[@id="s1zaZb"]/div[5]/div[10]/div[2]/input[2]').click()
time.sleep(1.5)
driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img').click()
wo=0
bndl=list()
files =os.listdir(adre)
mi = len(files)-1
formats=['.jpg','.jpeg','.webp','.png','.gif']
quan=100
min_size=100000
htr='a'
htn='b'
rep=0
while mi<quan and rep<5:
    t=0
    htr=htn
    htn=driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[3]/div[1]/a[1]/h1').text
    if htr==htn:
        print('------------------------------------------------------------------------------------------------------')
        rep+=1
    if wo<mi:
        lim=2
    elif wo>=mi:
        lim=20
    count=0
    fi=open(adr , "r")
    while count<lim and t==0:
        count+=1
        dela1=0.01*(1.35**count)
        time.sleep(dela1)
        htm=driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute("src")
        x1=txt_f(htm[10:],fi)
        if len(htm)>200:
            print(wo,' ',mi,' ',x1,'    ',htm[:200])
        else:
            print(wo,' ',mi,' ',x1,'     ',htm)
        if x1==1:
            t=2
        for item in formats:
            if item in htm and x1==0 and url_chk(htm,bndl)==1:
                t=1
                suf=item
                htm=htm[:htm.find(item)]+item
                # counte1=0
                # while counte1<5:
                try:
                    imag = requests.get(htm)
                except:
                    # counte1+=1
                    t=2           
                if t==2:
                    bndl.append(htm)
    fi.close()
    if t==1 :
        mi+=1
        rt=1
        nam=kw+'-'+str(mi)+suf
        name=os.path.join(adre , nam)
        # try:
        with open(name, 'wb') as file:
            file.write(imag.content)
        # except:
        #     mi-=1
        size = os.path.getsize(name)
        fi=open(adr , "r")
        if size<min_size:
            os.remove(name)
            mi-=1
            rt=0
        elif size>min_size:
            f2=open(adr , "a")
            try:
                with Image.open(name) as im:
                    width, height = im.size
                    li1=str(width)+'*'+str(height)+'  '+str(size)
                    lin=htm+' *** '+nam+'  '+str(width)+'*'+str(height)+'  '+str(size)+'B\n'
                    f2.write(lin)
            except:
                os.remove(name)
                mi-=1
            if txt_f(li1,fi)==1 and rt==1 and os.path.exists(name):
                os.remove(name)
                mi-=1
            f2.close()
        fi.close()
    driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[1]/a[3]').click()
    wo+=1
print(mi/wo) 
print(bndl)   
driver.quit()
