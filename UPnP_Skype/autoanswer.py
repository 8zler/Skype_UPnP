import sys
import os
sys.path.append('./modules')
import time
import Skype4Py

if os.name == "nt":
	skype = Skype4Py.Skype()
else:
	skype = Skype4Py.Skype(Transport='x11')

cmdLine = ""



def getUserAuthorized(file):
        f = open(file,"r")
        lines = f.read()
        lines = lines[:-1]
        res=lines.split(";")
        if res[-1] == '' or res[-1] == ';' or res[-1] == '\n':
                return ";".join(res)[:-1]
        return ";".join(res)


def addToUserPending(fileName,nickname):
        if len(nickname) > 0:                
                f = open(fileName,"a")
                data = getUserAuthorized(fileName).split(";")
                if nickname not in data:
                        f.write(nickname+";")
                        f.close()





def init():
	try:
		skype.Attach()
	except Skype4Py.errors.SkypeAPIError:
		print "could not attach, are you logged in?"	
	#run these functions when these things happen
	skype.OnCallStatus = onCall
	skype.OnUserAuthorizationRequestReceived = acceptFriend
def callStatusText(status):
	return skype.Convert.CallStatusToText(status)

def acceptFriend(user):
        print "demande receive"
        user._SetIsAuthorized(1)
        print "demande accepted"

#Runs when call status changes
def onCall(call, status):
	global callStatus
	global cmdLine
	print call.PartnerHandle +" is calling...",
	i=1
	calls = skype.ActiveCalls
	if len(calls) > 1:
                skype.SendMessage(calls[1].PartnerHandle,"Sorry this teleprense BOT is already in use.")
                calls[1].Finish()
                print "but the call is refused"
	callStatus = status	
	if callStatusText(status) == "Calling":
		if call.PartnerHandle in getUserAuthorized("/home/heitzler/PFE/authorized_person.txt").split(";"):
			call.Answer()
			print "and we respond to the call"
		else:
			skype.SendMessage(call.PartnerHandle,"Sorry you don't have access to this telepresence BOT.")
			call.Finish()
			addToUserPending("/home/heitzler/PFE/pending_authorisation.txt",call.PartnerHandle)
	elif callStatusText(status) == "Call in Progress":
                call.StartVideoSend()

def main():

	#run forever~
	while True:
		time.sleep(1)
		
		#if skype isn't attached, keep retrying until it works
		while not skype.AttachmentStatus == 0:
				try:
					skype.Attach()
				except Skype4Py.errors.SkypeAPIError:
					print "could not attach, maybe you're not logged in yet. Waiting 10 seconds..."
				time.sleep(10)
			
		
init()
main()
