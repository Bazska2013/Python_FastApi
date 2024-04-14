import json


class EventFileManager:
    FILE_PATH = 'event.json'

    @staticmethod
    def read_events_from_file():
        with open(EventFileManager.FILE_PATH, 'r') as file:
            return json.loads(file.read())

    @staticmethod
    def write_events_to_file(events):
        with open(EventFileManager.FILE_PATH, 'w') as file:
            file.write(json.dumps(events))

