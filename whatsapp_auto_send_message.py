'''
if not working, can be the chromedriver, please download the version 
equal of your chrome and OS at https://chromedriver.chromium.org/downloads
'''
import unittest
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os, re, time, json

actual_path = os.path.abspath(os.path.dirname(__file__))

def login():
	#browser = webdriver.Firefox(executable_path = 'C:/Users/Anderson/Desktop/programas/geckodriver.exe')
	browser = webdriver.Chrome('chromedriver.exe') # start an instance
	browser.get('https://web.whatsapp.com/') 
	time.sleep(2)
	input('After login with QrCode press Enter')
	return browser

#if at time theres another Web WhatsApp open, click in Use Here 
def usehere(browser):
	try:
		btn_usehere = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div/div/div[2]/div[2]')))
		btn_usehere.click()
	except Exception as e:
		print('Already logged in or error: '+e)

def send_message(users,message,browser):	
	try:
		browser.get('https://web.whatsapp.com/') 
		time.sleep(2)
		message_sent = {}
		jsonfile = open(actual_path+'/messages_sent.json', 'a')
		usehere(browser)
		i = 0
		for user in users:
			try:
				#search
				to_user = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="side"]/div[1]/div/label/input')))
				to_user.send_keys(user)
				time.sleep(2)
				to_user.send_keys(Keys.ENTER)
				time.sleep(2)
				#type the message
				field_message = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')))
				if (type(message)==list):
					field_message.send_keys(message[i])
					#log
					message_sent.update({'username': user,'message': message[i]})
					json.dump(message_sent, jsonfile)
					jsonfile.write('\n')
				else:
					field_message.send_keys(message)
					#log
					message_sent.update({'username': user,'message': message})
					json.dump(message_sent, jsonfile)
					jsonfile.write('\n')
				send = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button/span')))
				send.click()
				time.sleep(2)
				i += 1
			except Exception as e:
				print('Error to send message to '+user+': '+str(e))
				message_sent.update({'username': user,'error': str(e)})
				json.dump(message_sent, jsonfile)
				jsonfile.write('\n')
		jsonfile.close()
	except Exception as e:
		print('Error to send: '+str(e))

def main():
	browser = login()
	#you have to put names that exists in your WhatsApp contacts
	users = ['andersonlthome','erick']
	messages = []
	for user in users:
		messages.append('Good afternoon '+user+', fine?')
	send_message(users,messages,browser)
	browser.quit()

if __name__ == '__main__':
    main()