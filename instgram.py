from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os,time,pandas,xlrd
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import pymysql.cursors
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")

# # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
# # current directory
# chrome_driver = os.getcwd() +"\\chromedriver.exe"


# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
# driver.get("https://www.instagram.com/accounts/login/?next=%2Feliemoussafir%2F&source=desktop_nav")

# user = driver.find_element_by_name("username")
# user.send_keys('football___stars___')

def instagram():
	driver = webdriver.Chrome('chromedriver.exe')
	driver.get('https://www.instagram.com/accounts/login/')
	time.sleep(2)
	driver.find_element_by_name('username').send_keys("football___stars___")
	time.sleep(5)
	driver.find_element_by_name('password').send_keys("olivier130293")
	driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
	time.sleep(4)
	driver.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
	time.sleep(4)
	driver.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
	user_dict = {}
	excel_data_df = pandas.read_excel('Agent-Player List.xlsx')
	excel_data_df['Group A (player)'].dropna(inplace=True)
	excel_data_df['Group B (agent)'].dropna(inplace=True)
	list_user = excel_data_df['Group A (player)'].tolist()
	for user in list_user:
		all_folower = []
		driver.get('https://www.instagram.com/'+str(user)+'/')
		time.sleep(2)
		try:
			driver.find_element_by_xpath("/html[1]/body[1]/div[1]/section[1]/main[1]/div[1]/header[1]/section[1]/ul[1]/li[3]/a[1]").click()
			data = driver.find_element_by_xpath("//li[3]//a[1]//span[1]").text
			daa = data.replace(',','')
			foll = int(daa)
			time.sleep(2)
			followers_panel = driver.find_element_by_xpath('//body/div/div/div/div[2]')
			z=0
			while True:
				driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",followers_panel)
				z = z + 1
				time.sleep(0.5)
				if z > foll / 10:
					break
			soup = bs(driver.page_source)
			all_div = soup.find('div', {'class':'_1XyCr'})
			username = all_div.find_all('li')
			for all_tab in username:
				a_tag = all_tab.find_all('a')
				for all_user in a_tag:
					all_folower.append(all_user.text)
			value = list(set(all_folower))
			All_user_B = list_user = excel_data_df['Group B (agent)'].tolist()
			user_list = []
			for user__list_A in value:
				for Group_user_B in All_user_B:
					if user__list_A == Group_user_B:
						user_list.append(Group_user_B)
						user_dict.update({user : user_list})
					else:
						pass
			if len(user_list) == 0:
				user_dict.update({user : ["None"]})
		except:
			user_dict.update({user : ["None"]})
			user_status =driver.find_element_by_xpath('//section//section//div//div[1]//button[1]').text
			if user_status == 'Follow':
				followButton =driver.find_element_by_xpath('//section//section//div//div[1]//button[1]')
				followButton.click()
			elif user_status == 'Requested':
				pass
		list_user = excel_data_df['Group A (player)'].tolist()
		if list_user[-1] == user:
			list_user = excel_data_df['Group B (agent)'].tolist()
			for user in list_user:
				all_folower = []
				driver.get('https://www.instagram.com/'+str(user)+'/')
				time.sleep(5)
				try:
					driver.find_element_by_xpath("/html[1]/body[1]/div[1]/section[1]/main[1]/div[1]/header[1]/section[1]/ul[1]/li[3]/a[1]").click()
					data = driver.find_element_by_xpath("//li[3]//a[1]//span[1]").text
					daa = data.replace(',','')
					foll = int(daa)
					time.sleep(2)
					followers_panel = driver.find_element_by_xpath('//body/div/div/div/div[2]')
					z=0
					while True:
						driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",followers_panel)
						z = z + 1
						time.sleep(0.5)
						if z > foll / 10:
							break
					soup = bs(driver.page_source)
					all_div = soup.find('div', {'class':'_1XyCr'})
					username = all_div.find_all('li')
					for all_tab in username:
						a_tag = all_tab.find_all('a')
						for all_user in a_tag:
							all_folower.append(all_user.text)
					value = list(set(all_folower))
					All_user_A = list_user = excel_data_df['Group A (player)'].tolist()
					user_list = []
					for user__list_B in value:
						for All_user_A in All_user_A:
							if user__list_B == All_user_A:
								user_list.append(All_user_A)
								print("Match User BBBbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",All_user_A)
								user_dict.update({user : user_list})
							else:
								pass
					print("*********************************************************",user_list)
					if len(user_list) == 0:
						user_dict.update({user : ["None"]})
				except:
					user_dict.update({user : ["None"]})
					user_status =driver.find_element_by_xpath('//section//section//div//div[1]//button[1]').text
					if user_status == 'Follow':
						followButton =driver.find_element_by_xpath('//section//section//div//div[1]//button[1]')
						followButton.click()
					elif user_status == 'Requested':
						pass
	driver.close()
	print(user_dict)
	print(excel_data_df)
	return user_dict,excel_data_df
	
def save_to_db(user_dict,excel_data_df):
#     print(user_dict)
#     print(excel_data_df)
    mydb = pymysql.connect(host='localhost',user='root',password='C@lesthenics1698',
                  db='instagram_groups')
    print(mydb)
    lista = excel_data_df['Group A (player)'].tolist()
    listb = excel_data_df['Group B (agent)'].tolist()
    
    c = mydb.cursor()
    
    for key,val in user_dict.items():
        if key in lista:#for group A

            sql="select username from groupa_users where username=%s;"
            value=key
            is_exist = c.execute(sql,value)
#             print(is_exist)
            try:
                if is_exist==1:
                    #update
                    sql="update groupa_users set groupb_followers=%s where username=%s;"
                    value=(val,key)
                    c.execute(sql,value)

                if is_exist==0:
                    #insert
                    sql="insert into groupa_users(username,groupb_followers) values (%s,%s);"
                    value=(key,val)
                    c.execute(sql,value)
                
            except:
                print('something went wrong for group A')
#             

        else:#for group B
            sql="select username from groupb_users where username=%s;"
            value=key
            is_exist = c.execute(sql,value)
            try:
                if is_exist==1:
                    #update
                    sql="update groupb_users set groupa_followers=%s where username=%s;"
                    value=(val,key)
                    c.execute(sql,value)

                if is_exist==0:
                    #insert
                    sql="insert into groupb_users(username,groupa_followers) values (%s,%s);"
                    value=(key,val)
                    c.execute(sql,value)
            except:
                print('something went wrong for group A')        
        
        
        
        
#     c = mydb.cursor()
#     a = c.execute("select username from groupa_users where username='as'")
#     print(a)
#     res = c.fetchall()
    mydb.commit()
    c.close()
    mydb.close()
    print('DB task Done')
#     c.execute('select * from groupb_users')
#     res = c.fetchall()
#     print(res)	
if __name__ == '__main__':
	user_dict,excel_data_df = instagram()	
	# print(excel_data_df)
	save_to_db(user_dict,excel_data_df)