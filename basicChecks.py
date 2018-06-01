from gravity import Gravity
from gravity.account import Account

grv = Gravity("wss://grvapi.graphenelab.org/ws")
acc = Account('g9480a2230f7280f3790')

print ('Getting Account: {}'.format(acc))