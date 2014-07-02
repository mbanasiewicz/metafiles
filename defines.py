__author__ = 'maciejbanasiewicz'

import polish

database_name = "metafiles.sqlite"
project_root = '/Users/maciejbanasiewicz/PycharmProjects/metafiles/'
supported_mime_types = [
    'text/plain', #txt
    'audio/x-wav', #wav
    'audio/mpeg', #mp3
    'image/jpeg',
    'application/msword' #msword
]

def stopWordsForLanguage():
    return polish.polish_stop