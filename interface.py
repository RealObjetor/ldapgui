from tkinter import Tk, BOTH, Menu
from tkinter.ttk import Frame, Style

class Ejemplo(Frame):
  
  def __init__(self):
    super().__init__()
    self.initConsole()

  def initConsole(self):
    self.master.title("LDAP Management Console")
    self.style=Style()
    self.style.theme_use("alt")

    menubar=Menu(self.master)
    self.master.config(menu=menubar)

    ## Seccion File del menu.
    fileMenu=Menu(menubar)
    fileMenu.add_command(label="Connect",command=self.OpenConnection)
    fileMenu.add_command(label="Disconnect",command=self.CloseConnection)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=self.ExitOption)
    menubar.add_cascade(label="File", menu=fileMenu)
    ## Seccion Advanced del menu.
    AdvancedMenu=Menu(menubar)
    AdvancedMenu.add_command(label="Display Options")
    AdvancedMenu.add_command(label="Verify")
    AdvancedMenu.add_command(label="Configure")
    menubar.add_cascade(label="Advanced", menu=AdvancedMenu)
    ## Seccion Help del menu.
    HelpMenu=Menu(menubar)
    HelpMenu.add_command(label="Show Help")
    HelpMenu.add_command(label="About LDAP GUI")
    menubar.add_cascade(label="Help", menu=HelpMenu)

    self.pack(fill=BOTH, expand=1)

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
