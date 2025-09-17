from tinydb import TinyDB
from paginas.tinydbservice.tinydbservice import TinyDbService
from paginas.events.events import Event

"""Controller for managing events"""
EventController = TinyDbService[Event](TinyDB("eventdb.json"), Event)
