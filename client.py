import wx
import telnetlib
from time import sleep
import _thread as thread

class LoginFrame(wx.Frame):
    """
    Login Frame using Pythonwx GUI
    """
    def __init__(self, parent, id, title, size):
        # Initialize the component
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.serverAddressLabel = wx.StaticText(self, label="Enter the Server Address:", pos=(10, 50), size=(120, 25))
        self.userNameLabel = wx.StaticText(self, label="User Name:", pos=(40, 100), size=(120, 25))
        self.serverAddress = wx.TextCtrl(self, pos=(120, 47), size=(150, 25))
        self.userName = wx.TextCtrl(self, pos=(120, 97), size=(150, 25))
        self.loginButton = wx.Button(self, label='Login', pos=(80, 145), size=(130, 30))
        # Bind the button with self.login function
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        # show the frame
        self.Show()

    def login(self, event):
        # Handle login (when click the Button)
        try:
            serverAddress = self.serverAddress.GetLineText(0).split(':')
            con.open(serverAddress[0], port=int(serverAddress[1]), timeout=10)
            response = con.read_some()
            if response != b'Connect Success':
                self.showDialog('Error', 'Connect Fail!', (200, 100))
                return
            con.write(('login ' + str(self.userName.GetLineText(0)) + '\n').encode("utf-8"))
            response = con.read_some()
            if response == b'UserName Empty':
                self.showDialog('Error', 'UserName Empty!', (200, 100))
            elif response == b'UserName Exist':
                self.showDialog('Error', 'UserName Exist!', (200, 100))
            else:
                self.Close()
                ChatFrame(None, 2, title='Test Chat Client', size=(500, 400))
        except Exception:
            self.showDialog('Error', 'Connect Fail!', (95, 20))

    def showDialog(self, title, content, size):
        # Display the dialog window
        dialog = wx.Dialog(self, title=title, size=size)
        dialog.Center()
        wx.StaticText(dialog, label=content)
        dialog.ShowModal()



# window Frame
class ChatFrame(wx.Frame):
    """
    Chat Frame using Pythonwx GUI
    """

    def __init__(self, parent, id, title, size):
        # Initialize the GUI and bind all parts
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.chatFrame = wx.TextCtrl(self, pos=(5, 5), size=(490, 310), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.message = wx.TextCtrl(self, pos=(5, 320), size=(300, 25))
        self.sendButton = wx.Button(self, label="Send", pos=(310, 320), size=(58, 25))
        self.usersButton = wx.Button(self, label="Users", pos=(373, 320), size=(58, 25))
        self.closeButton = wx.Button(self, label="Close", pos=(436, 320), size=(58, 25))
        # send button bind with self.send() function
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)
        # users button bind with the look Users function
        self.usersButton.Bind(wx.EVT_BUTTON, self.lookUsers)
        # close the session window 
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)
        thread.start_new_thread(self.receive, ())
        self.Show()

    def send(self, event):
        # send message, e.g. write data to the socket (to) server
        message = str(self.message.GetLineText(0)).strip()
        if message != '':
            con.write(('say ' + message + '\n').encode("utf-8"))
            self.message.Clear()

    def lookUsers(self, event):
        # look for Users (send request to server)
        con.write(b'look\n')

    def close(self, event):
        # look for Users (send request to server)
        con.write(b'logout\n')
        # after telling server I'm out, just close the socket here
        con.close()
        self.Close()

    def receive(self):
        # accept the message send by serve
        while True:
            sleep(0.6)
            result = con.read_very_eager()
            if result != '':
                self.chatFrame.AppendText(result)

if __name__ == '__main__':
    app = wx.App()
    # send connect() through Telnet() and create socket to communicate to server
    con = telnetlib.Telnet()
    LoginFrame(None, -1, title="Login", size=(320, 250))
    app.MainLoop()



