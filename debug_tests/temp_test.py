# debug_tests/temp_test.py

from src.gpib.gpib_command_model335 import Model335GPIBCommand

def temp_test():
    model_335_command = Model335GPIBCommand()

    model_335_command.init_connection()
    temp = model_335_command.query_celsius()

    return temp


if __name__ == '__main__':
    temp_test()
