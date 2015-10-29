"""
Coding challenge from here: https://www.thumbtack.com/challenges/simple-database
Simple Relational Database

Usable with standard input or fileread.
Commands available:
SET a b: stores variable a with value b
GET a: gets value of variable a
UNSET a: removes variable a
NUMEQUALTO b: retreives count of variables with value b
BEGIN: begins a transaction
ROLLBACK: resets changes since the start of the last transactions
COMMIT: saves all open transactions to database
"""

# commands which take 0, 1, or 2 arguments
NO_ARG = ['BEGIN', 'ROLLBACK', 'COMMIT']
ONE_ARG = ['GET', 'UNSET', 'NUMEQUALTO']
TWO_ARG = ['SET']
# order which transaction data is being stored
NAME_IND = 0
VAL_IND = 1

import sys

class Database(object):
    """
    Database class
    """

    def __init__(self):
        """
        Set up empty database, empty transactions, and commands
        """
        self.__names = {}
        self.__values = {}
        self.__transactions = []
        self.__num_transactions = 0
        self.finished = False
        self.commands = {   'SET' : self.__set_value,
                            'GET' : self.__get_value,
                            'UNSET': self.__unset_value,
                            'NUMEQUALTO': self.__num_equal_to_value,
                            'BEGIN': self.__begin_transaction,
                            'ROLLBACK': self.__rollback_transaction,
                            'COMMIT': self.__commit_transaction}

    def get_command(self, command, arg_1=None, arg_2=None):
        """
        Receives a command from the user and calls the appropriate internal function
        command: any of the strings in self.commands
        arg_1: for SET, GET, UNSET: variable name. for NUMEQUALTO: value to get count for
        arg_2: for SET: value to store to variable name
        """
        if command == 'END':
            self.finished = True
            return
        elif command in TWO_ARG:
            return self.commands[command](arg_1, arg_2)
        elif command in ONE_ARG:
            return self.commands[command](arg_1)
        elif command in NO_ARG:
            return self.commands[command]()
        else:
            return 'UNRECOGNIZED COMMAND'

    def __begin_transaction(self):
        """
        Begins a transaction, meaning that the following commands will be stored
        as a 'transaction' rather than directly to the database until they are either
        committed or rolled back
        """
        # make copy of current data and add to transaction list
        self.__transactions.append((dict(self.__names), dict(self.__values)))
        self.__num_transactions += 1
        return

    def __rollback_transaction(self):
        """
        Rolls back one transaction, dropping the changes since the last 'BEGIN'
        """
        if self.__num_transactions == 0:
            return 'NO TRANSACTION'
        else:
            self.__transactions.pop()
            self.__num_transactions -= 1
            return

    def __commit_transaction(self):
        """
        Stores all changes in any existing transaction to the database and resets
        the transactions
        """
        if self.__num_transactions == 0:
            return 'NO TRANSACTION'
        else:
            self.__names, self.__values = self.__transactions.pop()
            self.__transactions = []
            self.__num_transactions = 0
            return

    def __set_value(self, name, value):
        """
        Store the variable name as value in the database
        Passes in the appropriate dictionaries and values to __assign_value (to account
        for possible open transactions)
        name: name of variable to store
        value: value of variable to store
        """
        # first remove any value previously stored, and deincrement the value count
        # so it doesn't get off
        self.__unset_value(name)
        # then add it below
        if self.__num_transactions == 0:
            # modify database value if we aren't in a transaction
            return self.__assign_value(self.__names, self.__values, name, value)
        else:
            # modify transaction values
            return self.__assign_value(
                                self.__transactions[self.__num_transactions-1][NAME_IND],
                                self.__transactions[self.__num_transactions-1][VAL_IND],
                                name, value)

    def __assign_value(self, names, values, name, value):
        """
        Actually stores the value to the name dictionary, and increments the counter in the
        value dictionary
        names: dictionary of names
        values: dictionary of value counts
        name: name of variable to be stored
        value: value of variiable to be stored
        """
        names[name] = value
        values[value] = values.get(value, 0) + 1

    def __get_value(self, name):
        """
        Retrieves the value of the variable stored to name, returning 'NULL' if
        there is nothing there
        name: the name of the variable to retrieve the value
        """
        if self.__num_transactions == 0:
            # retrieve from database if we aren't in a transaction
            return self.__names.get(name, 'NULL')
        else:
            # retrieve transaction value
            return self.__transactions[self.__num_transactions-1][NAME_IND].get(name, 'NULL')

    def __unset_value(self, name):
        """
        Unset the variable under the given name so that it is as if it was never set
        name: the name of the variable to be unset
        """
        if self.__num_transactions == 0:
            # unset database variable if not in transaction
            return self.__remove(self.__names, self.__values, name)
        else:
            # unset transaction variable
            return self.__remove(
                                self.__transactions[self.__num_transactions-1][NAME_IND],
                                self.__transactions[self.__num_transactions-1][VAL_IND],
                                name)

    def __remove(self, names, values, name):
        """
        Actually removes the name by popping it from the given dictionary, and
        deincrementing the count in the value dictionary
        names: dictionary of names
        values: dictionary of value counts
        name: name of variable to be removed
        value: value of variiable to be removed
        """
        try:
            # use a try catch so we don't crash if we try to remove an unset variable
            value = names.pop(name)
            values[value] -= 1
        except KeyError:
            pass
        return

    def __num_equal_to_value(self, value):
        """
        Finds the number of variables set to the given value, by retrieving the
        count from the appropriate dictionary
        value: the value that is being counted
        """
        if self.__num_transactions == 0:
            # retrieve count from database if not in transaction
            return self.__values.get(value,0)
        else:
            # retreive count from transaction otherwise
            return self.__transactions[self.__num_transactions-1][VAL_IND].get(value,0)

def file_read(db, filename):
    """
    Function that handles user input from files, with commands separated by newlines
    filename: the file which contains the commands to be followed
    """
    with open(filename, 'r-') as f:
        for line in f:
            # so that we cannot carry on after sending END
            if db.finished:
                break
            print line.strip('\n')
            # split command by spaces
            command = line.split()
            if command:
                out = db.get_command(*command)
                if out != None:
                    # we don't want to print None
                    print out

def std_in(db):
    """
    Function that handles user input from the command line
    """
    while not db.finished:
        # split command by spaces
        command = raw_input().split()
        if command:
            out = db.get_command(*command)
            if out != None:
                # we don't want to print None
                print out

if __name__ == '__main__':
    db = Database()
    if len(sys.argv) > 1:
        # if we give it a file, use the file..
        file_read(db, sys.argv[1])
    else:
        # otherwise use standard input
        std_in(db)
