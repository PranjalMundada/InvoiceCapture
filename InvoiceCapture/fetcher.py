# -*- coding: utf-8 -*-

import imaplib, os, email, time
from threading import Thread 
import filetype

class Attachement_Fetcher:
    
    def __init__(self, attachement_listner):
        self.fetcher_thread_flag = 1
        self.listner = attachement_listner
        self.host = "imap.gmail.com"
        self.port = 993
        self.userName = "pranjal.mundada@gmail.com"
        self.passwd = '3'
        self.passwd = "lgntmkrkiosivppn"
        self.image_path = 'received_invoices'
        self.imapSession = ''
    
    def start_fetching (self):
    
        self.fetcher_thread_flag = 1
        self.fetcher_thread = Thread(target = self.fetch_from_gmail)
        self.fetcher_thread.start()
        
        
    def create_session(self):
        self.detach_dir = '.'
        if 'DataFiles' not in os.listdir(self.detach_dir):
            os.mkdir('DataFiles')
        
        self.imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
        typ, accountDetails = self.imapSession.login(self.userName, self.passwd)
        
        if typ != 'OK':
            print ('Not able to sign in!')
            raise Exception("Not able to create email session")
        
        self.imapSession.select('Inbox')
        return self.imapSession
        
    def stop_fetching(self):        
        self.fetcher_thread_flag = 0.
        
        
    def fetch_from_gmail(self):
                
        while(self.fetcher_thread_flag):
            
            if self.imapSession == '':
                print("creating new email session")
                self.imapSession = self.create_session()
                
            #typ, data = self.imapSession.search(None, 'RECENT')
            typ, data = self.imapSession.search(None, '(ALL)',  'SUBJECT "Invoice"')
            
            if typ != 'OK':
                print ('Error searching Inbox.')
                raise
            
            print(data)
            #print('size', data.len())
            
            for msgId in data[0].split():
                print("1")
                typ, messageParts = self.imapSession.fetch(msgId, '(RFC822)')
                print("1B")    
                if typ != 'OK':
                    print ('Error fetching mail.')
                    raise
                print("1C") 
                emailBody = messageParts[0][1]
                print("1D") 
                mail = email.message_from_bytes(emailBody) #.message_from_string(emailBody)
                print("2")
                for part in mail.walk():
                    
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    fileName = part.get_filename()
            
                    if bool(fileName):
                        print("3")
                        
                        filePath = os.path.join(self.detach_dir, 'attachments', fileName)
                        
                        if not os.path.isfile(filePath) :
                            print( fileName)
                            fp = open(filePath, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                            
                        
                        #if filetype.is_image(filePath) == False or filetype.is_video(filePath) == False:
                        #   print("{filename} is a valid image...", filePath)
                        #  os.remove(filePath)
                    
                    print("filetype.is_image(filePath) :",filetype.is_image(filePath))
                            
                      
    
                        #self.attachement_listner.new_document_received(fileName)
            time.sleep(15)
            
        self.imapSession.close()
        self.imapSession.logout()
            

    #def fetch_from_url(self, image_path):
        
#i_f = Attachement_Fetcher(" ")
#i_f.fetch_from_gmail()





'''

while 1:
    mail = imaplib.IMAP4_SSL(imap_ssl_host)
    mail.login(username, password)
    mail.select('inbox')
    result, data = mail.uid('search', None, search_string(uid_max, criteria))
    uids = [int(s) for s in data[0].split()]

    for uid in uids:
        # Have to check again because Gmail sometimes does not obey UID criterion.
        if uid > uid_max:
            result, data = mail.uid('fetch', str(uid), '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    #message_from_string can also be use here
                    print(email.message_from_bytes(response_part[1])) #processing the email here for whatever
            uid_max = uid
mail.logout()
time.sleep(1)


'''
