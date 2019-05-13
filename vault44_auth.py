from __future__ import print_function
from google.auth.transport.requests import AuthorizedSession
from open.globals import *
import vault_servs

import csv
import time
import sys


class App:
    def __init__(self):
        pass
      

        
        
#get csv file, parse into list, slice to avoid previously created exports/headers
email_list= [a for a in csv.reader(open("./eml_list4.csv","r"))][2:]


#set up service and matter to create exports in
va_service = vault_servs.delegate_service(SERVICE_FILE,SCOPES,STD_USER)
va_matter = vault.servs.Matter_Exports(va_service, STD_MATTER)


#loop through email list and create an export per email.  Catch any failed exports in try/except
for email in email_list:
    try:
        created = va_matter.create_export(email[0]+"@remploy.co.uk")
        print("export created for {}".format(email[0]))
    except:
        print("export failed for {}".format(email[0]))
    time.sleep(120) # sleep to avoid goign over quota
    

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
