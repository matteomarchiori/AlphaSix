"""
File: api.py
Data creazione: 2019-03-20

<descrizione>

Licenza: Apache 2.0

Copyright 2019 AlphaSix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Versione: 0.1.0
Creatore: Matteo Marchiori, matteo.marchiori@gmail.com
Autori:
"""

import json
import datetime

from flask import request
import flask_restful
from bson.json_util import dumps

from mongo_db.facade import MongoFacade
from gestore_personale.observer import Subject


class SubjectResource(type(Subject), type(flask_restful.Resource)):
    pass


class Resource(Subject, flask_restful.Resource, metaclass=SubjectResource):

    def __init__(self, model: MongoFacade):
        super(Resource, self).__init__()
        self._model = model

    def notify(self, request_type: str, resource: str, url: str, msg: str):
        for obs in self._lst:
            return obs.update(request_type, resource, url, msg)


class User(Resource):

    def get(self, url: str):
        return self.notify('user', 'GET', url, None)

    def put(self, url: str):
        data = request.get_json(force=True)
        return self.notify('user', 'PUT', url, data)

    def delete(self, url: str):
        return self.notify('user', 'DELETE', url, None)


class PostUser(Resource):

    def post(self):
        """
        Usage example:
            `curl http://localhost:5000/users -X POST -d "data=some data"`
        """
        data = request.get_json(force=True)
        return self.notify('user', 'POST', None, data)


class Project(Resource):

    def get(self, url: str):
        return self.notify('project', 'GET', url, None)

    def delete(self, url: str):
        return self.notify('project', 'DELETE', url, None)


class Preference(Resource):

    def put(self, url: str) -> dict:
        data = request.get_json(force=True)
        return self.notify('preference', 'PUT', url, data)


class ApiHandler:

    def __init__(
        self,
        model: MongoFacade
    ):
        self._model = model

    def api_user(self, request_type: str, url: str, msg: str):
        if request_type == 'GET':
            try:
                user = self._model.read_user(url)
                userjson = json.loads(dumps(user))
                for i, data in enumerate(userjson['irreperibilita']):
                    userjson['irreperibilita'][i]['$date'] = datetime.datetime.strftime(
                        datetime.datetime.fromtimestamp(
                            userjson['irreperibilita'][i]['$date']/1000
                        ),
                        format="%Y-%m-%d"
                    )
                return userjson
            except AssertionError:
                return {'error': 'Utente inesistente.'}, 404
        elif request_type == 'PUT':
            nome = msg.get('name')
            cognome = msg.get('surname')
            email = msg.get('email')
            telegram = msg.get('telegram')
            modify = {}
            oldmail = self._model.get_user_email_web(url)
            oldtelegram = self._model.get_user_telegram_web(url)
            userid = oldmail if oldmail else oldtelegram
            if email or telegram:
                if nome:
                    modify.update(nome=nome)
                if cognome:
                    modify.update(cognome=cognome)
                if email:
                    modify.update(email=email)
                if telegram:
                    modify.update(telegram=telegram)
                if ((
                    email and
                    self._model.user_exists(email) and
                    email != oldmail
                )or(
                    telegram and
                    self._model.user_exists(telegram) and
                    telegram != oldtelegram
                    )
                ):
                    return {'error': 'I dati inseriti confliggono\
 con altri già esistenti.'}, 409
                if('nome' in modify):
                    self._model.update_user_name(
                        userid,
                        modify['nome']
                    )
                if('cognome' in modify):
                    self._model.update_user_surname(
                        userid,
                        modify['cognome']
                    )
                if(
                    'email' in modify and (
                    (not oldmail) or
                    (modify['email'] != oldmail)
                )):
                    self._model.update_user_email(
                        userid,
                        modify.get('email')
                    )
                    userid = modify['email']
                if('telegram' in modify and (
                    (not oldtelegram) or
                    (modify['telegram'] != oldtelegram)
                )):
                    self._model.update_user_telegram(
                        userid,
                        modify.get('telegram')
                    )
                    userid = modify['telegram']
                if('email' not in modify):
                    self._model.update_user_email(
                        userid,
                        ''
                    )
                    if oldmail:
                        userid = modify['telegram']
                    self._model.update_user_preference(
                        userid,
                        'telegram'
                    )
                if('telegram' not in modify):
                    self._model.update_user_telegram(
                        userid,
                        ''
                    )
                    if oldtelegram:
                        userid = modify['email']
                    self._model.update_user_preference(
                        userid,
                        'email'
                    )
                return {'ok': 'Utente modificato correttamente.'}, 200
            else:
                return {'error': 'Si prega di inserire almeno email o\
 telegram per modificare l\'utente.'}, 400
        elif request_type == 'DELETE':
            if url:
                self._model.delete_user(url)
                return {'ok': 'Utente rimosso correttamente'}, 200
            return {'error': 'Si prega di inserire almeno email o telegram \
per rimuovere l\'utente.'}, 409
        elif request_type == 'POST':
            nome = msg.get('name')
            cognome = msg.get('surname')
            email = msg.get('email')
            telegram = msg.get('telegram')
            if email or telegram:
                if (
                    (email and self._model.user_exists(email)) or
                    (telegram and self._model.user_exists(telegram))
                ):
                    return {'error': 'L\'utente inserito esiste già.'}, 409
                else:
                    self._model.insert_user(
                        name=nome,
                        surname=cognome,
                        email=email,
                        telegram=telegram
                    )
                    if email:
                        self._model.update_user_preference(email, 'email')
                    elif telegram:
                        self._model.update_user_preference(
                            telegram,
                            'telegram'
                        )
                    return {'ok': 'Utente inserito correttamente'}, 200
            else:
                return {'error': 'Si prega di inserire almeno email o telegram\
 per inserire l\'utente.'}, 409


    def api_project(self, request_type: str, url: str, msg: str):
        if request_type == 'GET':
            project = self._model.read_project(url)
            projectjson = json.loads(dumps(project))
            return projectjson
        elif request_type == 'DELETE':
            if url:
                users = self._model.get_project_users(url)
                for user in users:
                    if user.get('email'):
                        userid = user['email']
                    elif user.get('telegram'):
                        userid = user['telegram']
                    self._model.remove_user_project(userid, url)
                self._model.delete_project(url)
                return {'ok': 'Progetto rimosso correttamente'}, 200
            return {'error': 'Si prega di inserire l\'url \
per rimuovere il progetto.'}, 409

    def api_preference(self, request_type: str, url: str, msg: str):
        tipo = msg.get('tipo')
        if tipo == 'progetto':
            project = msg.get('project')
            priority = msg.get('priority')
            topics = msg.get('topics')
            keywords = msg.get('keywords')
            self._model.set_user_priority(
                url, project, priority
            )
            self._model.reset_user_topics(
                url,
                project
            )
            for topic in topics:
                self._model.add_user_topics(
                    url,
                    project,
                    topic
                )
            self._model.reset_user_keywords(
                url,
                project
            )
            for keyword in keywords:
                self._model.add_user_keywords(
                    url,
                    project,
                    keyword
                )
            return {'ok': 'Preferenza modificata correttamente'}, 200
        elif tipo == 'irreperibilita':
            giorni = msg.get('giorni')
            giorni_old = self._model.read_user(
                url
            ).get('irreperibilita')
            giorni_new = []
            for giorno in giorni:
                giorni_new.append(
                    datetime.datetime.strptime(giorno, '%Y-%m-%d')
                )
            if giorni_new:
                year = giorni_new[0].strftime('%Y')
                month = giorni_new[0].strftime('%m')
                for giorno in giorni_old:
                    if (
                        giorno.strftime('%Y') == year and
                        giorno.strftime('%m') == month
                    ):
                        if giorno not in giorni_new:
                            self._model.remove_giorno_irreperibilita(
                                url,
                                int(year),
                                int(month),
                                int(giorno.strftime('%d'))
                            )
                for giorno in giorni_new:
                    self._model.add_giorno_irreperibilita(
                        url,
                        int(year),
                        int(month),
                        int(giorno.strftime('%d'))
                    )
            return {'ok': 'Preferenza modificata correttamente'}, 200
        elif tipo == 'piattaforma':
            platform = msg.get('platform')
            if platform == "telegram":
                telegram = self._model.get_user_telegram_web(url)
                if not telegram:
                    return {'error': 'Telegram non presente nel sistema.'}, 404
            elif platform == "email":
                email = self._model.get_user_email_web(url)
                if not email:
                    return {'error': 'Email non presente nel sistema.'}, 404
            else:
                return {'error': 'La piattaforma deve essere telegram\
 o email.'}, 400
            self._model.update_user_preference(url, platform)
            return {'ok': 'Preferenza modificata correttamente'}, 200
