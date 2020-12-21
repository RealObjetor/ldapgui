#### Carga de módulos.
from tkinter import Tk, X, Y, BOTH, Menu, Canvas, LEFT, RIGHT, RAISED, NE, W, font, Scrollbar
from tkinter.ttk import Frame, Style
import sys
import ldapoperations
import loadconfig

#### Definicion de variables o constantes.
bindResult=False
serverConfig={}
SrvDSAInfo={}
credentials={}

#### Definicion de clases.
class ConfigNotFound(Exception):
  pass
class ConfigError(Exception):
  pass

class LDAPConsole(Frame):

  def __init__(self):
    super().__init__()
    self.initConsole()
    self.addMenuBar()
    self.createSections()

  def initConsole(self):
    self.master.title("LDAP Management Console")
    self.style=Style()
    self.style.theme_use("alt")
    ## Frame principal.
    self.pack(fill=BOTH, expand=1)

  def addMenuBar(self):
    ## Creacion de barra de menus.
    menubar=Menu(self.master)
    self.master.config(menu=menubar)
    ## Seccion File del menu.
    fileMenu=Menu(menubar,tearoff=0)
    fileMenu.add_command(label="Connect",command=self.OpenConnection)
    fileMenu.add_command(label="Disconnect",command=self.CloseConnection)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=self.ExitOption)
    menubar.add_cascade(label="File", menu=fileMenu)
    ## Seccion Advanced del menu.
    AdvancedMenu=Menu(menubar,tearoff=0)
    AdvancedMenu.add_command(label="Display Options")
    AdvancedMenu.add_command(label="Verify")
    AdvancedMenu.add_command(label="Configure")
    menubar.add_cascade(label="Advanced", menu=AdvancedMenu)
    ## Seccion Help del menu.
    HelpMenu=Menu(menubar,tearoff=0)
    HelpMenu.add_command(label="Show Help")
    HelpMenu.add_command(label="About LDAP GUI")
    menubar.add_cascade(label="Help", menu=HelpMenu)

  def createSections(self):
    ## Definicion de frames secundarios anidados en el principal.
    ## Nuevo frame para contener la representacion del arbol de directorio.
    self.treeNavFrame=Frame(self)
    self.treeNavFrame.config(relief=RAISED,borderwidth=2)
    self.treeNavCanvas=Canvas(self.treeNavFrame,bg="white",width=200,height=120)
    self.treeNavCanvas.pack(fill=Y,side=LEFT)
    self.treeNavFrame.pack(fill=Y,side=LEFT)
    ## Nuevo frame para contener la información de objetos seleccionados.
    self.infoFrame=Frame(self)
    self.infoFrame.config(relief=RAISED,borderwidth=2)
    self.infoFrameCanvas=Canvas(self.infoFrame,bg="white",width=500,height=400)
    self.infoFrameCanvas.pack(fill=X,anchor=NE)
    self.infoFrame.pack(fill=X,anchor=NE)

  def updateInfoSection(self,dntoSearch,infoToDisplay):
    self.infoFrameCanvas.delete("all")
    self.infoFrameCanvas.create_text(20,20,font=("Times",40,"bold"),anchor=W,text="{}".format(dntoSearch))
    row=40
    self.infoFrameCanvas.create_text(20,row,font=("Times",30),anchor=W,text="objectClass: ")
    for objclass in infoToDisplay[0]["attributes"]["objectClass"]:
      self.infoFrameCanvas.create_text(100,row,font=("Times",10),anchor=W,text="{}".format(objclass))
      row+=20
      print(objclass)

  def __oneRightClick(self,event):
    print("Right clicked mouse on line {}".format(event.widget.gettags(event.widget.find_closest(event.x,event.y))))

  def __oneLeftClick(self,event,ldapconnectionobject):
    ## Por defecto, click sobre cualquier entrada provoca una busqueda de la misma.
    print("Left clicked mouse on line {}".format(event.widget.gettags(event.widget.find_closest(event.x,event.y))))
    dntoSearch=event.widget.gettags(event.widget.find_closest(event.x,event.y))[0]
    print(dntoSearch)
    ldapoperations.SearchLdap(ldapconnectionobject,rootSearch=dntoSearch,scopeSearch="BASE")
    self.updateInfoSection(dntoSearch,ldapconnectionobject.response)

  def DisplayAndBind(self,textString,rowPos,colPos,ldapconnectionobject):
    self.treeNavCanvas.create_text(colPos,rowPos,font=("Times",10,"bold"),anchor=W,text="+ {}".format(textString),activefill="red",tags=textString)
    def lefclickhandler(event, self=self, parameters=ldapconnectionobject):
      return self.__oneLeftClick(event, ldapconnectionobject)
    self.treeNavCanvas.tag_bind(textString,'<Button-1>',lefclickhandler)
     
    self.treeNavCanvas.tag_bind(textString,'<Button-3>',self.__oneRightClick,add="+")

  def ExitOption(self):
    self.quit()
  def OpenConnection(self):
    self.quit()
  def CloseConnection(self):
    self.quit()

#### Definicion de funciones.

if __name__ == "__main__":
  
  print("Cargar configuración.")
  try:
    serverConfig, credentials=loadconfig.LoadConfig()
    ## El fichero de configuracion existe.
    if (not serverConfig) and (not credentials):
      raise ConfigNotFound("No se encontro el puto fichero.")
    ## Configuracion correcta
    if (not serverConfig) or (not credentials):
      raise ConfigError("Hay un puto error en el puto fichero.")
  except ConfigNotFound as e:
    print("Config file not found. {}".format(e))
    sys.exit(1)
  except ConfigError as e:
    print("There is an error within the config file. {}".format(e))
    sys.exit(1)
  
  srvObject, connObject=ldapoperations.BeginLdap(ldapServer=serverConfig["ldapServer"],ldapPort=serverConfig["ldapPort"],ldapCredentials=credentials)
  bindResult=ldapoperations.LdapBind(connObject)
  if bindResult:
    SrvDSAInfo=ldapoperations.GetDSAInfo(srvObject)
    #print("Bind realizado correctamente - {}.".format(bindResult))
    #print("Obteniendo informacion de serviddor LDAP.")
    #print("Vendor del LDAP Server - {}.".format(SrvDSAInfo["Vendor"]))
    #print("Version del LDAP Server - {}.".format(SrvDSAInfo["VendorVersion"]))
    #print("Contextos disponibles - {}.".format(SrvDSAInfo["NamingContexts"]))
    #print("Tipo de dato de NamingContexts {}.".format(type(SrvDSAInfo["NamingContexts"])))
    #print("Other attributes {}".format(SrvDSAInfo["OtherAttrs"]))
    #print(srvObject.info)
  else:
    print("Error en el bind - {}.".format(bindResult))
    sys.exit(1)

  ## Creacion de ventana principal.
  rootWindow=Tk()
  screenWidth=rootWindow.winfo_screenwidth()
  screenHeight=rootWindow.winfo_screenheight()
  rootWindow.geometry("640x480+150+150")
  rootWindow.minsize(640,480)
  mainConsole=LDAPConsole()

  #print("Leer el schema completo del servidor LDAP.")
  #print(srvObject.schema)
  #print("Leer el árbol completo del servidor LDAP.")
  print("Los naming contexts disponibles son los siguientes: {}.".format(SrvDSAInfo["NamingContexts"]))
  ## Busqueda base desde el raiz.
  ldapoperations.SearchLdap(connObject,rootSearch=SrvDSAInfo["NamingContexts"][0],scopeSearch="LEVEL")
  print(connObject.entries)
  #print("El tipo de objeto entries es {}.".format(type(connObject.entries)))
  ## Primero represento la raiz del naming coontext.
  ## El array treeLine contiene los identificadores de cada linea de texto
  ## que se incluye en el izquierdo de navegacion. Al acceder a cada uno de ellos
  ## podre hacer busquedas del objeto.
  #treeLine=[]
  #treeLine.append(DisplayAndBind(mainConsole,SrvDSAInfo["NamingContexts"][0],10,10))
  mainConsole.DisplayAndBind(SrvDSAInfo["NamingContexts"][0],10,10,connObject)
  yPos=30
  xPos=20
  for ldapentry in connObject.response:
    #treeLine.append(DisplayAndBind(mainConsole,ldapentry['dn'],yPos,xPos))
    mainConsole.DisplayAndBind(ldapentry['dn'],yPos,xPos,connObject)
    yPos+=20
    print(ldapentry)

  rootWindow.mainloop()
  connObject.unbind()
  print("Limpiando toodo.....")

  sys.exit(0)
