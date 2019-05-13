from google.oauth2 import service_account
from googleapiclient.discovery import build

def delegate_service(path_file,scopes,user):
    creds = service_account.Credentials.from_service_account_file(path_file,scopes=scopes)
    delegated_creds = creds.with_subject(user)
    service = build('vault', 'v1', credentials=delegated_creds)
    print("Service created")
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
