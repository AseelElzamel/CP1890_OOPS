import Q3_Application as app

def title():
    print('Task List')
    print()
def menu():
    print('COMMAND MENU')
    print('view - view pending tasks')
    print('history - view completed tasks')
    print('add - add a task')
    print('complete - complete a task')
    print('delete - delete a task')
    print('exit - exit program')
    print()

def main():
    title()
    menu()
    while True:
        cmd = input('Command: ').lower()
        if cmd == 'view':
            app.view()
        elif cmd == 'history':
            app.history()
        elif cmd == 'add':
            app.add()
        elif cmd == 'complete':
            app.complete()
        elif cmd == 'delete':
            app.delete()
        elif cmd == 'exit':
            app.conn.close()
            print()
            print('Bye!')
            break
        else:
            print('Command Not Found')

if __name__ == '__main__':
    main()