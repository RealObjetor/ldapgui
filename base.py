#### Carga de modulos.
from tkinter import Tk, X, Y, BOTH, Menu, Canvas, BOTTOM, LEFT, RIGHT, RAISED, NE, W, SW, font, Scrollbar, HORIZONTAL, VERTICAL
from tkinter.ttk import Frame, Style, Treeview
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
    ## Nuevo Frame para contener la representacion del arbol de 
    ## directorio incluyendo las barras de desplazamiento.
    self.treeNavFrame=Frame(self)
    self.treeNavFrame.config(relief=RAISED,borderwidth=2)
    self.treeNavView=Treeview(self.treeNavFrame,show="tree",selectmode="browse")
    ## Definicoin de barras de desplazamiento.
    ## La barra de desplazamiento tiene como padre el Frame pero controla 
    ## el widget treeview.
    ### Barra de desplazamiento horizontal.
    self.HorScrollBar=Scrollbar(self.treeNavFrame,activerelief=RAISED,orient=HORIZONTAL)
    self.HorScrollBar.config(command=self.treeNavView.xview)
    self.HorScrollBar.pack(fill=X,side=BOTTOM)
    ### Barra de desplazamiento vertical.
    self.VerScrollBar=Scrollbar(self.treeNavFrame,activerelief=RAISED,orient=VERTICAL)
    self.VerScrollBar.config(command=self.treeNavView.yview)
    self.VerScrollBar.pack(fill=Y,side=RIGHT)

    self.treeNavFrame.pack(fill=BOTH,side=LEFT)
    self.treeNavView.pack(fill=BOTH,side=LEFT)

    self.treeNavView.config(xscrollcommand=self.HorScrollBar.set,yscrollcommand=self.VerScrollBar.set) 
    ## Nuevo frame para contener la informacion de objetos seleccionados.
    self.infoFrame=Frame(self)
    self.infoFrame.config(relief=RAISED,borderwidth=2)
    self.infoFrameCanvas=Canvas(self.infoFrame,bg="white",width=500,height=400)
    self.infoFrameCanvas.pack(fill=X,anchor=NE)
    self.infoFrame.pack(fill=X,anchor=NE)

  def updateInfoSection(self,dntoSearch,infoToDisplay):
    self.infoFrameCanvas.delete("all")
    self.infoFrameCanvas.create_text(20,20,font=("Liberation Serif Bold",30,"bold"),anchor=W,text="{}".format(dntoSearch[0]))
    row=50
    self.infoFrameCanvas.create_text(20,row,font=("Liberation Serif Bold",20),anchor=W,text="objectClass: ")
    for objclass in infoToDisplay[0]["attributes"]["objectClass"]:
      self.infoFrameCanvas.create_text(160,row,font=("Liberation Serif Bold",10),anchor=W,text="{}".format(objclass))
      row+=20
      print(objclass)

  def __oneRightClick(self,event,ldapconnectionobject):
    print("Right clicked mouse on line {}".format(event.widget.selection()))

  def __oneLeftClick(self,event,ldapconnectionobject):
    ## Por defecto, click sobre cualquier entrada provoca una busqueda de la misma.
    print("Left clicked mouse on line {}".format(event.widget.selection()))
    dntoSearch=event.widget.selection()
    print(dntoSearch[0])
    ldapoperations.SearchLdap(ldapconnectionobject,rootSearch=dntoSearch[0],scopeSearch="BASE")
    self.updateInfoSection(dntoSearch,ldapconnectionobject.response)

  def DisplayAndBind(self,parentID,lineIDX,entryIID,textString,ldapconnectionobject):
    self.treeNavView.insert(parentID,lineIDX,entryIID,open=True,text=textString)
    def lefclickhandler(event, self=self, parameters=ldapconnectionobject):
      return self.__oneLeftClick(event, ldapconnectionobject)
    self.treeNavView.bind('<<TreeviewSelect>>',lefclickhandler)
    def rightclickhandler(event, self=self, parameters=ldapconnectionobject):
      return self.__oneRightClick(event, ldapconnectionobject)
    self.treeNavView.bind('<Button-3>',rightclickhandler)

  def ExitOption(self):
    self.quit()

  def OpenConnection(self):
    self.quit()

  def CloseConnection(self):
    self.quit()

#### Definicion de funciones.

if __name__ == "__main__":
  
  print("Cargar configuracion.")
  try:
    serverConfig, credentials=loadconfig.LoadConfig()
    ## El fichero de configuracion existe.
    if (not serverConfig) and (not credentials):
      raise ConfigNotFound("Configuration file not found.")
    ## Configuracion correcta
    if (not serverConfig) or (not credentials):
      raise ConfigError("There was an error in the configuration file.")
  except ConfigNotFound as e:
    print("Config error - {}".format(e))
    sys.exit(1)
  except ConfigError as e:
    print("Config error - {}".format(e))
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
  #print("Leer el arbol completo del servidor LDAP.")
  print("Los naming contexts disponibles son los siguientes: {}.".format(SrvDSAInfo["NamingContexts"]))
  ## Busqueda base desde el raiz.
  ldapoperations.SearchLdap(connObject,rootSearch=SrvDSAInfo["NamingContexts"][0],scopeSearch="BASE")
  #print(connObject.entries)
  #print("El tipo de objeto entries es {}.".format(type(connObject.entries)))
  ## Primero represento la raiz del naming coontext.
  ## El array treeLine contiene los identificadores de cada linea de texto
  ## que se incluye en el arbol de navegacion. Al acceder a cada uno de ellos
  ## podre hacer busquedas del objeto.
  #treeLine=[]
  mainConsole.DisplayAndBind("","0",SrvDSAInfo["NamingContexts"][0],SrvDSAInfo["NamingContexts"][0],connObject)
  identificador=1
  ldapoperations.SearchLdap(connObject,rootSearch=SrvDSAInfo["NamingContexts"][0],scopeSearch="SUBTREE")
  for ldapentry in connObject.response:
    if(ldapentry['dn'] == SrvDSAInfo["NamingContexts"][0]):
      print("Este no")
      continue
    print(ldapentry)
    parentEntry=ldapentry['dn'][ldapentry['dn'].index(",")+1:]
    mainConsole.DisplayAndBind(parentEntry,identificador,ldapentry['dn'],ldapentry['dn'][0:ldapentry['dn'].index(",")],connObject)
    identificador+=1

  rootWindow.mainloop()
  connObject.unbind()
  print("Limpiando toodo.....")

  sys.exit(0)
