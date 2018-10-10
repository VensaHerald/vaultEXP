from __future__ import print_function
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from googleapiclient.discovery import build
import globals
import csv
import time

class App:
	def __init__(self):
		pass
		
#function returns service object from googleapiclient for use by application.  does not create or validate any information passed to it		
def delegate_service(path_file,scopes,user):
	creds = service_account.Credentials.from_service_account_file(path_file,scopes=scopes)
	delegated_creds = creds.with_subject(user)
	service = build('vault', 'v1', credentials=delegated_creds)
	return service

#response dict containing only the exports key and all data
#mult_exports list containing list of dicts for each export
#export dict containing status, cloudstoragesink,stats,name,matterId,createTime,exportOptions,requested,query,id

#class for handling exports.  accepts service object and matter ID on initialisation.   
class Matter_Exports:
	def __init__(self,service,matter_id):
		self.matter_id = matter_id
		self.service = service
		self.exports = service.matters().exports().list(matterId=matter_id).execute().get('exports',[])
	
	def list_exports_id(self):
		export_list = []
		for export in self.exports:
			export_list.append(export.get('id',''))
		return export_list
		
	def status_export_by_id(self,exp_id):
		status = ''
		for export in self.exports:
			if export.get('id','') == exp_id:
				status = export.get('status','')
		return status
	
	def print_exports_status(self):
		for export in self.list_exports_id():
			print("Export {}: Status is {}\n".format(export,self.status_export_by_id(export)))
	
	def create_export(self,eml):
		email_account = [eml]
		#query_options = {}
		query_terms = ''
		query_body = {'corpus':'MAIL','dataScope':'ALL_DATA','searchMethod':'ACCOUNT','accountInfo':{'emails':email_account},
			#'terms':query_terms,
			#'mailOptions':query_options,
		}
		export_options = {'exportFormat':'MBOX'}
		export_create = {
			'name':'{} gmail export'.format(eml),
			'query':query_body,
			'exportOptions': {
				'mailOptions':export_options
			}
		}
		# print(export_create)
		return self.service.matters().exports().create(matterId=self.matter_id,body =export_create).execute()
		
		
#get csv file, parse into list, slice to avoid previously created exports/headers
email_list= [a for a in csv.reader(open("eml_list.csv","r"))][1:]
#set up service and matter to create exports in
va_service = delegate_service(SERVICE_FILE,SCOPES,STD_USER)
va_matter = Matter_Exports(va_service, STD_MATTER)

#loop through email list and create an export per email.  Catch any failed exports in try/except
for email in email_list:
	try:
		created = va_matter.create_export(email[0])
		print("export created for {}".format(email[0]))
	except:
		print("export failed for {}".format(email[0]))
	time.sleep(55) # sleep to avoid goign over quota

#creds = service_account.Credentials.from_service_account_file(SERVICE_FILE,scopes=SCOPES)

#authed_session = AuthorizedSession(creds)
#url = "https://ediscovery.google.com/discovery/matters/7e871834-80f2-42aa-904b-ee7cee2f099b/exports/exportly-2148a7ec-4ce0-41cf-ac12-9dd29b39b9ca/files/-1?hl=en_GB"
#response = authed_session.request('GET',url)
#print(type(response))
#print(response.text)


	
def download_export(exp_id):
	pass
	#make http request in form of
	#https://ediscovery.google.com/discovery/matters/{MATTER_ID}/exports/{EXPORT_ID}/files/{I}?hl=en_GB
	#where syntactical {} are relevant info and {I} is integer in the range (-1:5) 
	#will need to catch exceptions as files for {I} > 2 may not exist
	#these exceptions will return a 400 error
	#not sure what kind of requests these will fall under with regards to API  
	#will need to build in synchronous calling to prevent overloading of API requests
	#response of http request to be stored in relevant format in folder in mounted share

	
	

	
# va_matter.print_exports_status()