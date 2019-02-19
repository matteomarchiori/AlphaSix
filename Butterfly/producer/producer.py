"""
File: Producer.py
Data creazione: 2019-02-12

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
Creatore: Timoty Granziero, timoty.granziero@gmail.com
Autori:
    <nome cognome, email>
    <nome cognome: email>
    ....
"""


from abc import ABC, abstractmethod

class Producer(ABC):
    """Interfaccia Producer"""

    @abstractmethod
    def produce(self, topic, msg):
        """Produce il messaggio `msg` nel Topic designato del Broker"""
        pass


# class ConsoleProducer(Producer):
#     def __init__(self, config):
#         self._producer = KafkaProducer(**config)

#     def __del__(self):
#         self.close()

#     @property
#     def producer(self):
#         """Restituisce il KafkaProducer"""
#         return self._producer

#     def produce(self, topic: str, msg: str):
#         """Produce il messaggio in Kafka"""
#         try:
#             # Produce il messaggio sul Broker, codificando la
#             # stringa in binario
#             self.producer.send(topic, msg.encode())
#             self.producer.flush(10) # Attende 10 secondi
#         except kafka.errors.KafkaTimeoutError:
#             stderr.write('Errore di timeout\n')
#             exit(-1)

#     def close(self):
#         """Rilascia il Producer associato"""
#         self._producer.close()


# class WebhookProducer(Producer):
#     def __init__(self, config):
#         self._producer = KafkaProducer(
#             # Serializza l'oggetto Python in un oggetto JSON, codifica UTF-8
#             value_serializer=lambda m: json.dumps(m).encode('utf-8'),
#             **config
#         )

#     def __del__(self):
#         self.close()


#     @property
#     def producer(self):
#         """Restituisce il KafkaProducer"""
#         return self._producer


#     def produce(self, topic, msg: GLIssueWebhook):
#         """Produce il messaggio in Kafka.
#         Precondizione: msg è di tipo GLIssueWebhook

#         Arguments:
#         topic -- il topic dove salvare il messaggio.
#         """

#         assert isinstance(msg, GLIssueWebhook), \
#                 'msg non è di tipo GLIssueWebhook'

#         # Parse del JSON associato al webhook ottenendo un oggetto Python 
#         msg.parse()
#         try:
#             print()
#             # Inserisce il messaggio in Kafka, serializzato in formato JSON
#             self.producer.send(topic, msg.webhook())
#             self.producer.flush(10) # Attesa 10 secondi
#         except kafka.errors.KafkaTimeoutError:
#             stderr.write('Errore di timeout\n')
#             exit(-1)

#     def close(self):
#         """Rilascia il Producer associato"""
#         self._producer.close()

# # Funzione ausiliaria per ConsoleProducer
# def produce_messages(console_producer, topic, args):
#     """Genera i messaggi degli argomenti passati a linea di comando"""
#     for msg in args.message:
#         console_producer.produce(topic, msg)


# def main():

#     # Configurazione da config.json
#     with open(Path(__file__).parent / 'config.json') as f:
#         config = json.load(f)
#     config = config['producer']

#     """Fetch dei topic dal file topics.json
#     Campi:
#     - topics['id']
#     - topics['label']
#     - topics['project']
#     """
#     with open(Path(__file__).parent / 'topics.json') as f:
#         topics = json.load(f)

#     # Istanzia il Producer
#     # producer = ConsoleProducer(config)
#     producer = WebhookProducer(config)

#     # Parsing dei parametri da linea di comando
#     parser = argparse.ArgumentParser(description='Crea messaggi su Kafka')
#     parser.add_argument('-t', '--topic', type=str,
#                         help='topic di destinazione')
#     # parser.add_argument('message', type=str, nargs='+',
#     #                     help='crea messaggi su Kafka')
#     args = parser.parse_args()

#     # Produce i messaggi nel topic passato come argomento
#     # if args.topic:
#     #     produce_messages(ConsoleProducer, args.topic, args)
#     # else:
#     #     produce_messages(ConsoleProducer, topics[0]['label'])


#     # Inizializza il GLIssueWebhook con il path a webhook.json
#     webhook = GLIssueWebhook(Path(__file__).parent / 'webhook.json')
#     if args.topic:
#         producer.produce(args.topic, webhook)
#     else:
#         producer.produce(topics[0]['label'], webhook)


# if __name__ == '__main__':
#     main()