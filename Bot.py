# -*- coding:utf8 -*-
import os, time
from selenium import webdriver
import re
from bs4 import BeautifulSoup
import yaml

cwd = os.getcwd() + '/'
driver = webdriver.Chrome(cwd + 'chromedriver')
driver.get('https://dinbendon.net/do/login'); 
time.sleep(1)

username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")
result = driver.find_element_by_name("result")
submit = driver.find_element_by_name("submit")
fuckingShit = driver.find_elements_by_class_name("alignRight")
code = fuckingShit[2].text
a = re.findall(re.compile(r"\d+"), code)
ans = int(a[0]) + int(a[1])

with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile)
cfgUsername = cfg['account']['username']
cfgPassword = cfg['account']['password']
cfgShop = cfg['order']['shop']
cfgDish = cfg['order']['dish']

username.send_keys(cfgUsername)
password.send_keys(cfgPassword)
result.send_keys(ans)
submit.click()

code = BeautifulSoup(driver.page_source.encode('utf-8','replace'))
try:
        tmp = code.find_all(string=re.compile(cfgShop))
except IndexError, e:
        # if popeye doesnt exist
        # then you can only eat shit by yourself
        print "go eat shit!"
        exit(1)

# only buy the RD5's order
for i in tmp:
    if "rd5" in i.parent.previous_sibling.previous_sibling.text.lower():
                url = "https://dinbendon.net" + i.parent.parent.next_sibling.next_element()[0].get('href')

driver.get(url)
code = BeautifulSoup(driver.page_source.encode('utf-8','replace'))

try:
        noodleId = code.find_all(string=re.compile(cfgDish))[0].parent.parent.parent.find(class_='qty').get('id')
except IndexError, e:
        print "we dont have fucking ", cfgDish, " ok?"
        exit(1)

number = driver.find_element_by_id(noodleId)
number.send_keys("1")
person = driver.find_element_by_name("fallbackBox:buyerBuilder.playedName")
person.send_keys("ACC-Squarer")
form = driver.find_element_by_id("addOrderItemForm")
form.submit()
driver.close()
