#!/usr/bin/python

from limesurvey import Api

#demo de limesurvey
usuario = 'admin'
clave = 'test'
url = 'http://demo.limesurvey.org/index.php?r=admin/remotecontrol'

lime = Api(url,usuario,clave)

for e in lime.list_surveys():
    print e
