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

def instagram(user_name,passwd,excel_data_df,private_acc_list):
    ############################## LOGIN ########################################
    print(private_acc_list)
    driver = webdriver.Chrome('chromedriver.exe')

    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(2)
    driver.find_element_by_name('username').send_keys(user_name)
    time.sleep(2)
    driver.find_element_by_name('password').send_keys(passwd)
    driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
    print("//////////////////////////////////")
    time.sleep(4)
    driver.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
    time.sleep(4)
    driver.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
    user_dict = {}
    # excel_data_df = pandas.read_excel('Agent_Player_List.xlsx')
    excel_data_df['Group A (player)'].dropna(inplace=True)
    excel_data_df['Group B (agent)'].dropna(inplace=True)
    list_user_a = excel_data_df['Group A (player)'].tolist()

    for user in list_user_a:
        if user in private_acc_list:    
            print(user)
            all_following_a = []
            driver.get('https://www.instagram.com/'+str(user)+'/')
            time.sleep(2)
            try:
                driver.find_element_by_xpath("/html[1]/body[1]/div[1]/section[1]/main[1]/div[1]/header[1]/section[1]/ul[1]/li[3]/a[1]").click()
                following_num = driver.find_element_by_xpath("//li[3]//a[1]//span[1]").text
                following_num = following_num.replace(',','')
                following_num = int(following_num)
                time.sleep(2)
                followings_panel = driver.find_element_by_xpath('//body/div/div/div/div[2]')
                z=0
                while True:
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",followings_panel)
                    z = z + 1
                    time.sleep(0.5)
                    if z > following_num / 10:
                        break
                soup = bs(driver.page_source)
                all_divs = soup.find('div', {'class':'_1XyCr'})
                usernames = all_divs.find_all('li')
                for each_username in usernames:
                    a_tag = each_username.find_all('a')
                    for all_user in a_tag:
                        all_following_a.append(all_user.text)
                all_following_a = list(set(all_following_a))
                
                All_user_B = list_user = excel_data_df['Group B (agent)'].tolist()
                user_list = []
                for each_user in all_following_a:
                    if each_user in All_user_B:
                    
                        print("*****************************************************",each_user)

                        user_list.append(each_user)
                        # user_dict.update({user : user_list})
                    else:
                        pass
                if len(user_list) == 0:
                    user_dict.update({user : ["None"]})
                else:           
                    user_dict.update({user : user_list})        
                private_acc_list.remove(user)
            except:
                user_dict.update({user : ["None"]})#if the user is private
                user_status =driver.find_element_by_xpath('//section//section//div//div[1]//button[1]').text
                if user_status == 'Follow':#Follow the user
                    followButton =driver.find_element_by_xpath('//section//section//div//div[1]//button[1]')
                    followButton.click()
                elif user_status == 'Requested':#pass if we have already sent the follow request
                    pass
        #################################################################       
    # list_user = excel_data_df['Group A (player)'].tolist()
    # if list_user[-1] == user:
    All_user_B = excel_data_df['Group B (agent)'].tolist()

    for user in All_user_B:
        if user in private_acc_list:
            all_following_b = []
            driver.get('https://www.instagram.com/'+str(user)+'/')
            time.sleep(5)
            try:
                driver.find_element_by_xpath("/html[1]/body[1]/div[1]/section[1]/main[1]/div[1]/header[1]/section[1]/ul[1]/li[3]/a[1]").click()
                follower_num = driver.find_element_by_xpath("//li[3]//a[1]//span[1]").text
                follower_num = follower_num.replace(',','')
                follower_num = int(follower_num)
                time.sleep(2)
                following_panel = driver.find_element_by_xpath('//body/div/div/div/div[2]')
                z=0
                while True:
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",following_panel)
                    z = z + 1
                    time.sleep(0.5)
                    if z > follower_num / 10:
                        break
                soup = bs(driver.page_source)
                all_divs = soup.find('div', {'class':'_1XyCr'})
                usernames = all_divs.find_all('li')
                for each_username in usernames:
                    a_tag = each_username.find_all('a')
                    for all_user in a_tag:
                        all_following_b.append(all_user.text)
                all_following_b = list(set(all_following_b))
                All_user_A = list_user = excel_data_df['Group A (player)'].tolist()
                user_list = []
                for each_user in all_following_b:
                    
                    if each_user in All_user_A:
                        print("*****************************************************",each_user)
                        user_list.append(each_user)
                        # print("Match User BBBbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",All_user_A)
                        # user_dict.update({user : user_list})
                    else:
                        pass
                
                if len(user_list) == 0:
                    user_dict.update({user : ["None"]})
                else:   
                    user_dict.update({user : user_list})    
                private_acc_list.remove(user)    
            except:
                user_dict.update({user : ["None"]})
                private_acc_list.append(user)
                user_status =driver.find_element_by_xpath('//section//section//div//div[1]//button[1]').text

                if user_status == 'Follow':
                    followButton =driver.find_element_by_xpath('//section//section//div//div[1]//button[1]')
                    followButton.click()
                elif user_status == 'Requested':
                    pass
    driver.close()
    print(user_dict)
    print(excel_data_df)
    return user_dict,excel_data_df,private_acc_list
    
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
            print(val)
            val=str(val)
            sql="select username from groupa_users where username=%s;"
            value=key
            is_exist = c.execute(sql,value)
            # print(val)
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
        #for group B
        else:
            val=str(val)
            print(val)
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

def check_user_dict(first_user_dict,second_user_dict):
    correct_dict={}
    for (k1,v1),(k2,v2) in zip(first_user_dict.items(),second_user_dict.items()):
        if 'None' in v1 and 'None' not in v2:
            v1 = v2




if __name__ == '__main__':
    constants_df = pandas.read_excel('constants.xlsx')
    excel_data_df = pandas.read_excel('Agent_Player_List.xlsx')
    users_a = excel_data_df['Group A (player)'].tolist()
    users_b = excel_data_df['Group B (agent)'].tolist()
    private_acc_list=users_a + users_b
    # print(private_acc_list)

    #1st ID
    user_name = constants_df['Credentials_un'][0]
    passwd = constants_df['passwd'][0]
    s = time.time()
    user_dict,excel_data_df,private_acc_list = instagram(user_name,passwd,excel_data_df,private_acc_list)
    f = time.time()
    print(f-s)
    save_to_db(user_dict,excel_data_df)
    print('First ID executed')

    #2nd ID
    user_name_two = constants_df['Credentials_un'][1]
    passwd_two = constants_df['passwd'][1]
    s = time.time()
    user_dict,excel_data_df,private_acc_list = instagram(user_name,passwd,excel_data_df,private_acc_list)
    f = time.time()
    print(f-s)
    save_to_db(user_dict,excel_data_df)
    print('Second ID executed')

    #3rd ID
    user_name_three = constants_df['Credentials_un'][2]
    passwd_three = constants_df['passwd'][2]
    s = time.time()
    user_dict,excel_data_df,private_acc_list = instagram(user_name,passwd,excel_data_df,private_acc_list)
    f = time.time()
    print(f-s)
    save_to_db(user_dict,excel_data_df)
    print('Third ID executed')
      
    # user_dict = {'moussa.cisse3': ['mt93290', 'mhn.93t'], 'wilson_smk': ['None'], 'momoo.el': ['None'], 'Matthis.abline': ['None'], 'philnabe': ['None'], 'availlant24': ['None'], 'guerra.frederic': ['None'], 'robindes_s': ['None'], 'mhn.93t': ['None'], 'mt93290': ['None']}
    # save_to_db(user_dict,excel_data_df)
