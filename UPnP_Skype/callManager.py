import Skype4Py
import os


class CallManager:


    def __init__(self):
        if os.name == "nt":
            self.skype = Skype4Py.Skype()
        else:
            self.skype = Skype4Py.Skype(Transport='x11')
        try:
            self.skype.Attach()
        except Skype4Py.errors.SkypeAPIError:
            print "could not attach, are you logged in?"

    def holdResumeCall(self):
        calls = self.skype.ActiveCalls
        for call in calls:
            status = call._GetStatus()
            if status == Skype4Py.clsOnHold or status == "LOCALHOLD":
                call.Resume()
            if call._GetStatus() == Skype4Py.clsInProgress:
                call.Hold()



    def addFriend(self,nickname):
        requestMessage = "Please accept my request!"
        searchResults = self.skype.SearchForUsers(nickname)
        for res in searchResults:
            print res
            if res._GetHandle() == nickname:
                res.SetBuddyStatusPendingAuthorization(requestMessage)
                print "invite send to "+res._GetHandle()


    def delFriend(self,nickname):
        self.skype.User(nickname)._SetIsAuthorized(0)


    def getAllFriend(self):
        data = ""
        for user in self.skype.Friends:
            data+=user.Handle+";"
        return data[:-1]



    def endCall(self):
        calls = self.skype.ActiveCalls
        for call in calls:
            call.Finish()



    def changeStatus(self):
        user = self.skype.User("genox212")
        skype._SetCurrentUserStatus(Skype4Py.cusAway)



    def getStatus(self):
        return self.skype._GetCurrentUserStatus()


    def setStatus(self,arg):
        if arg:
            self.skype._SetCurrentUserStatus(Skype4Py.cusOnline)
        else:
            self.skype._SetCurrentUserStatus(Skype4Py.cusDoNotDisturb)



    def changeDisplayName(self,newNickname):
        user1 = self.skype._GetCurrentUserProfile()
        user1._SetFullName(newNickname)


    def muteMic(self):
        if len(self.skype.ActiveCalls) > 0:
            if self.skype._GetMute():
                self.skype._SetMute(False)
            else:
                self.skype._SetMute(True)



    def sendMessage(self,nickname,content):
        self.skype.SendMessage(nickname,content)
