from abc import ABC, abstractmethod

from mongo_db.facade import MongoFacade


class Processor():

    def __init__(self, message: dict, mongofacade: MongoFacade):  # aggiungere riferimento DB
        self.__message = message
        self.__mongofacade = mongofacade

    # Metodo che chiama a ruota tutti quelli dopo per processare il messaggio
    def prepare_message(self) -> dict:
        progetto = self.check_project()  # URL progetto
        obj = self.__message['object_kind']  # Issue o push ecc
        # Lista di tutti gli utenti disponibili oggi nel progetto
        utenti_disponibili = self.get_involved_users()
        # Lista di tutti gli utenti interessati e disponibili
        utenti_interessati = self.filter_users_by_topic(
            utenti_disponibili, obj
        )
        # Se non c'è nessuno, vedo la persona di priorità
        # più alta disponibile oggi per quel progetto
        if utenti_interessati == []:
            utenti_interessati = self.select_users_more_interested(
                progetto
            )
        self.__list_telegram = self.get_telegram_contacts(utenti_interessati)
        self.__list_email = self.get_email_contacts(utenti_interessati)
        final_map = {}
        final_map['app_receiver'] = {}
        final_map['app_receiver']['telegram'] = self.__list_telegram
        final_map['app_receiver']['email'] = self.__list_email

    # Controlla se c'è il progetto nel DB, se non c'è lo aggiunge
    def _check_project(self) -> str:
        urlProgetto = self._message['project_url']
        # Vediamo nel DB se il prog c'è
        exists_project = self.__mongofacade.get_project_by_url(urlProgetto)
        # Se non c'è lo aggiungiamo
        if not exists_project:
            self.__mongofacade.insert_project(urlProgetto)
        return urlProgetto

    # Lista di tutti gli utenti relativi al prog disponibili oggi
    def _get_involved_users(self, project: str) -> list:
        return self.__mogofacade.get_users_available(project)

    @abstractmethod
    def _filter_users_by_topic(self, users: list, obj: str) -> list:
        pass

    # Lista di tutti gli utenti disponibili e più interessati
    def _select_users_more_interested(self, project: str) -> list:
        return self.__mongofacade.get_users_max_priority(project)

    # Crea la lista di contatti telegram a cui inviare il messaggio
    def _get_telegram_contacts(self, users: list) -> list:
        contacts = []
        for user in users:
            telegramID = self.__mongofacade.get_user_telegram(user)
            if telegramID is not None:
                contacts.append(telegramID)
        return contacts

    # Crea la lista di contatti mail a cui inviare il messaggio
    def _get_email_contacts(self, users: list) -> list:
        contacts = []
        for user in users:
            emailID = self.__mongofacade.get_user_email(user)
            if emailID is not None:
                contacts.append(emailID)
        return contacts

    # Metodo pubblico per prendere la lista di contatti mail
    # def get_email_list(self) -> list:
    #     return self.__list_email

    # # Metodo pubblico per prendere la lista di contatti telegram
    # def get_telegram_list(self) -> list:
    #     return self.__list_telegram
