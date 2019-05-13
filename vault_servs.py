from google.oauth2 import service_account
from googleapiclient.discovery import build



class Google_Service:
    def __init__(self, file, scopes, user):
        self.file = file
        self.scopes = scopes
        self.user = user
    
    def create_service(self):
        creds = service_account.Credentials.from_service_account_file(self.file,scopes=self.scopes)
        delegated_creds = creds.with_subject(self.user)
        service = build('vault', 'v1', credentials=delegated_creds)
        print("Service created")
        return service
    
    

class Matter_Exports(Google_Service):
    def __init__(self,service,matter_id):
        self.matter_id = matter_id
        self.service = service
        self.exports = service.matters().exports().list(matterId=matter_id).execute().get('exports',[])
        if self.exports:
            print("Matter created")
    
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
