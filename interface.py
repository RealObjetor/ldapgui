from tkinter import Tk, Y, BOTH, Menu, Canvas, LEFT, RIGHT, RAISED, NE
from tkinter.ttk import Frame, Style

class Ejemplo(Frame):
  
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
    treeNavFrame=Frame(self)
    treeNavFrame.config(relief=RAISED,borderwidth=2)
    treeNavCanvas=Canvas(treeNavFrame,bg="white",width=200,height=120)
    treeNavCanvas.pack(fill=Y,side=LEFT)
    treeNavFrame.pack(fill=Y,side=LEFT)
    ## Nuevo frame para contener la información de objetos seleccionados.
    infoFrame=Frame(self)
    infoFrame.config(relief=RAISED,borderwidth=2)
    infoFrameCanvas=Canvas(infoFrame,bg="white",width=500,height=200)
    infoFrameCanvas.pack(anchor=NE)
    infoFrame.pack(anchor=NE)

  def ExitOption(self):
    self.quit()
  def OpenConnection(self):
    self.quit()
  def CloseConnection(self):
    self.quit()

def main():
  ventanaRaiz=Tk()
  ventanaRaiz.geometry("700x500+150+150")
  ventanaRaiz.minsize(380,180)
  consola=Ejemplo()
  ventanaRaiz.mainloop()
    
if __name__ == '__main__':
  main()
