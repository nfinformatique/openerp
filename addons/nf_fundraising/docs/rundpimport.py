import xmlrpclib

username = 'admin' #the user
pwd = '6fbF5k5m'      #the password of the user
dbname = 'FGB_OPEN'    #the database

# OpenERP Common login Service proxy object 
sock_common = xmlrpclib.ServerProxy ('http://192.168.1.163:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)

#replace localhost with the address of the server
# OpenERP Object manipulation service 
sock = xmlrpclib.ServerProxy('http://192.168.1.163:8069/xmlrpc/object')

#calling remote ORM create method to create a record 
print "IMPORT DATA"
print sock.execute(dbname, uid, pwd, 'res.partner', 'import_dp', [])
print "MERGING DOUBLES"
print sock.execute(dbname, uid, pwd, 'res.partner', 'merge_doubles', [])
print "GETTING NB PROSPECTUS"
print sock.execute(dbname, uid, pwd, 'res.partner', 'nb_prospectus', [])
