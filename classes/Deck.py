import random

from .Card import Card

class Deck:
    _cards = []
    name = None

    def __init__(self, *args, **kwargs):
        self._cards = []
        for key in kwargs:
            if key == 'cards' and type(kwargs['cards']) == list:
                for card in kwargs[key]:
                    if type(card) == dict:
                        self._cards.append(Card(name = card['name'], description = card['description'], year = card['year'] ))
                    elif isinstance(card, Card):
                        self._cards.append(card)
                    else:
                        pass

            elif key == 'name':
                self.name = kwargs[key]
                
    def __str__(self):
        return ('%s(%i): ' % (self.name,len(self)) )+', '.join([str(card) for card in self._cards])

    def __len__(self):
        return len(self._cards)

    def getCards(self):
        return [card for card in self._cards]

    def getCard(self,i):
        return self._cards[i]

    def isSorted(self):
        if len(self) < 2:
            return True
        
        for i in range (1,len(self)):
            prevCard = self.getCard(i-1)
            currCard = self.getCard(i)
            if prevCard.year > currCard.year:
                return False
        
        return True

    def shuffle(self):
        random.shuffle(self._cards)
        return self

    def sort(self,reverse = False):
        self._cards.sort(reverse = reverse)
        return self

    def isEmpty(self):
        return len(self) == 0

    def take(self, num):
        
        if num > len(self):
            num = len(self)
        
        newDeck = Deck(cards = self._cards[:num])
        self._cards = self._cards[num:]
        return newDeck

    def takeCard(self, card = None):

        if self.isEmpty():
            return None
        elif card == None:
            return self.take(1)._cards[0]
        elif isinstance(card, Card) and (card in self._cards):
            self._cards.remove(card)
            return card
        else:
            return None

    def putCard(self,card,position = None):

        if position == None or position >= len(self):
            self._cards.append(card)
        else:
            self._cards.insert(max(0,position),card)
        
        return self
