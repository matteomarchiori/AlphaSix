"""
File: GLProducer.py
Data creazione: 2019-02-18

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

# Posizione: Butterfly/
# Uso: python3 -m path.to.GLProducer

import argparse
from sys import stderr
from kafka import KafkaProducer
import kafka.errors
import json
from pathlib import Path
from producer.producer import Producer
#from webhook.gitlab.GLIssueWebhook import GLIssueWebhook
from redminelib import Redmine

class RedmineProducer(Producer):

    def __init__(self, config): # COSTRUTTORE
        self._producer = KafkaProducer(
            # Serializza l'oggetto Python in un oggetto JSON, codifica UTF-8
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
            **config
        )

    def __del__(self): # DISTRUTTORE
        self.close()

    @property
    def producer(self):
        """Restituisce il KafkaProducer"""
        return self._producer



def main():

    # Configurazione da config.json
    with open(Path(__file__).parents[1] / 'config.json') as f:
        config = json.load(f)

    """Fetch dei topic dal file topics.json
    Campi:
    - topics['id']
    - topics['label']
    - topics['project']
    """
    with open(Path(__file__).parents[2] / 'topics.json') as f:
        topics = json.load(f)

    # Istanzia il Producer
    producer = RedmineProducer(config)

        # Parsing dei parametri da linea di comando
    parser = argparse.ArgumentParser(description='Crea messaggi su Kafka')
    parser.add_argument('-t', '--topic', type=str,
                        help='topic di destinazione')
    args = parser.parse_args()





if __name__ == '__main__':
    main()