import os,re
import urllib
import sys

cloudflareEmail="EMAIL@EXAMPLE.COM"	#CF Login Email Address
cloudflareAPIkey="cloudflareapikeylowercase"	#API Key as shown on https://www.cloudflare.com/my-account
baseDomain='yourdomain.com'	#Domain Name as shown on https://www.cloudflare.com/my-websites.html
recordType='A'   	#See "Type" Column on https://www.cloudflare.com/dns-settings?z=example.com
recordName='yoursubdomain'	#See "Name" Column on https://www.cloudflare.com/dns-settings?z=example.com

#Find the CloudFlare ID of your (sub)domain based on the recordName and recordType
data={'a': 'rec_load_all','tkn': cloudflareAPIkey,'email': cloudflareEmail,'z': baseDomain}
data = urllib.urlencode(data)
f = urllib.urlopen("https://www.cloudflare.com/api_json.html", data)
recloadall=f.read()
recloadall=recloadall[0:recloadall.find('"display_name":"'+str(recordName)+'","type":"'+str(recordType)+'"')]
recordID=recloadall[recloadall.rfind("rec_id")+9:recloadall.rfind("rec_tag")-3]
if recordID.find(':"error"')>-1:
	recordID=recordID[recordID.find('"msg":"')+6:recordID.find(",",recordID.find('"msg":"')+3)]
print "CF Record:",recordID

#Get your current device IP Address
f = urllib.urlopen("http://ip-api.com/xml")
ipe=f.read()
ip=ipe[ipe.find("<query><![CDATA[")+16:ipe.rfind("]]>",ipe.find("<query><![CDATA["))].strip()
print "IP Address:",ip

#Update with Cloudflare
data={'a': 'rec_edit','tkn': cloudflareAPIkey,'id': recordID,'email': cloudflareEmail,'z': baseDomain,'type': recordType,'name': recordName,'content': ip,'service_mode': '0','ttl': '1'}
data = urllib.urlencode(data)
f = urllib.urlopen("https://www.cloudflare.com/api_json.html", data)
response=f.read()
print "Update:",response[response.find('result":')+9:response.find(',',response.find('result":')+3)-1]
