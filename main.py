
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import json


file1 = open('data.json',"r",encoding='utf-8')
LoadedData = json.load(file1)
LoadedData1={}
EnableHidden=False

def sort(header):
    file1 = open('data.json',"r",encoding='utf-8')
    LoadedData = json.load(file1)

    mi=[]
    dictionary={}
    for x in LoadedData:
        mi.append(LoadedData[x][header])
    mi.sort()
    for i in mi:
        for x in LoadedData:

            if i == LoadedData[x][header]:
                dictionary[x] = {
                    "Username": LoadedData[x]["Username"],
                    "DisplayName": LoadedData[x]["DisplayName"],
                    "Phone": LoadedData[x]["Phone"],
                    "Email": LoadedData[x]["Email"],
                    "UserRole": LoadedData[x]["UserRole"],
                    "Enable": LoadedData[x]["Enable"]
                    }
    return dictionary



def sortenabled(header):
    file1 = open('data.json',"r",encoding='utf-8')
    LoadedData = sortenablednumber()
    print(LoadedData)

    mi=[]
    dictionary={}
    for x in LoadedData:
        mi.append(LoadedData[x][header])
    mi.sort()

    for i in mi:
        for x in LoadedData:
            if (i == LoadedData[x][header]) and (LoadedData[x]["Enable"] == True) :
                dictionary[x] = {
                    "Username": LoadedData[x]["Username"],
                    "DisplayName": LoadedData[x]["DisplayName"],
                    "Phone": LoadedData[x]["Phone"],
                    "Email": LoadedData[x]["Email"],
                    "UserRole": LoadedData[x]["UserRole"],
                    "Enable": LoadedData[x]["Enable"]
                    }


    return dictionary


def sortenablednumber():
    file1 = open('data.json',"r",encoding='utf-8')
    LoadedData = json.load(file1)


    dictionary={}
    nu=1
    for x in LoadedData:
        if (LoadedData[x]["Enable"] == True) :
            dictionary[nu] = {
                "Username": LoadedData[x]["Username"],
                "DisplayName": LoadedData[x]["DisplayName"],
                "Phone": LoadedData[x]["Phone"],
                "Email": LoadedData[x]["Email"],
                "UserRole": LoadedData[x]["UserRole"],
                "Enable": LoadedData[x]["Enable"]
                }
            nu=nu+1
    return dictionary



class MainWidget(BoxLayout):    
    AddWindow = ObjectProperty(None)
    AddSpace = ObjectProperty(None)
    TopBar = ObjectProperty(None)



    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.AddWindow=FormWindow()
        self.AddSpace=SideSpace()

    def refreshtable(self,idnumber,Username,Email,Enable):

        self.ids.userlists.add_widget(BoxLayout(size_hint=(.05,1)))
        self.b1=LineL(text=str(idnumber),size_hint=(.15,1))
        self.ids.userlists.add_widget(self.b1)
        self.b1=LineL(text=Username,size_hint=(.9,1))
        self.ids.userlists.add_widget(self.b1)
        self.b1=LineL(text=Email,size_hint=(.95,1))
        self.ids.userlists.add_widget(self.b1)
        self.b1=LineL(text=str(Enable),size_hint=(.3,1))
        self.ids.userlists.add_widget(self.b1)
        self.ids.userlists.add_widget(BoxLayout(size_hint=(0.05,1)))  


    def press(self,text):
         
        if text=="+ New User":
            self.ids.downwindow.add_widget(self.AddWindow)
            self.ids.downwindow.add_widget(self.AddSpace)
            self.ids.TopBar.ids.SaveUser.disabled = False

        elif text=="Save User":

            Username=(self.AddWindow.ids.Username.text)
            DisplayName=(self.AddWindow.ids.DisplayName.text)
            Phone=(self.AddWindow.ids.Phone.text)
            Email=(self.AddWindow.ids.Email.text)
            UserRole=(self.AddWindow.ids.UserRole.text)
            Enable=(self.AddWindow.ids.Enable.active)
            file1 = open('data.json',"r",encoding='utf-8')
            LoadedData = json.load(file1)
            IdN=len(LoadedData)+1

            if Username=="" or DisplayName=="" or Phone =="" or Email =="" or UserRole=="Sellect a User Role":
                pops = Complete()
                pops.open()    

            else:
                NewUser={IdN:{
                    "Username":Username,
                    "DisplayName":DisplayName, 
                    "Phone":Phone,
                    "Email":Email, 
                    "UserRole":UserRole, 
                    "Enable":Enable}
                    }

                file=open("data.json", "r+",encoding='utf-8')
                data = json.load(file)
                data.update(NewUser)
                file.seek(0)
                json.dump(data, file,ensure_ascii=False, indent=6)

                pops = Saved()
                pops.open()  

                self.ids.downwindow.remove_widget(self.AddWindow)
                self.AddWindow=FormWindow()

                self.ids.downwindow.remove_widget(self.AddSpace)
                self.AddSpace=SideSpace()



                if EnableHidden==False:
                    idnumber=len(LoadedData)+1
                    self.refreshtable(idnumber,Username,Email,Enable)
                    
                #else:
                #    idnumber=len(LoadedData)+1
                #    self.refreshtable(idnumber,Username,Email,"-")

                self.ids.TopBar.ids.NewUser.disabled = False
                self.ids.TopBar.ids.SaveUser.disabled = True

        elif text=="Back":
            self.ids.downwindow.remove_widget(self.AddWindow)
            self.AddWindow=FormWindow()
            self.ids.downwindow.remove_widget(self.AddSpace)
            self.AddSpace=SideSpace()
            self.ids.TopBar.ids.NewUser.disabled = False
            self.ids.TopBar.ids.SaveUser.disabled = True

    def release(self,text):
        if text=="+ New User":
            self.ids.TopBar.ids.NewUser.disabled = True


    def filter(self,text):
        global LoadedData1
        file1 = open('data.json',"r",encoding='utf-8')
        LoadedData = json.load(file1)

        self.ids.userlists.clear_widgets()
        if text=="ID":
            if EnableHidden==True:
                LoadedData1=sortenablednumber()
            else:
                LoadedData1=LoadedData
        elif text=="User Name":
            if EnableHidden==False:
                LoadedData1=sort("Username")
            else:
                LoadedData1=sortenabled("Username")
        elif text=="Email":
            if EnableHidden==False:
                LoadedData1=sort("Email")
            else:
                LoadedData1=sortenabled("Email")
        elif text=="Enable":
            if EnableHidden==False:
                LoadedData1=sort("Enable")
            else:
                pass         
        for x in LoadedData1:
            lineindex=(LoadedData1[x])
            idnumber=x
            Username=(lineindex["Username"])
            Email=(lineindex["Email"])
            Enable=str(lineindex["Enable"])
            self.refreshtable(idnumber,Username,Email,Enable)


    def HideDisable(self,CheckBox,value):
        global EnableHidden
        self.ids.userlists.clear_widgets()

        file1 = open('data.json',"r",encoding='utf-8')
        LoadedData2 = json.load(file1)


        if value =="down":
            EnableHidden=True
            no=1
            for x in LoadedData2:
                lineindex=(LoadedData2[str(x)])
                if (str(lineindex["Enable"])) == "True":
                    idnumber=no
                    Username=(lineindex["Username"])
                    Email=(lineindex["Email"])
                    Enable=str(lineindex["Enable"])
                    self.refreshtable(idnumber,Username,Email,Enable)
                    no+=1
        else:
            EnableHidden=False
            for x in LoadedData2:
                lineindex=(LoadedData2[str(x)])
                idnumber=x
                Username=(lineindex["Username"])
                Email=(lineindex["Email"])
                Enable=str(lineindex["Enable"])
                self.refreshtable(idnumber,Username,Email,Enable)


class MyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def action1(self):
        self.colok =(0.25882352941176473, 0.5215686274509804, 0.9568627450980393, 1)

    def action2(self):
        self.colok =(0.5450980392156862, 0.803921568627451, 0.803921568627451, 1)       


class HeaderButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def action1(self):
        pass

    def action2(self):
        pass


class TopBar(BoxLayout):
    hidecheck = ObjectProperty
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ListHeader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ListArea(ScrollView):
    pass

class UserLists(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for x in LoadedData:
            lineindex=(LoadedData[str(x)])
            idnumber=x
            username=(lineindex["Username"])
            email=(lineindex["Email"])
            enable=str(lineindex["Enable"])
            self.create(idnumber,username,email,enable)

    def create(self,idnumber,username,email,enable):    
        self.add_widget(BoxLayout(size_hint=(.05,1)))
        self.b1=LineL(text=idnumber,size_hint=(.15,1))
        self.add_widget(self.b1)
        self.b1=LineL(text=username,size_hint=(.9,1))
        self.add_widget(self.b1)
        self.b1=LineL(text=email,size_hint=(.95,1))
        self.add_widget(self.b1)
        self.b1=LineL(text=enable,size_hint=(.3,1))
        self.add_widget(self.b1)
        self.add_widget(BoxLayout(size_hint=(0.05,1)))

class FormWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LineL(Label):
    pass

class SideSpace(BoxLayout):
    pass

class MySpinner(Spinner):
    def __init__(self, **kwargs):
        super(MySpinner, self).__init__(**kwargs)
        self.dropdown_cls = SpinnerDropdown
        self.option_cls = SpinnerOptions
    UserRoles=("Guest","Admin","SuperAdmin")

class SpinnerOptions(SpinnerOption):
    pass

class SpinnerDropdown(DropDown):
    pass

class Complete(Popup):
    pass

class Saved(Popup):
    pass

class UI_ExampleApp(App):
    pass

UI_ExampleApp().run()
