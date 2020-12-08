##################################
### Modulo de operaciones LDAP ###
##################################
from ldap3 import Server, Connection, ALL, IP_V4_ONLY, SIMPLE, SYNC 
import ldap3.core.exceptions

def BeginLdap(ldapServer="",ldapPort=389,ldapCredentials={},connSSL=False,connTimeout=10):
  
   #print("Los parametros pasados son los siguientes:")
   #print("Servidor LDAP = {}".format(ldapServer))
   #print("Puerto LDAP   = {}.".format(ldapPort))
   #print("Credenciales  = {} - {}.".format(ldapCredentials["user"],ldapCredentials["password"]))

   try:
     srvObject=Server(ldapServer,port=ldapPort,use_ssl=connSSL,get_info=ALL,mode=IP_V4_ONLY,formatter="",connect_timeout=connTimeout)
     ### Control de errores.
     connObject=Connection(srvObject,ldapCredentials["userDN"],ldapCredentials["password"],client_strategy=SYNC,raise_exceptions=True)
     ### Control de errores.
   except OSError as systemError:
     print(systemError)
   else:
     ### Devuelvo los dos objetos.
     return srvObject, connObject

def LdapBind(LdapConnObject):
   try:
     bindResult=LdapConnObject.bind()
   except ldap3.core.exceptions.LDAPSocketOpenError as socketError:
     print("Exception: {}".format(socketError))
     return False
   except ldap3.core.exceptions.LDAPInvalidDNSyntaxResult as invalidDNerror:
     print("Exception: {}".format(invalidDNerror))
     return False
   except ldap3.core.exceptions.LDAPInvalidCredentialsResult as invalidCredentialserror:
     print("Exception: {}".format(invalidCredentialserror))
     return False
   else:
     return bindResult    

def GetDSAInfo(ServerObject):
   DSAInfo={}
   try:
     DSAInfo["NamingContexts"]=ServerObject.info.naming_contexts
     DSAInfo["SupportedControls"]=ServerObject.info.supported_controls
     DSAInfo["SupportedExtensions"]=ServerObject.info.supported_extensions
     DSAInfo["SupportedFeatures"]=ServerObject.info.supported_features
     DSAInfo["SupportedLDAPVersions"]=ServerObject.info.supported_ldap_versions
     DSAInfo["SupportedSASLMechs"]=ServerObject.info.supported_sasl_mechanisms
     DSAInfo["Vendor"]=ServerObject.info.vendor_name
     DSAInfo["VendorVersion"]=ServerObject.info.vendor_version
     DSAInfo["SchemaEntry"]=ServerObject.info.schema_entry
     DSAInfo["OtherAttrs"]=ServerObject.info.other
   except OSError as systemError:
     print(systemError)
   else:
     return DSAInfo 

def SearchLdap(connectionObject,rootSearch="",scopeSearch="BASE",filterSearch="(objectClass=*)"):
   try:
     connectionObject.search(rootSearch,filterSearch,search_scope=scopeSearch, \
                             dereference_aliases=ldap3.DEREF_NEVER, \
                             attributes=["objectClass","uid","cn","name","sn","uidnumber","gidnumber"])
   except OSError as systemError:
     print(systemError)
   except ldap3.core.exceptions.LDAPInvalidFilterError as invalidFilter:
     print("Exception: {}".format(invalidFilter))
   except ldap3.core.exceptions.LDAPInvalidScopeError as invalidScope:
     print("Exception: {}".format(invalidScope))
   except ldap3.core.exceptions.LDAPAttributeError as attributeError:
     print("Exception: {}".format(attributeError))
   except ldap3.core.exceptions.LDAPInvalidDereferenceAliasesError as invalidDereference:
     print("Exception: {}".format(invalidDereference))

     
