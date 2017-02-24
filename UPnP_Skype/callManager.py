import Skype4Py
import os


class CallManager:
    

    def holdcall(self):
        if os.name == "nt":
            skype = Skype4Py.Skype()
        else:
            skype = Skype4Py.Skype(Transport='x11')
        try:
            skype.Attach()
        except Skype4Py.errors.SkypeAPIError:
            print "could not attach, are you logged in?"
        calls = skype.ActiveCalls
        for call in calls:
            call.Hold()


    def resumecall(self):
        if os.name == "nt":
            skype = Skype4Py.Skype()
        else:
            skype = Skype4Py.Skype(Transport='x11')
        try:
            skype.Attach()
        except Skype4Py.errors.SkypeAPIError:
            print "could not attach, are you logged in?"
        calls = skype.ActiveCalls
        for call in calls:
            call.Resume()


    def addFriend(self,nickname):
        if os.name == "nt":
            skype = Skype4Py.Skype()
        else:
            skype = Skype4Py.Skype(Transport='x11')
        try:
            skype.Attach()
        except Skype4Py.errors.SkypeAPIError:
            print "could not attach, are you logged in?"
        requestMessage = "Please accept my request!"
        searchResults = skype.SearchForUsers(nickname)
        print "tout lesdsofhsjhgfhkjsgdfjsss"
        print searchResults
        for res in searchResults:
            print res
            if res._GetHandle() == nickname:
                res.SetBuddyStatusPendingAuthorization(requestMessage)
                print "invite send to "+res._GetHandle()



    def sendMessage(self,nickname,content):
        if os.name == "nt":
            skype = Skype4Py.Skype()
        else:
            skype = Skype4Py.Skype(Transport='x11')
        try:
            skype.Attach()
        except Skype4Py.errors.SkypeAPIError:
            print "could not attach, are you logged in?"
        skype.SendMessage(nickname,content)
