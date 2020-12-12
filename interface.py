from tkinter import Tk, X, Y, BOTH, Menu, Canvas, LEFT, RIGHT, RAISED, NE, W, font, Scrollbar
from tkinter.ttk import Frame, Style

class LDAPConsole(Frame):
  
  def __init__(self):
    super().__init__()
    self.initConsole()

  def initConsole(self):
    self.master.title("LDAP Management Console")
    self.style=Style()
    self.style.theme_use("alt")
    ## Frame principal.
    self.pack(fill=BOTH, expand=1)

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


  def ExitOption(self):
    self.quit()
  def OpenConnection(self):
    self.quit()
  def CloseConnection(self):
    self.quit()

def initTk():
  return Tk()

def oneRightClick(event):
  print("Right clicked mouse on line {}".format(event.widget.gettags(event.widget.find_closest(event.x,event.y))))

def oneLeftClick(event):
  print("Left clicked mouse on line {}".format(event.widget.gettags(event.widget.find_closest(event.x,event.y))))

def displayEntry(mainConsoleObj,textString,yPos):
  lineEntry=mainConsoleObj.treeNavCanvas.create_text(10,yPos,font=("Times",10,"bold"),anchor=W,text="+ {}".format(textString),activefill="red",tags=textString)
  mainConsoleObj.treeNavCanvas.tag_bind(lineEntry,'<Button-1>',oneRightClick)
  mainConsoleObj.treeNavCanvas.tag_bind(lineEntry,'<Button-3>',oneLeftClick,add="+")
  return lineEntry
  
