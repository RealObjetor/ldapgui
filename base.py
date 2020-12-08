#### Carga de módulos.
import sys
import ldapoperations
import loadconfig

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

print("Inicializar entorno LDAP.")
srvObject, connObject=ldapoperations.BeginLdap(ldapServer=serverConfig["ldapServer"],ldapPort=serverConfig["ldapPort"],ldapCredentials=credentials)
print("El tipo de srvObject es {}.".format(type(srvObject)))
print("El objeto srvObject contiene la siguiente información {}.".format(srvObject))
print("El tipo de connObject es {}.".format(type(connObject)))
print("El objeto connObject contiene la siguiente información {}.".format(connObject))

print("Conexion y bind con el servidor LDAP.")
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

print("Leer el schema completo del servidor LDAP.")
#print(srvObject.schema)
print("Leer el árbol completo del servidor LDAP.")
ldapoperations.SearchLdap(connObject,rootSearch=SrvDSAInfo["NamingContexts"][0],scopeSearch="SUBTREE")
#print(connObject.entries)
print("El tipo de objeto entries es {}.".format(type(connObject.entries)))
contador=1
for ldapentry in connObject.entries:
  print("Entrada {}".format(contador))
  print(ldapentry)
  contador=contador+1

print("Realizar representación gráfica del árbol del servidor LDAP.")

connObject.unbind()

exit(0)
