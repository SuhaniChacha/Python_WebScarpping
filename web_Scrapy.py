import selenium
import time 
import sqlite3
import numpy as np
import pandas as pd
from goto import with_goto
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
df = pd.read_csv("C:\\Users\\Suhani\\Desktop\\pincode_csv.csv",encoding = "ISO-8859-1")
d = df[df['circlename']=="Gujarat"]
m = d[d['districtname']=="Ahmedabad"]
pin_code_list = m['pincode']
pin_code_list = pin_code_list.values.T.tolist()

pin_code_list = list(dict.fromkeys(pin_code_list))



driver = webdriver.Chrome()
driver.get("http://www.irdaonline.org/PublicAccess/AgentLocator.aspx")
driver.implicitly_wait(10000)
def get_array(i):
	select = Select(driver.find_element_by_id('ddlInsuranceType'))
	select.select_by_value(i) #1 to 3 Life
	time.sleep(1) 

	select_box = driver.find_element_by_name("ddlInsurer") 
	options = [x for x in select_box.find_elements_by_tag_name("option")]
	x = []
	for element in options:
		x.append(element.get_attribute("value"))
	
	return x
	
general_insurer = get_array('1')
print(general_insurer)
life_insurer = get_array('2')
print(life_insurer)
health_insurer = get_array('3')
print(health_insurer)


for e in general_insurer:	
	for i in range(0,len(pin_code_list)):
		print(pin_code_list[i])
		print(e)
		select = Select(driver.find_element_by_id('ddlInsuranceType'))
		select.select_by_value('1')
		time.sleep(1) 
		select1 = Select(driver.find_element_by_id('ddlInsurer'))
		select1.select_by_value(e) 
		select2 = Select(driver.find_element_by_id('ddlState'))
		select2.select_by_value('6') 
		time.sleep(1) 
		select3 = Select(driver.find_element_by_id('ddlDistrict'))
		select3.select_by_value('102') 
		time.sleep(1) 
		
		inputElement = driver.find_element_by_id("txtPINCode")
		driver.find_element_by_id("txtPINCode").clear()
		inputElement.send_keys(pin_code_list[i])
		
		
		driver.find_element_by_id("btnLocate").submit()
		
		print ("pinzz : -------------- ")
		try: 
			table_elements = WebDriverWait(driver, 1).until(EC.presence_of_all_elements_located(
				(By.XPATH, "//*[@id='fgAgentLocator']//tr")))
		except:
			print("empty")
		print ("tzble : -------------- ")
		for j in table_elements:
			m=""
			m = m +j.text
			m = m.split('\n')
			print(m)
			if(len(m)==15):
				
				#conn = MySQLdb.connect('localhost', user='root', password='')
				#conn=MySQLdb.connect(host='localhost',user='root',passwd='')
				conn =sqlite3.connect('database.db')
				cursor = conn.cursor()
				#cursor.execute('Create database agent_locator')
				#cursor.execute('use agent_locator')
				table='create table IF NOT EXISTS loc(agent_name text(100), license_no text(12),idra_urn text(15), agent_id text(25),insurance_type text(25),insurere text(200),dp_id text(10), state text(25),district text(50), pin_code text(6),valid_from text(25), valid_to text(25), absorbed_agent text(25) , phone_no text(10), mobile_no text(10))'

				cursor.execute(table)
				cursor.execute('INSERT INTO loc(agent_name, license_no ,idra_urn , agent_id ,insurance_type ,insurere ,dp_id , state,district , pin_code ,valid_from , valid_to , absorbed_agent  , phone_no , mobile_no ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (m[0],m[1],m[2],m[3],m[4],m[5],m[6],m[7],m[8],m[9],m[10],m[11],m[12],m[13],m[14]))
				conn.commit()
				conn.close()
				
			elif(len(m)==14):

				#conn = MySQLdb.connect('localhost', user='root', password='')
				#conn=MySQLdb.connect(host='localhost',user='root',passwd='')
				conn =sqlite3.connect('database.db')
				cursor = conn.cursor()
				#cursor.execute('Create database agent_locator')
				#cursor.execute('use agent_locator')
				table='create table IF NOT EXISTS loc(agent_name text(100), license_no text(12),idra_urn text(15), agent_id text(25),insurance_type text(25),insurere text(200),dp_id text(10), state text(25),district text(50), pin_code text(6),valid_from text(25), valid_to text(25), absorbed_agent text(25) , phone_no text(10), mobile_no text(10))'

				cursor.execute(table)
				cursor.execute( "INSERT INTO loc(agent_name, license_no ,idra_urn , agent_id ,insurance_type ,insurere , state,district , pin_code ,valid_from , valid_to , absorbed_agent  , phone_no , mobile_no)  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (m[0],m[1],m[2],m[3],m[4],m[5],m[6],m[7],m[8],m[9],m[10],m[11],m[12],m[13]) )
				
				conn.commit()
				conn.close()
			
		driver.find_element_by_id("txtPINCode").clear()
		
	