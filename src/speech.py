import base64
import os
from contextlib import contextmanager, AbstractContextManager
from pathlib import Path
from uuid import uuid4

import discord
import requests

MY_GUILD = discord.Object(id=358780693595291652)


def text_to_speech(text: str) -> bytes:
    url = 'https://texttospeech.googleapis.com/v1beta1/text:synthesize'
    api_key = 'AIzaSyDvncFUJKqDLGaUX_701UVIqEH4znWjUKU'

    body = {
        'input': {
            'text': text
        },
        'voice': {
            'languageCode': 'ru-RU',
            'name': 'ru-RU-Standard-B',
            'ssmlGender': 'MALE'
        },
        'audioConfig': {
            'audioEncoding': 'MP3'
        }
    }

    args = [('key', api_key)]

    r = requests.post(url, json=body, params=args)
    content = base64.b64decode(r.json()['audioContent'])
    return content


def save(b: bytes) -> Path:
    path = Path(uuid4().hex)

    with open(path, 'wb') as stream:
        stream.write(b)

    return path


def delete(path: Path):
    os.remove(path)
