#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd 
import numpy as np
import requests
import re
import time # For time-related functions
import math # For more advanced math operations


from bs4 import BeautifulSoup
from fake_useragent import UserAgent # For 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


# In[20]:


# Define main_url for listing page, and base_url for later detail page
main_url = 'https://toyotatrust.astra.co.id/stock'


# In[21]:


# Set useragent as random fake user-agent
ua = UserAgent()
userAgent = ua.random

# Set the options for chromedriver
options = Options()

# options.add_argument('--headless') # If headless is enabled, the browser won't show up
options.add_argument('--disable-gpu') # Also used for headless
options.add_argument('--disable-extensions') # Disable any extensions
options.add_argument("--disable-notifications") # Disable notifications
options.add_argument("--disable-popup-blocking") # Disable pop-up
options.add_argument('--blink-settings=imagesEnabled=false') # Disable loading image for faster and more efficient page load
options.add_argument(f'--user-agent={userAgent}') # For choosing user-agent profile
options.add_argument('--incognito') # Enable incognito mode

# Set chromedriver as selenium webdriver and set timeout limit as 10 seconds
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(10)
driver.get(main_url)
print("Open PLP page 1")
time.sleep(10)


# In[22]:


req = requests.get(main_url, headers={'User-Agent': ua.random}, timeout=10)


# In[23]:


#Create function to collect PDP URL
def collector_URL():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Loop by using the result of .find_all() function and find the "href" attribute from each elements
    for link in soup.find_all("div", {"class": "MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation1 MuiCard-root css-o64p2b"}):
        car_link.append("https://toyotatrust.astra.co.id" + link.find("a").get("href"))
    # Let's check the result
    print(f"Total link: {len(car_link)}")
    return car_link


# In[24]:


# Create an empty list for collect PDP URL

car_link = []

#Panggil function collector_URL() untuk mengumpulkan link URL PDP dari halaman PLP yg dibuka dan masukkan ke list car_link

#Collect PLP page 1
collector_URL()
print("Collect link URL PDP from PLP page 1 ")


# In[25]:


time.sleep(10)


# In[26]:


jumlah_page=8
for i in range(2,jumlah_page+1):
    driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/nav/ul/li[10]/button').click() #pindah page
    print("Open PLP page ",+i)
    time.sleep(10)
    collector_URL() #collect URL
    print("Collect link URL PDP from PLP page ",+i)
    time.sleep(10)
    


# In[27]:


car_link


# In[28]:


len(car_link)


# In[31]:


# Create empty lists for each feature
product_link = []
product_name = []
product_model = []
product_type = []
product_price = []
product_police_n = []
product_police_n_t= []
product_mileage= []
production_year= []
product_post_location= []
product_color= []
product_fuel_type= []
product_transmission= []


# In[32]:


#create scrapping automation script to collect data from each PDP URL
for pdp in car_link:
    # Assign another req and soup variables for PDP
    print(pdp)
    pdp_req = requests.get(pdp)
    pdp_soup = BeautifulSoup(pdp_req.text, "html.parser")
    
    price = pdp_soup.find_all("h6", {"class": "MuiTypography-root MuiTypography-h6 css-1lnycu1"})
    spek = pdp_soup.find_all("div", {"class": "MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-19g4pw0"})
    location= pdp_soup.find_all("h6", {"class": "MuiTypography-root MuiTypography-subtitle2 css-3pkvrl"})
    
    # Product_link
    product_link.append(pdp)
    
    
    # Product_Name
    try:
        pn1=pdp.split("/")[-1].split("-")
        pn2=""
        for i in range(0,len(pn1)-1):
            pn2=pn2+" "+pn1[i]
        product_name.append(pn2.strip())
        
    except Exception:
         product_name.append(None)
     
    
    # Product_Model
    try:
        product_model.append(spek[0].find_all('p')[1].get_text())
        
    except Exception:
         product_model.append(None)
            
            
     # Product_Type
    try:
        product_type.append(spek[0].find_all('p')[13].get_text())
        
    except Exception:
         product_type.append(None)
            
            
    #Product_Price
    try:
        product_price.append(price[0].get_text())
        
    except Exception:
        product_price.append(None)
        
        
    #Product_Police_Number
    try:
        product_police_n.append(spek[0].find_all('p')[7].get_text())
        
    except Exception:
        product_police_n.append(None)
        
    #Product_Police_Number_Type
    try:
        plat=spek[0].find_all('p')[7].get_text()
        num = re.findall(r'\d+', plat)
        if int(num[0])%2==0:
             product_police_n_t.append("even")
        else:
             product_police_n_t.append("odd")     
        
    except Exception:
         product_police_n_t.append(None)
    
    
    # product_mileage    
    try:
        product_mileage.append(spek[0].find_all('p')[3].get_text())
        
    except Exception:
         product_mileage.append(None)
    
    # production_year   
    try:
        production_year.append(spek[0].find_all('p')[5].get_text())
        
    except Exception:
        production_year.append(None)
        
        
    # product_post_location   
    try:        
        product_post_location.append(location[1].get_text().split(" ")[-1])
        
    except Exception:
        product_post_location.append(None)
        
    
    # product_color    
    try:
        product_color.append(spek[0].find_all('p')[9].get_text())
        
    except Exception:
         product_color.append(None)
            
            
    # product_fuel_type   
    try:
        product_fuel_type.append(spek[0].find_all('p')[15].get_text())
        
    except Exception:
         product_fuel_type.append(None)
    
    
    # product_transmission    
    try:
        product_transmission.append(spek[0].find_all('p')[11].get_text())
        
    except Exception:
         product_transmission.append(None)
            


# In[33]:


# Create a DataFrame using the data collected
data = {'Product link': product_link,'Product name': product_name,'Product Model': product_model, 'Product Type': product_type,
        'Product price' : product_price,'Product police number': product_police_n,'Product police number type':product_police_n_t,
        'Product Mileage': product_mileage,'Production year' : production_year,'Product post location': product_post_location,
        'Product color' : product_color, 'Product fuel type': product_fuel_type,
         'Product Transmission': product_transmission}


# In[34]:


output = pd.DataFrame(data)
output


# In[35]:


#export dataframe to csv
output.to_csv('ADAB _(72291)_(Wahyu_Maulana_Ziwangga)_autotrust_data_v3.csv', encoding='utf-8')


# In[ ]:




