import requests,io,random

ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101'
ua += ' Firefox/60.0'
HEADERS = {'user-agent': ua}

class FriendApi():
	def __init__(self,url,user,password):
		self.session=requests.session()
		r=self.session.post(url+"login/",data={'username':user,'password':password,'auth-params':'login','submit':'Acceder','openid-url':''},headers=HEADERS)
		if 'Login failed. Please check your credentials.' in r.text:
			raise ValueError('Error con la contraseña o usuario')
		print(r.json)
		self.url=url
		self.user=user
		self.password=password
	def share(self,title,text):
		r=self.session.post(self.url.replace('login/','')+'item/',data={\
		'title':title\
		,'body':text\
		,'preview':'0'\
		,'post_id':''\
		,'post_id_random':str(random.randint(1,100000000000))}\
		,headers=HEADERS)
		if '<title>Forbidden</title>' in r.text:
			print(r.text)
			print('API')
			raise ValueError('Error con la contraseña o usuario')
		print(r.json,r.text,'gere')
	def html_network(self):
		return self.session.get("https://friendicarg.nsupdate.info/network",headers=HEADERS)
	def logout(self):
		self.session.get("https://friendicarg.nsupdate.info/logout",headers=HEADERS)


f=FriendApi("https://friendicarg.nsupdate.info/","x93","balbinotA13.")
