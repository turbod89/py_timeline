import datetime
import pprint
import random
import json
import os


from classes.User import User
from classes.Party import Party
from classes.Card import Card
from classes.Deck import Deck

def mock_createUsers():
    with open('./mockData/users.json') as json_data:
        data = json.load(json_data)
        return [ User (name = u['name'], firstName = u['firstName'], lastName = u['lastName']) for u in data]

def mock_createDeck():
    decks = None
    with open('./mockData/decks.json') as json_data:
        data = json.load(json_data)
        decks = [Deck(name=u['name'], cards = u['cards']) for u in data]

    return decks



def mock_createParties(users, deck):

    parties = [
        Party(name="first party", deck = deck),
    ]

    for p in parties:
        sample_users = [users[i] for i in sorted(random.sample(range(len(users)), random.randint(2,len(users))))]
        p.join(sample_users)

    return parties


def main():
    users = mock_createUsers()
    decks = mock_createDeck()
    parties = mock_createParties(users,decks[0])
    
    party = parties[0]
    party.start().print()

    while party.getState() < 2:
        user = party.getDealer()
        hand = party.getHand(user)

        position = random.randint(0,len(party.tableDeck))
        card = hand.getCard(random.randint(0,len(hand)-1))

        print ('User %s puts card %s in position %i' % (str(user),str(card),position))
        success = party.placeCard(card,position)
        print (str(success))
        party.print()

if __name__ == '__main__':
    main()
