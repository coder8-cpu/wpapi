from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .main_ import create_edge_driver
from rest_framework.views import APIView
import random as r
import os
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium.webdriver.remote.webdriver import WebDriver
import pickle
#signup
#login
#account instance (token,unique_id,executor_path)
#return apis(msg,media,doc)
#connect to existing session
#handle errors




class EstablishConnection(APIView):

    def __init__(self) -> None:
        self.session_list = []
        self.context = {}
        self.uni = ""
    def Create_Instance(self):
        int_a = r.randint(0,9)
        int_b = r.randint(10,15)
        int_c = r.randint(0,9)
        int_d = r.randint(25,35)
        unique_id = str(int_a) + str(int_b) +str(int_c) +str(int_d)
        self.uni = unique_id
        os.makedirs(unique_id,exist_ok=False)
        driver = create_edge_driver(f"C:/Users/pc/Desktop/env/{unique_id}")
        self.session_list.append(driver)

        driver.get('https://web.whatsapp.com')
  
  
        driver.implicitly_wait(20) 
        try:
            qr_code = driver.find_element(By.TAG_NAME, 'canvas').screenshot_as_base64
        except Exception:
            driver.quit()
            return redirect("/qr-code")
        return qr_code, driver
    def save_driver_session_to_json(self,driver, filename):
        session_info = {
            'session_id': driver.session_id,
            'executor_url': driver.command_executor._url,
            'profile_dir': f"C:/Users/pc/Desktop/env/{self.uni}"
        }

        with open(filename, 'w') as file:
            json.dump(session_info, file)
   
    def render_qr(self,request):
        qr_code, driver = self.Create_Instance()
        self.save_driver_session_to_json(driver=driver,filename='token.pickle')
        request.session['session_id'] = driver.session_id
        self.context[driver.session_id] = driver
    
        request.session.save()
        
        
        


        return render(request, 'qr_code.html', {'qr_code': qr_code,'session': driver.session_id})
        # try:
        #     WebDriverWait(driver, 300).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='chat-list']"))
        #     )
        #     return HttpResponse("done scan!")
        # except Exception:
        #     driver.quit()
        #     return redirect("/qr-code")
    
    

    

    def connect_to_existing_session(self,session_id, executor_url,profile):
       
       
   
        driver = create_edge_driver(profile)
       
    
        
        

        return driver

    def load_driver_session_from_json(self,filename):
        with open(filename, 'r') as file:
            session_info = json.load(file)
        session_id = session_info['session_id']
        executor_url = session_info['executor_url']
        profile = session_info['profile_dir']
        print(executor_url)
        return self.connect_to_existing_session(session_id, executor_url,profile)





    
       
    
    def start_new_chat(self,driver, phone_number,message):
   
        new_chat_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='new-chat-outline']"))
        )
        new_chat_button.click()
        print("done")

    
        search_box = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='3']"))
        )
        search_box.click()
        search_box.send_keys(phone_number)
        search_box.send_keys("\n") 
        message_box = WebDriverWait(driver,15 ).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
        )
        message_box.send_keys(message)
        message_box.send_keys("\n")
        message_box.send_keys("\n")
        message_box.send_keys("\n")
        
        


    def send_message(self,request,phonenumber,message):
        import time
        session_id =  request.session.get('session_id')
        driver = self.context.get(session_id)
       
        if not driver:

            driver = self.load_driver_session_from_json("token.pickle")
            driver.get('https:/web.whatsapp.com/')
      
            self.start_new_chat(driver,phonenumber,message)
            return JsonResponse({'status': 'Message sent'})
           
        
            

        self.start_new_chat(driver,phonenumber,message)
        return JsonResponse({'status': 'Message sent'})
     
        


