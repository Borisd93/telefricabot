from html2text import html2text
import requests,io,random,re

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
	def notifications(self,limit):
		r=self.session.get(self.url+'/notifications/system',headers=HEADERS)
		cont=0
		out=''
		for i in re.findall('https://friendicarg.nsupdate.info/notification/.*',r.text):
			cont=cont+1
			if cont-1==limit:
				break
			else:
				out=out+'\n'+'\n'+i.replace(re.findall('"><img src=".*" aria-hidden="true" class="notif-image">',i)[0],' ').replace('<span class="notif-when">','').replace('</span></a>','')
		return out
	def network(self,limit):
		texto=self.session.get('https://friendicarg.nsupdate.info/network').text
		exp=re.findall('<div class="wall-item-body e-content p-name">.*</div>',texto)
		exp1=re.findall('"display/.*"',texto)
		out=[]
		for i in range(0,limit):
			try:
				out.append(html2text(exp[i])+'\n'+self.url+exp1[i].replace('"','').replace('> _< span class=sr-only','')+'\n\n')
			except:
				break
		return out
