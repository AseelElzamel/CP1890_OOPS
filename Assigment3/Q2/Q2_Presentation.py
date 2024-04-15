import Q2_Application as app


def title():
    print('Player Manager')
    print()


def menu():
    print('COMMAND MENU')
    print()
    print('view - View Players')
    print('add - Add a Player')
    print('delete - Delete a Player')
    print('update - Update a Player')
    print('exit - Exit Program')
    print()


def main():
    title()
    menu()
    while True:
        cmd = input('Command: ').lower()
        print()
        if cmd == 'view':
            app.view_players()
        elif cmd == 'add':
            app.add_player()
        elif cmd == 'delete':
            app.del_player()
        elif cmd == 'update':
            app.update_player()
        elif cmd == 'exit':
            app.conn.close()
            break
        else:
            print('Command not found')


if __name__ == '__main__':
    main()
