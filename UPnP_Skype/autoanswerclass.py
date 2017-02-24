import sys
import os
sys.path.append('./modules')
import time
import Skype4Py

##Will segfault if Transoprt='x11' isn't there
##if os.name == "nt":
##	skype = Skype4Py.Skype()
##else:
##	skype = Skype4Py.Skype(Transport='x11')
##
##global cmdLine variable. So far is only used for adding people to the auto-answer list
##cmdLine = ""

##call = skype.PlaceCall("sherif.meimari1","randa.nasreldin")
##time.sleep(5)
##call.StartVideoSend()

def getUserAuthorized(fileName):
        f = open(fileName,"r")
        lines = f.readlines()
        res=""
        for line in lines:
                res+=line[:-1]+";"
        res=res[:-1]
        return res

class SkypeAPI:

        def __init__(self):
                self.skype = Skype4Py.Skype()


        def sku(self):
                try:
                        #skype = Skype4Py.Skype()
                        self.skype.Attach()
                except Skype4Py.errors.SkypeAPIError:
                        print "could not attach, are you logged in?"                
                #run these functions when these things happen
                self.skype.OnCallStatus = self.onCall
                self.skype.OnUserAuthorizationRequestReceived = self.acceptFriend
                        
        #converts skype call status to readable text
        def callStatusText(self,status):
                return self.skype.Convert.CallStatusToText(status)

        def acceptFriend(self,user):
                print "demande recu"
                user._SetIsAuthorized(1)
                print "demande accepteyyy"

        #Runs when call status changes
        def onCall(self,call, status):
                global callStatus
                global cmdLine
                print call.PartnerHandle +" is calling...",
                i=1
                calls = self.skype.ActiveCalls
                if len(calls) > 1:
                        self.skype.SendMessage(calls[1].PartnerHandle,"Sorry this teleprense BOT is already in use.")
                        calls[1].Finish()
                        print "but the call is refused"
                callStatus = status	
                if callStatusText(status) == "Calling":
                        if call.PartnerHandle in getUserAuthorized("/home/heitzler/PFE/autorized_person.txt").split(";"):
                                call.Answer()
                                print "and we respond to the call"
                        else:
                                self.skype.SendMessage(call.PartnerHandle,"Sorry you don't have access to this telepresence BOT.")
                                call.Finish()
                elif callStatusText(status) == "Call in Progress":
                        call.StartVideoSend()

        def main(self):
                #run forever~
                while True:
                        time.sleep(1)                        
                        #if skype isn't attached, keep retrying until it works
                        while not self.skype.AttachmentStatus == 0:
                                        try:
                                                self.skype.Attach()
                                        except Skype4Py.errors.SkypeAPIError:
                                                print "could not attach, maybe you're not logged in yet. Waiting 10 seconds..."
                                        time.sleep(10)
			
		
