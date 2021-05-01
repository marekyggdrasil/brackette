import json

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from truthsayer import assets
from truthsayer.game import Game


class InvalidReserve(Exception):
    def __init__(self, reserve):
        self.reserve = reserve
        super().__init__('InvalidReserve')

    def __str__(self):
        return '{0} is not any players reserve.'.format(self.reserve)


class InvalidTerritory(Exception):
    def __str__(self):
        return 'Given territory is not an Arrakis territory.'


class InvalidUnit(Exception):
    def __str__(self):
        return 'Given unit is not a valid unit.'


class InvalidLeader(Exception):
    def __str__(self):
        return 'Invalid leader.'


class Dune(Game):
    def __init__(self, id, factions,
            game_state={'meta': {'players': []}, 'state': {'areas': {}, 'dials': {}, 'decks': {}}}):
        arrakis = pkg_resources.read_text(assets, 'arrakis.json')
        arrakis = json.loads(arrakis)
        self.arrakis = arrakis['territories']
        for territory in self.arrakis:
            game_state['state']['areas'][territory] = {'tokens': {}}
        for faction in factions:
            game_state['state']['areas'][faction] = {'tokens': {}}
        self.units = arrakis['units']
        super().__init__(id, game_state=game_state)

    # token commands
    def move(self, source, target, unit, number):
        self.isTerritory(source)
        self.isTerritory(target)
        self.isUnit(unit)
        self.moveToken(source, target, unit, number)

    def ship(self, source, target, unit, number):
        self.isReserve(source)
        self.isTerritory(target)
        self.isUnit(unit)
        self.moveToken(source, target, unit, number)

    def change(self, territory, unit, number):
        self.isTerritory(territory)
        self.isUnit(unit)
        if unit == 'spiritual_advisor':
            self.moveToken(territory, 'box', unit, number)
            self.moveToken('box', territory, 'bene_gesserit_troops', number)
        elif unit == 'bene_gesserit_troops':
            self.moveToken(territory, 'box', unit, number)
            self.moveToken('box', territory, 'spiritual_advisor', number)

    # payee is the one receiving
    def pay(self, spice, payor, payee):
        self.moveToken(payor, payee, 'spice', spice)

    def kill(self, leader):
        self.isLeader(leader)
        self.moveToken('battle', 'tleilaxu_tanks', leader, 1)

    def revive(self, leader, reserves):
        self.isLeader(leader)
        self.moveToken('tleilaxu_tanks', reserves, leader, 1)

    def nominate(self, leader, reserves):
        self.isLeader(leader)
        self.moveToken(reserves, 'battle', leader, 1)

    # card commands
    def battlePlan(self, card, source_area):
        self.isCard(card)
        self.isPlayer(player)
        self.moveCard(source_area, 'battle', card)

    def traitor(self, leader, player):
        self.isLeader(leader)
        self.moveCard(source_area, 'battle', leader)

    # validators
    def isReserve(self, reserve):
        if reserve not in self.reserves:
            raise InvalidReserve(reserve)

    def isTerritory(self, territory):
        if territory not in self.arrakis:
            raise InvalidTerritory

    def isUnit(self, unit):
        if unit not in self.units:
            raise InvalidUnit

    def isLeader(self, leader):
        if leader not in self.leaders:
            raise InvalidLeader
