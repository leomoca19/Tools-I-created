from datetime import datetime


def welcome():
    print('Welcome to a to-do list manager by Leonardo')


def goodbye():
    print('Goodbye!')


def print_(*string):
    """
    prints without a newline
    """
    print(*string, end='')


def prompt(question, answers=None):
    """
    displays the question, then prompts the user to input an answer and validates the input

    :param question: string to be displayed to ask for input
    :param answers: a list of the possible accepted answers, accepts any answer if None
    :return: the validated answer
    """

    full_str = question

    # add possible answers
    if answers:
        full_str += ' ' + '|'.join(answers)

    # character to show the user should input
    full_str += ': '

    # validate answer
    while True:
        print_(full_str)

        if not answers:
            return input()

        if (answer := input()) in answers:
            return answer

        print('Bad input')


def get_id(string):
    """
    prompts string and accepts only integers
    """

    while True:
        answer = input(string)
        if answer.isdigit():
            return int(answer)
        else:
            print('Bad input')


class TaskManager:
    class Task:
        def __init__(self,
                     id,
                     description,
                     status='pending',
                     date=datetime.now().date().strftime("%b-%d-%Y")):
            self.id = id
            self.description = description
            self.date = date
            self.status = status

        def __str__(self):
            return f'ID: {self.id} - {self.description}\n{self.date} - {self.status}\n'

    def __init__(self, id_counter=1):
        self.id_counter = id_counter
        self.tasks = []

    def __len__(self):
        return len(self.tasks)

    def find_by_id(self, id):
        """
        :param id: the task id
        :return: index of the task with the given id
        """

        for i, task in enumerate(self.tasks):
            if task.id > id:
                return None

            if task.id == id:
                return i

    def add_sample_task(self, x):
        """
        adds x sample tasks
        """

        s = self
        for i in range(x):
            s.tasks.append(s.Task(s.id_counter, 'sample'))
            s.id_counter += 1

    def view_tasks(self, status=None):
        """
        Display all current tasks with an option to view completed and pending tasks separately.
        """

        if n := len(ts := self.tasks):
            if status == 'next':
                # find first pending task
                i = 0
                while ts[i].status != 'pending':
                    i += 1

                if i < n:
                    print(f'Next Task:\n{ts[i]}')
                else:
                    print('No pending Tasks')
            else:
                # create a list of desired tasks to print
                print(*[t for t in ts if not status or t.status == status],
                      sep='\n')
        else:
            print('No tasks')

    def add_task(self, description):
        """
        Adds a new tasks to the to-do list by prompting or argument
        """
        self.tasks.append(self.Task(self.id_counter, description))
        self.id_counter += 1

    def update_task(self, id):
        """
        Allow the user to mark tasks as complete and edit the task details
        :return: the updated task
        """

        i = self.find_by_id(id)
        if i is not None:
            task = self.tasks[i]
            print(f'Task selected: {task}')

            answer = prompt('Mark as completed?', ['y', 'n'])
            if answer == 'y':
                task.status = 'completed'

            answer = prompt('Update description?', ['y', 'n'])
            if answer == 'y':
                task.status = input('Enter new description:')

            return task

        else:
            print('Task not found')

    def remove_task(self, id):
        """
        Deletes a task from the list by id
        :return: the deleted task
        """

        i = self.find_by_id(id)
        if i is not None:
            tmp = self.tasks[i]
            del self.tasks[i]
            return tmp
        else:
            print('Task ID not found')

    def save_to_file(self, file_name):
        """
        Saves tasks in a file
        """

        with open(file_name, 'w') as file:
            for task in self.tasks:
                file.write(str(task))
            file.write('last id: ' + str(self.id_counter) + '\n')

    def load_from_file(self, file_name):
        """
        Loads tasks from a file
        """

        with open(file_name, 'r') as file:

            while line := file.readline():

                # if this is the last line of the file, stop reading
                if line[:9] == 'last id: ':
                    self.id_counter = int(line[9:])
                    break

                skip_str = 4  # discard 'ID: '
                empty_pos = line.find(' ', skip_str)

                id = int(line[skip_str:empty_pos])  # read ID
                description = line[empty_pos + 3:-1]  # discard ' - ', '\n' and read description

                line = file.readline()
                empty_pos = line.find(' ')

                date = line[:empty_pos]  # read date
                status = line[empty_pos + 3:-1]  # discard ' - ' and '\n' and read status

                new_task = self.Task(id, description, status, date)
                self.tasks.append(new_task)


def run(io_file='tasks.txt'):
    """
    run the application

    :param io_file: name of the file to read from and write to
    """

    tm = TaskManager()

    tm.load_from_file(io_file)
    welcome()

    header = ('Exit 0 | View Tasks 1 | Add Task 2 | Update Task 3 | Delete Task 4\n'
              'Select an option')
    good_ans = ['0', '1', '2', '3', '4']

    while answer := prompt(f'Tasks in system: {len(tm)}\n' + header, good_ans):
        match answer:
            case '0':
                _header = 'Are you sure you want to save and exit'
                _good_ans = ['y', 'n']

                if prompt(_header, _good_ans) == 'y':
                    break

            case '1':
                _header = ('All 0 | Pending 1 | Completed 2 | Next Task 3\n'
                           'Select an option')
                _good_ans = ['0', '1', '2', '3']

                # transform int input to task status
                match answer := int(prompt(_header, _good_ans)):
                    case 0:
                        answer = None
                    case 1:
                        answer = 'pending'
                    case 2:
                        answer = 'completed'
                    case 3:
                        answer = 'next'

                tm.view_tasks(answer)

            case '2':
                tm.add_task(prompt('Enter a description of your new task'))
                print(f'Task added:{tm.tasks[-1]}')

            case '3':
                id = get_id('Select a Task ID: ')
                print(f'Updated task:\n{tm.update_task(id)}')

            case '4':
                id = get_id('Select a Task ID: ')
                print(f'Deleted task:\n{tm.remove_task(id)}')

    goodbye()
    tm.save_to_file('tasks.txt')


if __name__ == '__main__':
    run()
