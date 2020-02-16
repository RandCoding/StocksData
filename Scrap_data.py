#!/usr/bin/env python
# coding: utf-8

# In[39]:


#Scrapping Data of Top Gainers from Finviz
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui


# In[2]:


def get_top_gainers_dataframe():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Options for not openning a window.

    driver = webdriver.Chrome("chromedriver",options=options)
#     url = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers"
    url="https://finviz.com/screener.ashx?v=111&s=ta_topgainers&f=fa_epsqoq_pos,fa_salesqoq_pos,geo_usa,sh_price_u10&ft=4"
#     url = "https://finviz.com/screener.ashx?v=341&s=ta_topgainers&f=fa_epsqoq_pos,fa_salesqoq_pos,geo_usa,sh_avgvol_o100,sh_curvol_u750,sh_price_u5&ft=4"
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content,features="lxml")

    table = soup.find('table', attrs={'width':'100%','cellpadding':'3','cellspacing':'1', 'border':'0', 'bgcolor':'#d3d3d3'})

    table_body = table.find('tbody')

    rows = table_body.find_all('tr')

    data=[]
    columns=[]
    first = True
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        if first:
            columns = cols
            first = False

        else:

            data.append([ele for ele in cols if ele]) 


    return pd.DataFrame(data, columns = columns) 


# In[64]:


def get_max_available_date(ticker):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Options for not openning a window.

    driver = webdriver.Chrome("chromedriver",options=options)
    
    url = f'https://finance.yahoo.com/quote/{ticker}/history'
    
    driver.get(url)

    content = driver.page_source
    soup = BeautifulSoup(content,features="lxml")
    
    ok_button = driver.find_element_by_xpath('//button[@type="submit" and @name="agree" and @value="agree"]')
    ok_button.click()
    
    wait = ui.WebDriverWait(driver,20)
    wait.until(lambda driver: driver.find_element_by_xpath('//input[@type="text" and @data-test="date-picker-full-range"]'))
    down_button = driver.find_element_by_xpath('//input[@type="text" and @data-test="date-picker-full-range"]')
    down_button.click()
    
    wait.until(lambda driver: driver.find_element_by_css_selector('#Col1-1-HistoricalDataTable-Proxy > section > div.Mt\(15px\).drop-down-selector.historical > div.Bgc\(\$lv1BgColor\).Bdrs\(3px\).P\(10px\) > div:nth-child(1) > span.Pos\(r\) > div > div.Ta\(c\).C\(\$tertiaryColor\) > span:nth-child(8)'))
    max_button = driver.find_element_by_css_selector('#Col1-1-HistoricalDataTable-Proxy > section > div.Mt\(15px\).drop-down-selector.historical > div.Bgc\(\$lv1BgColor\).Bdrs\(3px\).P\(10px\) > div:nth-child(1) > span.Pos\(r\) > div > div.Ta\(c\).C\(\$tertiaryColor\) > span:nth-child(8)')
    max_button.click()
    
    startDate = driver.find_element_by_name("startDate")
    endDate = driver.find_element_by_name("endDate")
    
    return startDate.get_attribute('value'),endDate.get_attribute('value')
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




