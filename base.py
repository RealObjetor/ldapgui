#### Carga de módulos.
import sys
import ldapoperations
import loadconfig
import interface

class ConfigNotFound(Exception):
  pass
class ConfigError(Exception):
  pass

#### Definicion de variables o constantes.
bindResult=False
serverConfig={}
SrvDSAInfo={}
credentials={}

print("Cargar configuración.")
try:
  serverConfig, credentials=loadconfig.LoadConfig()
  ## El fichero de configuracion existe.
  if (not serverConfig) and (not credentials):
    raise ConfigNotFound
  ## Configuracion correcta
  if (not serverConfig) or (not credentials):
    raise ConfigError
except ConfigNotFound:
  print("Config file not found.")
  sys.exit(1)
except ConfigError:
  print("There is an error within the config file.")
  sys.exit(1)

rootWindow=interface.initTk()
## Informacion sobre geometria de ventana.
screenWidth=rootWindow.winfo_screenwidth()
screenHeight=rootWindow.winfo_screenheight()
rootWindow.geometry("640x480+150+150")
rootWindow.minsize(640,480)
mainConsole=interface.LDAPConsole()

#print("Inicializar entorno LDAP.")
srvObject, connObject=ldapoperations.BeginLdap(ldapServer=serverConfig["ldapServer"],ldapPort=serverConfig["ldapPort"],ldapCredentials=credentials)
#print("El tipo de srvObject es {}.".format(type(srvObject)))
#print("El objeto srvObject contiene la siguiente información {}.".format(srvObject))
#print("El tipo de connObject es {}.".format(type(connObject)))
#print("El objeto connObject contiene la siguiente información {}.".format(connObject))

#print("Conexion y bind con el servidor LDAP.")
bindResult=ldapoperations.LdapBind(connObject)
if bindResult:
  print("Bind realizado correctamente - {}.".format(bindResult))
  print("Obteniendo informacion de serviddor LDAP.")
  SrvDSAInfo=ldapoperations.GetDSAInfo(srvObject)
  print("Vendor del LDAP Server - {}.".format(SrvDSAInfo["Vendor"]))
  print("Version del LDAP Server - {}.".format(SrvDSAInfo["VendorVersion"]))
  print("Contextos disponibles - {}.".format(SrvDSAInfo["NamingContexts"]))
  print("Tipo de dato de NamingContexts {}.".format(type(SrvDSAInfo["NamingContexts"])))
  print("Other attributes {}".format(SrvDSAInfo["OtherAttrs"]))
  print(srvObject.info)
else:
  print("Error en el bind - {}.".format(bindResult)) 

#print("Leer el schema completo del servidor LDAP.")
#print(srvObject.schema)
#print("Leer el árbol completo del servidor LDAP.")
print("Los naming contexts disponibles son los siguientes: {}.".format(SrvDSAInfo["NamingContexts"]))
## Busqueda base desde el raiz.
ldapoperations.SearchLdap(connObject,rootSearch=SrvDSAInfo["NamingContexts"][0],scopeSearch="LEVEL")
print(connObject.entries)
#print("El tipo de objeto entries es {}.".format(type(connObject.entries)))
interface.displayEntry(mainConsole,SrvDSAInfo["NamingContexts"][0],10)
rowPos=30
treeLine=[]
for ldapentry in connObject.response:
  treeLine.append(interface.displayEntry(mainConsole,ldapentry['dn'],rowPos))
  rowPos+=20
  print(ldapentry)

print("Realizar representación gráfica del árbol del servidor LDAP.")

connObject.unbind()
rootWindow.mainloop()

exit(0)
