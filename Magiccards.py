import mariadb as sql
import os
from textual.app import App


## code adapted from Dr. Richard Stansbury's Deliverable 3 Example
##################################################################
# Helper Functions
def connectDB(host = 'localhost', user='root', password='', database='magicCards'):
    ''' Establishes a connection with the database and returns the cursor.'''
    db = sql.connect(host=host, user=user, password=password, database=database, autocommit=True)
    return db.cursor()

def printCards(tuples):
    ''' Prints the results of a query on the magicCards with all attributes.'''
    tableStyle = '\t|{:25} | {:4} | {:10} | {:15} | {:16} |'
    print()
    print(tableStyle.format("Card Name","Year","Mana Type","Card Type", "Card Cost (USD)"));
    for t in tuples:
        print(tableStyle.format(*t));
    print()

def printDecks(tuples):
    ''' Prints the results of a query on the magicCards with all attributes.'''
    tableStyle = '\t|{:25} | {:7} | {:10} | {:4} |'
    print(tableStyle.format("Deck Name","Format ID","Mana Type","Deck code"));
    for t in tuples:
        print(tableStyle.format(*t));
    print()


##################################################################
# Main Menu
def main():
    ''' Implements the main loop for the user interface'''
    cursor = connectDB()   
    print("My Magic Card Database\n")
    
    # Present user with the main menu and then perform the
    # desired action based on their choice.
    while ((choice := menuMain()) != 0):
        if choice == 1: # Print all game info
            queryAllCards(cursor)            
        elif choice == 2:
            gameInfoSearch(cursor)
        elif choice ==3:
            queryAllDecks(cursor)
        elif choice ==4:
                addCard(cursor)
        elif choice == 5:
                addDeck(cursor)
        elif choice ==6:
                deleteCard(cursor)
        elif choice == 7:
                searchDeck(cursor)

    
    
def menuMain():
    ''' Prints the main menu to the command line, 
        parses the choice, and returns the result.'''
    try:
        print("\tWhat do you want to do?")
        print("\t(1) Show All Cards")
        print("\t(2) Search for cards")
        print("\t(3) Print all deck info")
        print("\t(4) Add card")
        print("\t(5) Create Deck")
        print("\t(6) Delete Card ")
        print("\t(7) View Cards In Deck")
        print("\t(0) Quit\n")
        return int(input("\t> "))
    except:
        choice = -1; #invalid choice
    
    #recurse until the user provides a valid input.
    if choice < 0 or choice > 7:
        print("\t\tInvalid choice...try again.\n")
        return menuMain() 

        
#################################################################       
#  Option 1: All Card Info  // All Deck info

def queryAllCards(cursor):
    ''' Queries the Videogames relation and prints the resulting table.'''
    query = "SELECT * FROM MagicCards";
    cursor.execute(query)
    results = cursor.fetchall()
    
    if cursor.rowcount > 0:
        printCards(results)
    else:
        print("\n\t\tNo info matching: {}\n".format(query))

def queryAllDecks(cursor):
    ''' Queries the Decks relation and prints the resulting table.'''
    query = "SELECT * FROM Decks";
    cursor.execute(query)
    results = cursor.fetchall()
    
    if cursor.rowcount > 0:
        printDecks(results)
    else:
        print("\n\t\tNo info matching: {}\n".format(query))


#################################################################       
#  Option 2: Search Cards by Attributes

def gameInfoSearch(cursor):
    ''' Provides the user with a menu to select their query type and
        given their choice calls the appropriate function'''
    choice = menuGameSearch()
    
    if choice == 0:
        print("Returning to main menu.")
        return
    elif choice == 1:
        queryCardName(cursor)
    elif choice == 2:
        queryCardsYear(cursor)
    elif choice == 3:
        queryCardsMana(cursor)
    elif choice == 4:
        queryCardType(cursor)
#################################################################       
#  Option3: Add a new card / deck




def menuGameSearch():
    ''' Prints a sub-menu for Card Search.  User input is parsed
        and validated'''
    try:
        print("\tSearch Card Info\n")
        print("\tWhich attribute do you want to search by?")
        print("\t(1) Card Name")
        print("\t(2) Release year")
        print("\t(3) Mana Type")
        print("\t(4) Card Type")
        return int(input("\n\t> "))
    except:
        choice = -1;
      
    if choice < 0 or choice > 7:
        print("\t\tInvalid choice...try again.\n")
        return menuMain()




def queryCardName(cursor):
    ''' Prompts the user for a game title to search and
        prints a table with each row being a tuple from the
        query results.'''
    CardName = input("\n\t Card Name? >  ");
    
    query = "SELECT * FROM MagicCards where CardName=?"
    cursor.execute(query,(CardName,))
    results = cursor.fetchall()
    
    if cursor.rowcount > 0:
        printCards(results)
    else:
        print("\n\t\tYou do not have any {} cards in your collection\n".format(CardName))


def queryCardsYear(cursor):
    ''' Prompts the user for a release year to search and
        prints a table with each row being a tuple from the
        query results.'''
    releaseYear = int(input("\n\t Year of Release? >  "));
    
    query = "SELECT * FROM MagicCards where releaseYear=?"
    cursor.execute(query,(releaseYear,))
    results = cursor.fetchall()
    
    if cursor.rowcount > 0:
        printCards(results)

    else:
         print("\n\t\tYou do not have cards from {} in your collection\n".format(releaseYear))
 
def queryCardsMana(cursor):
   
    mana = input("\n\t Mana Type? >  ");
    
    query = "SELECT * FROM MagicCards where manaType=?"
    cursor.execute(query,(mana,))
    results = cursor.fetchall()
    
    if cursor.rowcount > 0:
        printCards(results)

    else:
         print("\n\t\tYou do not have any {} cards in your collection\n".format(mana))
        
def queryCardType(cursor):
 
    cardType = input("\n\t Card Type? >  ");
    
    query = ('SELECT * FROM MagicCards where cardType=?')
    cursor.execute(query,(cardType,))
    results = cursor.fetchall()
    
    if cursor.rowcount > 0:
        printCards(results)

    else:
         print("\n\t\tYou do not have any {} cards in your collection\n".format(cardType))

def addCard(cursor):
    query = "INSERT INTO MagicCards (CardName, releaseYear, manaType, cardType, cardCost) VALUES (%s,%d, %s,%s,%d)"

    CardName = input("\n\t Card Name? >  ");
    releaseYear = input("\n\t Year? >  ");
    manaType = input("\n\t Mana Type? >  ");
    cardType = input("\n\t Card Type? >")
    cardCost = input("\n\t Card Cost? >  ");

    cursor.execute(query, (CardName,releaseYear,manaType,cardType,cardCost))
    print("{} Has Been Added to the list of cards!".format(CardName))


def addDeck(cursor):
    query = "INSERT INTO Decks(deckName, FormatID, castType, deckCode) VALUES (%s,%s, %s, ,%d)"

    CardName = input("\n\t Deck Name? >  ");
    format = input("\n\t What format will it be in? >  ");
    mana = input("\n\t cast Type? >  ");
    code = input("\n\t create a deck code for your deck ? >  ");

    cursor.execute(query, (CardName,format,mana,code))

def searchDeck(cursor):
 
    deck = input("\n\t Deck Code? >  ");
    query = "SELECT * FROM Collection where deckCode=?"
    cursor.execute(query,(deck,))
    results = cursor.fetchall()
    
    if cursor.rowcount > 0:
        printDecks(results)
    else:
        print("\n\t\tYou do not have any {} cards in your collection\n".format(deck))

def deleteCard(cursor):
    CardName = input("\n\t What is the name of your card you would like to delete? >  ");
    query = "DELETE FROM MagicCards WHERE CardName =?"
    cursor.execute(query,(CardName,))
    print("{} Has Been Removed from the list of cards!".format(CardName))



    ####################################
if __name__ == "__main__":
    os.system('cls')
    main()
        
            