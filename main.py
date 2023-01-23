import requests
from bs4 import BeautifulSoup
import os
import re


def web_driver(link):
	login_url = "https://judge.softuni.org/Account/Login"
	
	with requests.session() as s:
		home_page = s.get(login_url)
		
		# Judge uses two factor token authentication, so first we need to find the
		# payload Request verification token and then the one in the cookies.
		# Both of them are different and needed in order we can log in.
		rvt = BeautifulSoup(home_page.text, 'html.parser').find('input', {'name': '__RequestVerificationToken'})[
			'value']
		cookie_rvt = home_page.cookies['__RequestVerificationToken']
		
		headers = {
			"cookie":
				f"language=en; undefined=undefined;"
				f" _ga=GA1.2.1154278602.1673292951; _gid=GA1.2.929395719.1673292951;"
				f" __RequestVerificationToken={cookie_rvt}; ASP.NET_SessionId=uxwrdtfpdicjcdkzqgrdb1na;"
				f" cookies-notification=ok; _gat=1",
		}
		
		payload = {
			'__RequestVerificationToken': rvt,
			"UserName": "your_username",  # input your username here
			"Password": "password",  # input your password here
			"RememberMe:": 'false'
		}
		
		response = s.post(login_url, data=payload, headers=headers)
		info = s.get(link)
		
		# We parse the information using BeautifulSoup and find the needed text.
		soup = BeautifulSoup(info.text, 'html.parser')
		names = soup.find_all('a', 'k-link')
		
		return names, soup.find('h1').text


URL = input('Please enter a link from Judge to create files:\n')

file_names, title = web_driver(URL)

match = re.findall(r"\bLab|Exercise \d?\b", title)
title = match[0].lower().replace(' ', '_')
unwanted_symbols = ['-', "\'", '\"', '.']

# !! Need to enter the wanted directory. Just enter it once per module.
directory = fr""  # Enter it in the string.
directory = directory.replace('\\', '/')


# # Creating the specified directory for the lesson if it is not present.
cwd = directory + '/' + title
if not os.path.exists(cwd):
	os.makedirs(f"{cwd}")

# Change the current working directory and creating the files.
os.chdir(cwd)

# iterate over the found file names and create them after renaming them with our desired pattern
for match in file_names:
	name = match.text.lower()

	for symbol in unwanted_symbols:
		if symbol in name:
			name = name.replace(symbol, '')

	file_name = name.replace(' ', '_')

	file = open(f"{file_name}.py", "w")
	file.close()

