from google.oauth2 import service_account
from googleapiclient.discovery import build
import csv
import time
import sys


class Google_Service:
    def __init__(self, file, scopes, user):
        self.file = file
        self.scopes = scopes
        self.user = user
    
    def create_service(self):
        creds = service_account.Credentials.from_service_account_file(self.file,scopes=self.scopes)
        delegated_creds = creds.with_subject(self.user)
        self.service = build('vault', 'v1', credentials=delegated_creds)
        print("Service created")
        
    
    

class Vault_Service(Google_Service):
    def __init__(self, file, scopes, user, matter_id):
        super().__init__(file, scopes, user)
        self.matter_id = matter_id
        
    
    def get_exports(self):
        self.exports = self.service.matters().exports().list(matterId=self.matter_id).execute().get('exports',[])
        if self.exports:
            print("Got Exports")
    
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
    
    def create_1_export(self,eml):
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
    
    def create_exports(self,path):
        # Get file, exclude headers
        email_list= [a for a in csv.reader(open(path,"r"))][1:]
        #loop through email list and create an export per email.  Catch any failed exports in try/except
        for email in email_list:
            try:
                created = va_matter.create_1_export(email[0]+"@remploy.co.uk")
                print("export created for {}".format(email[0]))
            except:
                print("export failed for {}".format(email[0]))
            time.sleep(120) # sleep to avoid goign over quota
        return 0
    
