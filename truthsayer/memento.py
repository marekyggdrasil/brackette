from __future__ import annotations
from truthsayer.time import generateUTCTimestamp, tsToHuman
from abc import ABC, abstractmethod
from diff_match_patch import diff_match_patch


class Originator:
    def __init__(self):
        self._state = ''

    def apply_diff(self, diff):
        dmp = diff_match_patch()
        patches = dmp.patch_fromText(diff)
        self._state, _ = dmp.patch_apply(patches, self._state)

    def revert(self, memento: Memento) -> None:
        diff = memento.get_diff()
        self.apply_diff(diff)
        return self._state

    def export(self) -> Memento:
        return ConcreteMemento(self._state)

    def do_stuff(self, something):
        self._state = something


# https://refactoring.guru/design-patterns/memento/python/example
class Memento(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_date(self) -> str:
        pass


class ConcreteMemento(Memento):
    def __init__(self, diff: str) -> None:
        self._diff = diff
        self._date = generateUTCTimestamp()

    def get_diff(self) -> str:
        return self._diff

    def get_name(self) -> str:
        return f"{tsToHuman(self._date)} / ({self._diff[0:9]}...)"

    def get_date(self) -> str:
        return self._date


class Caretaker():
    def __init__(self, originator: Originator) -> None:
        self._mementos = []
        self._originator = originator
        self._state = originator._state

    def backup(self) -> None:
        print("\nCaretaker: Saving Originator's state...")
        original = self._state
        revision = self._originator._state
        diff = self.get_diff(revision, original)
        self._mementos.append(ConcreteMemento(diff))
        self._state = revision

    def get_diff(self, original, revision):
        dmp = diff_match_patch()
        patches = dmp.patch_make(original, revision)
        diff = dmp.patch_toText(patches)
        return diff

    def undo(self) -> None:
        if not len(self._mementos):
            return
        memento = self._mementos.pop()
        print(f"Caretaker: Restoring state to: {memento.get_name()}")
        self._state = self._originator.revert(memento)


    def show_history(self) -> None:
        print("Caretaker: Here's the list of mementos:")
        for memento in self._mementos:
            print(memento.get_name())
