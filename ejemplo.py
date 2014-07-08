#!/usr/bin/python

from limesurvey import Api

# demo de limesurvey
usuario = 'admin'
clave = 'test'
url = 'http://demo.limesurvey.org/index.php?r=admin/remotecontrol'

lime = Api(url, usuario, clave)

for e in lime.list_surveys():

    propiedades = lime.get_survey_properties(e[0], settings='["active"]')

    if propiedades['active'] == 'Y':
        print "La encuesta %s esta activa" % e[0]
        # print lime.get_summary(e[0])
    else:
        print "La encuesta %s no esta activa" % e[0]
        # print lime.delete_survey(e[0])
