import configparser

class ServerConfigError(Exception):
  pass
class CredsConfigError(Exception):
  pass
class configFileNotFound(Exception):
  pass

def LoadConfig(configfile="./ldapgui.ini"):
   
   serverConfig={"ldapServer":"NONE","ldapPort":0}
   credsConfig={"userDN":"NONE","password":"NONE"}

   configFile=configparser.ConfigParser()
   try:
     if(not configFile.read(configfile)):
       raise configFileNotFound
   except configparser.MissingSectionHeaderError:
     print("Missing section headers in {}".format(configfile))
     return serverConfig.clear(), credsConfig.clear()
   except OSError as systemError:
     print(systemError)
   except configFileNotFound:
     print("Configuration file {} was not found.".format(configfile))
     return serverConfig.clear(), credsConfig.clear()

   try:
     if("SERVER" in configFile):
       SERVER=configFile["SERVER"]
       serverConfig["ldapServer"]=SERVER["ipaddress"]
       serverConfig["ldapPort"]=SERVER.getint("ldapPort",389)
     else:
       raise ServerConfigError
     
     if("CREDS" in configFile):
       CREDS=configFile["CREDS"]
       credsConfig["userDN"]=CREDS["user"]
       credsConfig["password"]=CREDS["password"]
     else:
       raise CredsConfigError
   except configparser.NoOptionError:
     print("Specified option not found.")
     serverConfig.clear()
     credsConfig.clear()
   except ServerConfigError:
     print("Error de configuracion de servidor")
     serverConfig.clear()
   except CredsConfigError:
     print("Error de configuracion de credenciales")
     credsConfig.clear()
   finally:
     return serverConfig, credsConfig     
       
