#!/usr/bin/python

import urllib2
import json
import sys
from csv import DictReader


class Api:
    def __init__(self, url, user, pw):
        self.url = url
        self._user = user
        self._password = pw

        data = """{   "id": 1,
                    "method": "get_session_key",
                    "params": { "username": "%s",
                                "password": "%s" } } """ % (user, pw)

        self.session_key = self._obtenerJson(data)['result']

    def _obtenerJson(self, data):
        # print data
        req = urllib2.Request(url=self.url, data=data)
        req.add_header('content-type', 'application/json')
        req.add_header('connection', 'Keep-Alive')

        try:
            f = urllib2.urlopen(req)
            myretun = f.read()
            return json.loads(myretun)

        except:
            e = sys.exc_info()[0]
            print ("<p>Error: %s</p>" % e)

    def list_surveys(self):
        json_list_surveys = self._list_surveys()

        encuestas=[]
        for e in json_list_surveys:
            encuesta = e['sid'], e['surveyls_title']
            # Me quedo con el SID y el Titulo

            encuestas.append(encuesta)

        return encuestas

    def _list_surveys(self):
        """Devuelve el JSON ENTERO"""
        data = """{ "id": 1,
                    "method": "list_surveys",
                    "params": { "sSessionKey": "%s" } }""" % (self.session_key)

        return self._obtenerJson(data)['result']

    def activate_survey(self, sid):
        data = """{ "id": 1,
                    "method": "activate_survey",
                    "params": { "sSessionKey": "%s",
                                "SurveyID": %d } }""" % (self.session_key, sid)
        return self._obtenerJson(data)['result']

    def import_survey(self, datos, titulo, sid):
        data = """{ "id": 1,
                    "method": "import_survey",
                    "params": { "sSessionKey": "%s",
                                "sImportData": "%s",
                                "sImportDataType": "lss",
                                "sNewSurveyName": "%s",
                                "DestSurveyID": %d } }""" \
                                % (self.session_key, datos, titulo, sid)
        return self._obtenerJson(data)['result']

    def release_session_key(self):
        data = """ { "method": "release_session_key",
                     "params": { "sSessionKey" : "%s"},
                     "id":1}' }""" % (self.session_key)
        return self._obtenerJson(data)['result']

    def export_responses(self, sid):
        data = """ {          "method":"export_responses",
                            "params": { "sSessionKey": "%s",
                                        "iSurveyID":  %d,
                                        "DocumentType": "csv",
                                        "ResponseType": "long",
                                        "sHeadingType": "full" },
                            "id": 1 } """ % (self.session_key, sid)
        return self._obtenerJson(data)['result']

    def _add_response(self, sid, datos):
        data = """ {          "method":"add_response",
                              "params": { "sSessionKey": "%s",
                                          "iSurveyID": %d,
                                          "aResponseData": %s },
                            "id": 1 } """ % (self.session_key, sid, datos)
        return self._obtenerJson(data)['result']

    def importar_desde_archivo(self, sid, archivo):
        respuestas = DictReader(open(archivo))

        for r in respuestas:
            self._add_response(sid, json.dumps(r))
