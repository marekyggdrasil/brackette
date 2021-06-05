# truthsayer

```python
from mementeur.memento import Originator, Caretaker

originator = Originator()
caretaker = Caretaker(originator)

originator.do_stuff('hello')
print(originator._state)
print(originator._hash)
caretaker.backup()

originator.do_stuff('meoreo')
print(originator._state)
print(originator._hash)
caretaker.backup()

originator.do_stuff('kinda')
print(originator._state)
print(originator._hash)
caretaker.backup()

caretaker.undo()
print(originator._state)
print(originator._hash)

caretaker.undo()
print(originator._state)
print(originator._hash)

caretaker.redo()
print(originator._state)
print(originator._hash)

caretaker.undo()
print(originator._state)
print(originator._hash)

caretaker.show_history()
```

outputs

```
hello
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
meoreo
bbba0753c25637757dd58e943bf8089f66aa5a408cc1764458230e3112ab41e1
kinda
29f0e99be96b1bf5bfb5902b10171f4b7d8135fe205fc8c94b81754c0d661513
meoreo
bbba0753c25637757dd58e943bf8089f66aa5a408cc1764458230e3112ab41e1
hello
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
meoreo
bbba0753c25637757dd58e943bf8089f66aa5a408cc1764458230e3112ab41e1
hello
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
Caretaker: Here's the list of past mementos:
2021-04-27 14:25:43 UTC 6411ee087bfe7ce14043d451748b5199ef7ccaa42aa6e0f8ab2c63de94281c7d
Caretaker: Here's the list of future mementos:
2021-04-27 14:25:43 UTC 2783de246149f2cfec85bf718a938ddcb0c1bdad249afc56f53882c6de3f8475
2021-04-27 14:25:43 UTC 0a14b4c21ac263fe47312f688975fc1022feb531db396dca9eb9ed0571f862ee
```
