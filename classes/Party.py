import datetime
from .User import User
from .Deck import Deck


class Party:

    STATE_CREATED = 0
    STATE_STARTED = 1
    STATE_FINISHED = 2

    ERROR_OK = 0
    ERROR_UNKNOW = 1

    INITIAL_NUM_CARDS = 3

    name = "party"
    users = []
    dealer = None
    creation_date = datetime.datetime.now()
    state = STATE_CREATED
    
    mainDeck = Deck()
    tableDeck = Deck()
    discartDeck = Deck()
    userDecks = []


    def __init__(self, *args, **kwargs):
        for key in kwargs:
            if key == 'name':
                self.name = kwargs[key]
            elif key == 'deck':
                self.mainDeck = Deck(name='pool',cards = kwargs[key].getCards())

        self.userDecks = []
        self.tableDeck = Deck(name = 'table')
        self.discartDeck = Deck(name = 'discart')

    def __str__(self):
        return 'Party \'%s\', with %i users' % (self.name, len(self.users))

    def __len__(self):
        return len(self.users)

    def start(self):
        if self.state >= self.STATE_STARTED:
            return self.ERROR_UNKNOW
        elif len(self) < 2:
            return self.ERROR_UNKNOW
        else:
            self.state = self.STATE_STARTED
            self.dealer = 0
            # shuffle cards
            self.mainDeck.shuffle()
            for user in self.users:
                self.userDecks.append(self.mainDeck.take(self.INITIAL_NUM_CARDS))
            # put first card
            card = self.mainDeck.takeCard()
            self.tableDeck.putCard(card)
        
        return self
            

    def _checkIfUserExists(self, targetUser):
        for user in self.users:
            if user.name == targetUser.name:
                return True
        return False

    def join(self, user):
        if isinstance(user, User):
            if self._checkIfUserExists(user):
                return self.ERROR_UNKNOW
            else:
                self.users.append(user)
        elif type(user) == list:
            for u in user:
                error = self.join(u)
                if error != self.ERROR_OK:
                    return error
        else:
            return self.ERROR_UNKNOW

        return self.ERROR_OK

    def leave(self, user):
        if isinstance(user, User):
            if self._checkIfUserExists(user):
                self.users.remove(user)
            else:
                return self.ERROR_UNKNOW

        elif type(user) == list:
            
            for u in user:
                error = self.leave(u)
                if error != self.ERROR_OK:
                    return error
        else:
            return self.ERROR_UNKNOW

        return self.ERROR_OK


    def getStateDesc(self):
        if self.state == self.STATE_CREATED:
            return "Game created, just waiting to start"
        elif self.state == self.STATE_STARTED:
            return "Game started, playing"
        elif self.state == self.STATE_FINISHED:
            return "Game finished"
        else:
            return "Game state unknow"

    def getState(self):
        return self.state

    def getDealer(self):
        return self.users[self.dealer % len(self.users)]

    def getHand(self,user):
        index = self.users.index(user)

        if type(index) == int:
            return self.userDecks[index]
        else:
            return self.ERROR_UNKNOW


    def _setState(self,state):
        self.state = state
        return self

    def _updateState(self):
        
        if self.getState() == self.STATE_STARTED:
            for i in range(len(self.users)):
                if len(self.userDecks[i]) == 0:

                    return self._setState(self.STATE_FINISHED)
            
            if len(self.mainDeck) == 0:
                    return self._setState(self.STATE_FINISHED)


    def placeCard(self,card,position):
        
        if self.getState() == self.STATE_STARTED:
            dealer = self.getDealer()
            hand = self.getHand(dealer)
            tokenCard = hand.takeCard(card)
            
            if tokenCard == None:
                return self.ERROR_UNKNOW

            success = False
            if self.tableDeck.isEmpty():
                success = True
            elif position >= len(self.tableDeck):
                success = self.tableDeck.getCard(len(self.tableDeck)-1) <= card
            elif position == 0:
                success = card <= self.tableDeck.getCard(0)
            else:
                success = self.tableDeck.getCard(position -1) <= card and card <= self.tableDeck.getCard(position)

            self.dealer += 1
            if success:
                self.tableDeck.putCard(tokenCard,position)
            else:
                self.discartDeck.putCard(tokenCard)
                newTokenCard = self.mainDeck.takeCard()
                hand.putCard(newTokenCard)
            
            self._updateState()

            return success
            
        else:
            return self.ERROR_UNKNOW


















    def print(self):
        print ('Name:\t\'%s\'\tState:%s\t\n' % (self.name, self.getStateDesc()))
        if self.getState() == self.STATE_CREATED:
            for i in range(len(self.users)):
                user = self.users[i]
                print ('\t%i. %s' % (i,str(user)))

        elif self.getState() == self.STATE_STARTED:
            for i in range(len(self.users)):
                user = self.users[i]
                userDeck = self.userDecks[i]

                if self.getDealer() == user:
                    print('\t--> %i. %s\t%s' % (i, str(user),str(userDeck)))
                else:
                    print('\t    %i. %s\t%s' % (i, str(user), str(userDeck)))

            print('')
            print('\t%s' % str(self.tableDeck))
            #print('\t%s' % str(self.mainDeck))
            #print('\t%s' % str(self.discartDeck))
            print('')

