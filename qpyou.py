from tools import Tools
import hashlib
import json
import random
import requests
import socket

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class QPYOU(object):
	def __init__(self,did=None):
		self.s=requests.session()
		self.s.verify=False
		if 'Admin-PC' == socket.gethostname():
			self.s.proxies.update({'http': 'http://127.0.0.1:8888','https': 'https://127.0.0.1:8888',})
		self.s.headers.update({'Content-Type':'application/json','Accept-Language':'en-gb','User-Agent':'SMON_Kr/3.7.0.37000 CFNetwork/808.2.16 Darwin/16.3.0'})
		self.did=did
		self.guest_uid=None
		self.p1='{"language":"en","timezone":null,"game_language":"en","server_id":"","device_country":"RU","hive_country":"RU"}'
		self.p2='{"hive_country":"RU","device_country":"RU","guest_uid":"%s","timezone":null,"language":"en","game_language":"en","server_id":""}'
		
	def MD5(self,i):
		m = hashlib.md5()
		m.update(i)
		return m.hexdigest()
		
	def create(self):
		res = json.loads(self.s.post('https://api.qpyou.cn/guest/create',data=self.p1).content)
		self.guest_uid=res['guest_uid']
		return res
	
	def auth(self):
		return json.loads(self.s.post('https://api.qpyou.cn/guest/auth',data=self.p2%(self.guest_uid)).content)
		
	def registered(self):
		return json.loads(self.s.post('https://api.qpyou.cn/device/registered',data=self.p1).content)
		
	def me(self):
		res=self.s.post('https://api.qpyou.cn/user/me',data=self.p1)
		if 'thorization Faile' in res.content:
			return None
		return json.loads(res.content)
		
	def hiveLogin(self,user,password):
		self.s.cookies.update({'advertising_id':Tools().rndDeviceId(),'appid':'com.com2us.smon.normal.freefull.apple.kr.ios.universal','device':'iPad5,4','did':str(random.randint(200000000,300000000)) if not self.did else str(self.did),'native_version':'Hub v.2.6.4','osversion':'10.2','platform':'ios','vendor_id':Tools().rndDeviceId()})
		self.registered()
		self.s.post('https://hub.qpyou.cn/auth',data='{"language":"en","timezone":null,"game_language":"en","server_id":"","device_country":"RU","hive_country":"DE"}',allow_redirects=False)
		data={'id':user,'password':'','dkagh':self.MD5(password)}
		self.s.get('https://hub.qpyou.cn/auth/recent_account')
		rr= self.s.post('https://hub.qpyou.cn/auth/login_proc',data=data,headers={'Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1','Referer':'http://hub.qpyou.cn/auth/login'},allow_redirects=False)
		sss= rr.headers['Location'].split('&')
		sessionkey=sss[3].replace('sessionkey=','')
		_did=sss[2].replace('did=','')
		res=self.me()
		if not res:
			return None
		return res['uid'],_did,sessionkey

	def createNew(self):
		self.s.cookies.update({'advertising_id':Tools().rndDeviceId(),'appid':'com.com2us.smon.normal.freefull.apple.kr.ios.universal','device':'iPad5,4','did':str(random.randint(200000000,300000000)) if not self.did else str(self.did),'native_version':'Hub v.2.6.4','osversion':'10.2','platform':'ios','vendor_id':Tools().rndDeviceId()})
		self.registered()
		res=self.create()
		self.auth()
		return res['guest_uid'],res['did']