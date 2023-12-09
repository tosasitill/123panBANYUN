import time
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import argparse

def login(username, password):
	time.sleep(2.5)
	account_login_tab = driver.find_element(By.XPATH, '//div[@data-node-key="user"]')
	account_login_tab.click()
	driver.find_element(By.ID, 'basic_passport').send_keys(username)
	driver.find_element(By.ID, 'basic_password').send_keys(password)
	driver.find_element(By.CLASS_NAME, 'loginBtn').click()
	print('登录成功！')
	time.sleep(0.5)
	wait = WebDriverWait(driver, 10)
	close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ant-modal-close')))
	print('傻逼弹窗关闭完成')
	close_button.click()

def upload_file(file_paths):
	driver.get('https://www.123pan.com/3119576')
	time.sleep(2.5)
	ele121k = driver.find_element(By.CSS_SELECTOR, '#app > div > div > section > section > section > main > div > div.homeClass > div:nth-child(1) > div.ant-dropdown-trigger.sysdiv.parmiryButton')
	ele121k.click()
	print('找到上传按钮')
	time.sleep(2.5)
	element_to_click = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/ul/li[1]')
	element_to_click.click()
	print('选择文件上传')
	time.sleep(2.5)
	a = 0
	print('开始文件上传')
	for file_path in file_paths:
	a = a + 1
	file_uploader = driver.find_element(By.CSS_SELECTOR, 'ul > li:nth-child(1) > span > div > input[type=file]')
	file_uploader.send_keys(file_path)
	time.sleep(0.5)
	print('当前已成功上传', a, '次')
	
	# 等待成功的 JSON 响应
	success_response = {"code": 0, "message": "成功"}
	while True:
		# 发送 HTTP 请求，替换为实际的请求 URL
		response = requests.get('https://example.com/api/check_status')
	
		# 检查响应内容是否包含成功的 JSON
		if response.json() == success_response:
			print('收到成功的响应，跳出循环')
			break
	
		# 暂停一段时间再次检查
		time.sleep(5)
if __name__ == "__main__":
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15')
	chrome_options.add_argument('--disable-gpu')
	parser = argparse.ArgumentParser(description='Automate web interactions for file upload and sharing.')
	parser.add_argument('username', type=str, help='Your username for login')
	parser.add_argument('password', type=str, help='Your password for login')
	parser.add_argument('file_paths', nargs='+', type=str, help='Paths to files for upload')
	args = parser.parse_args()
	driver = webdriver.Chrome(options=chrome_options)
	driver.get('https://www.123pan.com/')
	login(args.username, args.password)
	upload_file(args.file_paths)

	driver.quit()
