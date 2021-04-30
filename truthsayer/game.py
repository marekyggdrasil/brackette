from __future__ import annotations
import json

from truthsayer.memento import Originator


class InvalidArea(Exception):
    def __init__(self, id, hash, area):
        self._id = id
        self._hash = hash
        self._area = area
        super().__init__('InvalidArea')

    def __str__(self):
        return '{0} {1} invalid game area {2}'.format(self._id, self._hash, self._area)


class InsufficientResources(Exception):
    def __init__(self, id, hash, token, area):
        self._id = id
        self._hash = hash
        self._token = token
        self._area = area
        super().__init__('InsufficientResources')

    def __str__(self):
        return '{0} {1} there is no sufficient amount of {2} in area {3}'.format(self._id, self._hash, self._token, self._area)


class CardNotPresent(Exception):
    def __init__(self, id, hash, card, area):
        self._id = id
        self._hash = hash
        self._card = card
        self._area = area
        super().__init__('CardNotPresent')

    def __str__(self):
        return '{0} {1} the card {2} is not present in the area {3}'.format(self._id, self._hash, self._card, self._area)


class EmptyDeck(Exception):
    def __init__(self, id, hash, deck_name):
        self._id = id
        self._hash = hash
        self._deck_name = deck_name
        super().__init__('EmptyDeck')

    def __str__(self):
        return '{0} {1} the deck {2} is empty'.format(self._id, self._hash, self._deck_name, self._area)


class InvalidPlayer(Exception):
    def __init__(self, id, hash, player_name):
        self._id = id
        self._hash = hash
        self._player_name = player_name
        super().__init__('InvalidPlayer')

    def __str__(self):
        return '{0} {1} no such player {2}'.format(self._id, self._hash, self._player_name)


class Game(Originator):
    def __init__(self, id,
            game_state={'meta': {'players': []}, 'state': {'areas': {}, 'dials': {}, 'decks': {}}}):
        super().__init__()
        self._id = id
        self._game_state = game_state
        self._state = self.backup()

    def backup(self):
        self._state = json.dumps(self._game_state)
        return super().backup()

    def moveToken(self, source_area, target_area, token, number):
        self.moveAsset('tokens', source_area, target_area, token)

    def moveCard(self, source_area, target_area, card):
        self.moveAsset('cards', source_area, target_area, card)

    def moveAsset(self, asset_type, source_area, target_area, asset):
        self.validateArea(source_area, asset_type)
        self.validateArea(target_area, asset_type)
        self.validateAsset(source_area, asset_type, asset, number=number)
        self._game_state['state']['areas'][source_area][asset_type][asset] -= number
        if asset not in self._game_state['state']['areas'][target_area][asset_type].keys():
            self._game_state['state']['areas'][target_area][asset_type][asset] = 0
        self._game_state['state']['areas'][target_area][asset_type][asset] += number

    def discardCard(self, source_area, target_deck, card):
        self.validateArea(source_area, 'cards')
        self.validateAsset(source_area, 'cards', card, number=1)
        self._game_state['state']['areas'][source_area]['cards'][card] -= 1
        self._game_state['state']['decks'][target_deck].append(card)

    def drawCard(self, source_deck, target_area):
        self.validateArea(target_area, 'cards')
        if len(self._game_state['state']['decks'][source_deck]) == 0:
            raise EmptyDeck(self._id, self._hash, source_deck)
        card = self._game_state['state']['decks'][source_deck].pop()
        if card not in self._game_state['state']['areas'][target_area]['cards'].keys():
            self._game_state['state']['areas'][target_area]['cards'][card] = 0
        self._game_state['state']['areas'][target_area]['cards'][card] += 1

    def dial(self, number, player_name):
        self.validatePlayer(player_name)
        self._game_state['state']['dials'][player_name] = number

    def bid(self, number, player_name):
        self.validatePlayer(player_name)
        self._game_state['state']['bids'][player_name] = number

    # data validators
    def validateArea(self, area_name, asset_type):
        if area_name not in self._game_state['state']['areas'].keys():
            raise InvalidArea(self._id, self._hash, area_name)

    def validateAsset(self, area_name, asset_type, asset, number=None):
        if asset not in self._game_state['state']['areas'][area_name][asset_type].keys():
            raise InsufficientResources(self._id, self._hash, asset, source_area)
        if number is None:
            return
        if self._game_state['state']['areas'][area_name][asset_type][asset] < number:
            raise InsufficientResources(self._id, self._hash, asset, area_name)

    def validatePlayer(self, player_name):
        if player_name not in self._game_state['meta']['players'].keys():
            raise InvalidPlayer(self._id, self._hash, player_name)
