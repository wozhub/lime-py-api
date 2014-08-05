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
            response = f.read()
            return json.loads(response)

        except:
            e = sys.exc_info()[0]
            print ("<p>Error: %s</p>" % e)

    def delete_survey(self, sid):
        data = """{ "id": 1,
                    "method": "delete_survey",
                    "params": { "sSessionKey": "%s",
                                "iSurveyID": %s } }""" % (self.session_key,
                                                          sid)
        return self._obtenerJson(data)['result']

    def set_survey_property(self, sid, prop, value):
        data = """{ "id": 1,
                    "method": "set_survey_properties",
                    "params": { "sSessionKey": "%s",
                                "iSurveyID": %s,
                                "aSurveySettings": { "%s": "%s" }
            } }""" % (self.session_key, sid, prop, value)
        return self._obtenerJson(data)['result']

    def get_survey_properties(self, sid, settings=None):

        if settings is None:
            settings = """ [
            "sid","savetimings","allowprev","tokenanswerspersistence",
            "showgroupinfo","showwelcome","owner_id","template","printanswers",
            "assessments","shownoanswer","showprogress","admin","language",
            "ipaddr","usecaptcha","showqnumcode","allowjumps","active",
            "additional_languages","refurl","usetokens","bouncetime",
            "navigationdelay","expires","datestamp","datecreated",
            "bounce_email","bounceprocessing","nokeyboard","startdate",
            "usecookie","publicstatistics","attributedescriptions",
            "bounceaccounttype","alloweditaftercompletion","adminemail",
            "allowregister","publicgraphs","emailresponseto",
            "bounceaccounthost","googleanalyticsstyle","anonymized",
            "allowsave","listpublic","emailnotificationto","bounceaccountpass",
            "googleanalyticsapikey","faxto","autonumber_start","htmlemail",
            "tokenlength","bounceaccountencryption","format","autoredirect",
            "sendconfirmation","showxquestions","bounceaccountuser" ] """

        data = """{ "id": 1,
                    "method": "get_survey_properties",
                    "params": { "sSessionKey": "%s",
                                "iSurveyID": %s,
                                "aSurveySettings": %s
            } }""" % (self.session_key, sid, settings)
        return self._obtenerJson(data)['result']

    def get_summary(self, sid):
        data = """{ "id": 1,
                    "method": "get_summary",
                    "params": { "sSessionKey": "%s",
                                "iSurveyID": %s,
                                "sStatname": "all" } }""" % (self.session_key,
                                                             sid)
        return self._obtenerJson(data)['result']

    def list_surveys(self):
        json_list_surveys = self._list_surveys()

        encuestas = []
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
                                "SurveyID": %s } }""" % (self.session_key, sid)
        return self._obtenerJson(data)['result']

    def import_survey(self, datos, titulo, sid, tipo='lss'):
        data = """{ "id": 1,
                    "method": "import_survey",
                    "params": { "sSessionKey": "%s",
                                "sImportData": "%s",
                                "sImportDataType": "%s",
                                "sNewSurveyName": "%s",
                                "DestSurveyID": %d } }""" \
                                % (self.session_key, datos, tipo, titulo, sid)
        return self._obtenerJson(data)['result']

    def release_session_key(self):
        data = """ { "method": "release_session_key",
                     "params": { "sSessionKey" : "%s"},
                     "id":1}' }""" % (self.session_key)
        return self._obtenerJson(data)['result']

    def export_responses(self, sid):
        data = """ {    "id" : 1,
                        "method":"export_responses",
                        "params": { "sSessionKey": "%s",
                                    "iSurveyID":  %s,
                                    "sDocumentType": "csv",
                                    "sHeadingType": "full",
                                    "sResponseType": "long"
                        } } """ % (self.session_key, sid)
        return self._obtenerJson(data)['result']

    def _add_response(self, sid, datos):
        data = """ {          "method":"add_response",
                              "params": { "sSessionKey": "%s",
                                          "iSurveyID": %s,
                                          "aResponseData": %s },
                            "id": 1 } """ % (self.session_key, sid, datos)
        return self._obtenerJson(data)['result']

    def importar_desde_archivo(self, sid, archivo):
        """Esto no funciona!"""
        respuestas = DictReader(open(archivo))

        for r in respuestas:
            print self._add_response(sid, json.dumps(r))

    def _list_groups(self, sid):
        data = """ {          "method":"list_groups",
                              "params": { "sSessionKey": "%s",
                                          "iSurveyID": %s },
                            "id": 1 } """ % (self.session_key, sid)
        return self._obtenerJson(data)['result']

    def list_groups(self, sid):
        json_list_groups = self._list_groups(sid)

        grupos = []
        for g in json_list_groups:
            grupo = g['id']['gid'], g['group_name']
            grupos.append(grupo)

        return grupos

    def _list_questions(self, sid, gid):
        data = """ {          "method":"list_questions",
                              "params": { "sSessionKey": "%s",
                                          "iSurveyID": %s,
                                          "iGroupID": %s },
                            "id": 1 } """ % (self.session_key, sid, gid)
        return self._obtenerJson(data)['result']

    def list_questions(self, sid, gid):
        json_list_questions = self._list_questions(sid, gid)

        preguntas = []
        for q in json_list_questions:
            pregunta = q['id']['qid'], q['question']
            preguntas.append(pregunta)

        return preguntas
