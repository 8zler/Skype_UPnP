import sys
import os
sys.path.append('./modules')
import time
import Skype4Py

#Will segfault if Transoprt='x11' isn't there
if os.name == "nt":
	skype = Skype4Py.Skype()
else:
	skype = Skype4Py.Skype(Transport='x11')

#global cmdLine variable. So far is only used for adding people to the auto-answer list
cmdLine = ""

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

def addToUserPending(fileName,nickname):
        f = open(fileName,"a")
        f.write(nickname+"\n")
        f.close()


def init():
##	global cmdLine
##	cmdLine = sys.argv
##	print 'args: ' + str(len(cmdLine))
##
##	#if no contact is specified
##	if len(cmdLine) < 2:
##		print 'Usage: python AutoAnswer.py [user] [user2] [user3] etc...'
##		sys.exit()

	#Connect the Skype object to the Skype client.
	try:
		skype.Attach()
	except Skype4Py.errors.SkypeAPIError:
		print "could not attach, are you logged in?"
	
	#run these functions when these things happen
	skype.OnCallStatus = onCall
	skype.OnUserAuthorizationRequestReceived = acceptFriend
##	for user in skype.UsersWaitingAuthorization:
##                print "User: " + user.Handle + " " + str(user.BuddyStatus)
##                if user.BuddyStatus == 1:
##                        print "User: " + user.Handle + " " + str(user.BuddyStatus)
##                        user.BuddyStatus = 2
		
#converts skype call status to readable text
def callStatusText(status):
	return skype.Convert.CallStatusToText(status)

def acceptFriend(user):
        print "demande recu"
        user._SetIsAuthorized(1)
        print "demande accepteyyy"

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
	#print 'Call status: ' + callStatusText(status)	
	if callStatusText(status) == "Calling":
		if call.PartnerHandle in getUserAuthorized("/home/heitzler/PFE/autorized_person.txt").split(";"):
			call.Answer()
			print "and we respond to the call"
		else:
			skype.SendMessage(call.PartnerHandle,"Sorry you don't have access to this telepresence BOT.")
			call.Finish()
			addToUserPending("/home/heitzler/PFE/pending_authorisation.txt",call.PartnerHandle)
	elif callStatusText(status) == "Call in Progress":
                call.StartVideoSend()
##        elif callStatusText(status) == "Finished" or callStatusText(status) == "Refused":
##                os._exit(0)

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
