import sqlite3
from Q2_Objects import Player

conn = sqlite3.connect('player_db.sqlite')
c = conn.cursor()


def view_players():
    c.execute('select * from Player ORDER BY Wins DESC;')
    players = c.fetchall()

    PLAYERS = []
    for player in players:
        PLAYERS.append(Player(player[1], player[2], player[3], player[4]))

    print(f"{'Name':20} {'Wins':>6} {'Losses':>6} {'Ties':>6} {'Games':>6}")
    print('-' * 50)
    for player in PLAYERS:
        print(
            "{:<20} {:>6} {:>6} {:>6} {:>6}".format(player.name, player.wins, player.losses, player.ties, player.games))
    print()


def add_player():
    c.execute('select name from Player ;')
    players_names = c.fetchall()
    names = []
    for player in players_names:
        names.append(player[0])
    playerID = len(names) + 1
    while True:
        try:
            name = input('Name:')
            if name not in names:
                break
            else:
                print('Name already taken')
        except ValueError:
            print('Name must be entered')
    while True:
        try:
            wins = int(input('Wins: '))
            losses = int(input('Losses: '))
            ties = int(input('Ties: '))
            if wins >= 0 and losses >= 0 and ties >= 0:
                break
            else:
                print('Value cannot be negative')
        except ValueError:
            print('Input must be an integer')
        except Exception:
            print('Something went wrong')
    c.execute('insert into Player values (?,?,?,?,?)', (playerID, name, wins, losses, ties))
    conn.commit()
    print('{} was added to database.'.format(name))
    print()


def del_player():
    c.execute('select name from Player ;')
    players_names = c.fetchall()
    names = []
    for player in players_names:
        names.append(player[0])
    while True:
        name = input('Name: ').title()
        if name not in names:
            print('Player does not exist')
        else:
            c.execute('delete from Player WHERE Name=?', (name,))
            conn.commit()
            print('{} was deleted from database.'.format(name))

            break
    print()


def update_player():
    c.execute('select name from Player ;')
    players_names = c.fetchall()
    names = []
    for player in players_names:
        names.append(player[0])
    while True:
        name = input('Name: ').title()
        if name not in names:
            print('Player does not exist')
        else:
            while True:
                try:
                    wins = int(input('Wins: '))
                    losses = int(input('Losses: '))
                    ties = int(input('Ties: '))
                    if wins >= 0 and losses >= 0 and ties >= 0:
                        break
                    else:
                        print('Value cannot be negative')
                except ValueError:
                    print('Input must be an integer')
                except Exception:
                    print('Something went wrong')
            query = 'update Player set wins=?,losses=?,ties=? where Name=?'
            c.execute(query, (wins, losses, ties, name))
            conn.commit()
            print("{};s was updated from database.".format(name))
            break
    print()

    # print(names)
# players = connect_db()
# add_player()
# view_players()
#
# del_player()
# view_players()

# update_player()
# view_players()
