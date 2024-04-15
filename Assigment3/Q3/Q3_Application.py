import sqlite3
from Q3_Objects import Task

conn = sqlite3.connect('task_list_db.sqlite')
c = conn.cursor()

def view():
    c.execute('SELECT * FROM Task WHERE completed=0')
    completed = c.fetchall()
    if len(completed) == 0:
        print('No pending tasks')
        print()
    else:
        for i, task in enumerate(completed, start=1):

            print(f'{i}. {task[1]}')
        print()

def history():
    c.execute('SELECT * FROM Task WHERE completed=1')
    pending = c.fetchall()
    if len(pending) == 0:
        print('You have not completed any pending tasks')
        print()
    else:
        for i, task in enumerate(pending, start=1):
            print(f'{i}. {task[1]} (DONE!)')
        print()

def add():
    c.execute('select taskID from Task order by taskID desc;')
    task_list = c.fetchone()
    while True:
        description = input('Description: ')
        if len(description) == 0:
            print('Description cannot be empty')
        else:
            break
    new_task = Task(description)
    new_task.taskID = task_list[0] + 1
    c.execute('insert into Task values(?,?,?)', (new_task.taskID,new_task.description,new_task.status))
    conn.commit()
    print(f'{description} was added to task list')
    print()

def complete():
    c.execute('select taskID from Task where completed=0')
    task_list = c.fetchall()
    while True:
        try:
            del_task= int(input('Number: ')) - 1
            if del_task >= 0:
                task_index = task_list[del_task]
                taskID = task_index[0]
                break
            else:
                print(f'Task not on list')
        except ValueError:
            print('Please enter a number')
        except IndexError:
            print('Task does not exist')
        except Exception:
            print('Something went wrong')
    print()

    c.execute('update Task set completed = 1 where taskID=?', (taskID,))
    conn.commit()
    c.execute('select description from Task where taskID=?', (taskID,))
    description = c.fetchone()

    print(f"'{description[0]}' is completed")
    print()

def delete_completed():
    c.execute('select taskID from Task where completed=1')
    task_list = c.fetchall()
    if len(task_list) == 0:
        pass
    else:
        while True:
            try:
                del_task = int(input('Number: ')) - 1
                if del_task >= 0:
                    task_index = task_list[del_task]
                    taskID = task_index[0]
                    break
                else:
                    print(f'Task not on list')
            except ValueError:
                print('Please enter a number')
            except IndexError:
                print('Task does not exist')
            except Exception:
                print('Something went wrong')
        c.execute('delete from Task  where taskID=?', (taskID,))
        conn.commit()
        print('Task Deleted')
    print()


def delete_pending():
    c.execute('select taskID from Task where completed=0')
    task_list = c.fetchall()
    if len(task_list) == 0:
       pass
    else:
        while True:
            try:
                del_task = int(input('Number: ')) - 1
                if del_task >= 0:
                    task_index = task_list[del_task]
                    taskID = task_index[0]
                    break
                else:
                    print(f'Task not on list')

            except ValueError:
                print('Please enter a number')
            except IndexError:
                print('Task does not exist')
            except Exception:
                print('Something went wrong')
        c.execute('delete from Task where taskID=?', (taskID,))
        conn.commit()
        print('Task Deleted')
    print()


def delete():
    print('Options - ')
    print('c - Delete from Completed Task')
    print('p - Delete from Pending Task')
    print()
    while True:
        opt = input('Enter your option: ')
        if opt == 'c':
            history()
            print()
            delete_completed()

            break
        elif opt == 'p':
            view()
            print()
            delete_pending()

            break
        else:
            print('Invalid option')

# view()
# history()
# add()
# complete()
# delete()
