import re

from prediction import regression, multivariate_regression, most_profitable_laptop


def start_main_loop():
    print('Type "help" for more information.')
    while True:
        command = get_command()
        if command == 'exit':
            break
        elif command == 'help':
            commands()
        elif command.startswith('regression'):
            single_regression(command)
        elif command.startswith('multivariate'):
            multi_regression(command)
        elif command == 'profit':
            profit()
        else:
            error()


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)
            error()
    return wrapper


@error_handler
def single_regression(command):
    args = command.split()
    regression(args[1])


@error_handler
def multi_regression(command):
    args = command.split()
    multivariate_regression(args[1:])


@error_handler
def profit():
    df = most_profitable_laptop()
    print(df)


def commands():
    print('Available commands:\n'
          '- regression <prop_name> - single variable linear regression\n'
          '- multivariate <prop1> <prop2> .. <propN> - multivariate linear regression\n'
          '- profit - get most profitable laptops\n')


def error():
    print('Invalid command, try "help" to get more information.')


def get_command():
    return re.sub('[^a-z_ ]', '', input('>>> ').strip().lower())


if __name__ == '__main__':
    start_main_loop()
