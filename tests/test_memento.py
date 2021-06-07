import unittest

from brackette.memento import Originator, Caretaker


class FlaskTest(unittest.TestCase):
    def test_everything(self):
        originator = Originator()
        caretaker = Caretaker(originator)
        originator.do_stuff('hello')
        assert originator._state == 'hello'
        caretaker.backup()
        originator.do_stuff('meoreo')
        assert originator._state == 'meoreo'
        caretaker.backup()
        caretaker.undo()
        assert originator._state == 'hello'
        caretaker.redo()
        assert originator._state == 'meoreo'
        originator.do_stuff('kinda')
        assert originator._state == 'kinda'
        caretaker.backup()
        caretaker.undo()
        caretaker.undo()
        assert originator._state == 'hello'
        caretaker.redo()
        assert originator._state == 'meoreo'
        caretaker.redo()
        assert originator._state == 'kinda'
