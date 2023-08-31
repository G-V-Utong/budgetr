#!/usr/bin/python3
"""Point of entry of the CLI
(cmd line interpreter)"""
import cmd
import json
from models.__init__ import storage
from models.base_model import BaseModel
from models.user import User
from models.expense import Expense
from models.budget import Budget
from models.tag import Tag
from models.transaction import Transaction
from models.catagory import Catagory
import shlex  # for splitting the line along spaces except in double quotes

#from models.review import Review


class BudgetrCommand(cmd.Cmd):
    """CL Interpreter"""
    prompt = '(budgetr) '

    classes = {'BaseModel': BaseModel, 'User': User, 'Tag': Tag,
               'Catagory':Catagory, 'Expense': Expense,
               'Budget': Budget, 'Transaction': Transaction}

    __lists = ['BaseModel', 'User', 'Expense', 'Budget',
               'Tag', 'Transaction', 'Catagory']
    """'User', 'Place', 'State'
               'City', 'Amenity', 'Review']"""

    __methods_ac = ['all', 'count']
    __methods_sd = ['show', 'destroy']

    #types = {'data': str}

    def help_quit(self):
        print('Quit command to exit the program\n')

    def emptyline(self):
        """shouldn’t execute anything
        """
        pass

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """End-of-file
        """
        return True

    def precmd(self, arg):
        """Hook method executed just before the command line
        "line" is interpreted, but after the input prompt
        is generated and issued. The return value is used
        as the command which will be executed."""
        swargs = arg.split('.')

        if swargs[0] in self.__lists:

            swargs1 = swargs[1].split('(')
            swargs2 = swargs1[1].split(')')
            ids = swargs2[0].strip('"\'')

            if swargs1[0] in self.__methods_ac:
                arg = swargs1[0] + ' ' + swargs[0]

            elif swargs1[0] in self.__methods_sd:
                arg = swargs1[0] + ' ' + swargs[0] + ' ' + ids

        return arg

    """
    def do_create(self, arg):
        if not arg:
            print('** class name missing **')
        elif arg not in self.__lists:
            print('** class doesn\'t exist **')

        else:
            if arg == 'BaseModel':
                arg = BaseModel()
            elif arg == 'User':
                arg = User()
            elif arg == 'ExpenseT':
                arg = ExpenseT()
            elif arg == 'BudgetT':
                arg = BudgetT()


            arg.save()
            print(arg.id)

    """
    def do_create(self, args):
        """ Create an object of any class"""

        args = args.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        elif args[0] not in BudgetrCommand.classes:
            print("** class doesn't exist **")
            return

        else:
            # if args[0] in HBNBCommand.classes:

            dicts = {}

            for arr in args[1:]:
                if "=" in arr:
                    arrs = arr.split('=')
                    k = arrs[0]
                    v = arrs[1]

                    if v[0] == v[-1] == '"':
                        v = v.replace('"', '')
                        v = v.replace('_', ' ')

                    else:
                        if '.' in v:
                            v = float(v)
                        else:
                            try:
                                v = int(v)

                            except DoesNotExist:
                                continue
                    dicts[k] = v

        new_instance = BudgetrCommand.classes[args[0]](**dicts)
        print(new_instance.id)
        #storage.save()
        new_instance.save()


    def do_show(self, arg):
        """Prints the string representation of an instance
        based on the class name and id
        ex: show BaseModel 1234-1234-1234
        """
        swargs = arg.split()
        """lists = ['BaseModel', 'User']"""

        if len(swargs) == 0:
            print('** class name missing **')

        elif swargs[0] not in self.__lists:
            print('** class doesn\'t exist **')

        elif len(swargs) == 1:
            print('** instance id missing **')

        elif len(swargs) == 2:
            dicts = storage.all()

            """obj_key = v.__class__.__name__ + '.' + v.id"""

            add_swargs = swargs[0] + '.' + swargs[1]

            for k, v in dicts.items():
                obj_key = v.__class__.__name__ + '.' + v.id

                if (add_swargs == obj_key):
                    print(dicts[add_swargs])
                    return

            print('** no instance found **')

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        ex: destroy BaseModel 1234-1234-1234
        """
        swargs = arg.split()
        """lists = ['BaseModel', 'User']"""

        if len(swargs) == 0:
            print('** class name missing **')

        elif swargs[0] not in self.__lists:
            print('** class doesn\'t exist **')

        elif len(swargs) == 1:
            print('** instance id missing **')

        elif len(swargs) == 2:
            dicts = storage.all()

            add_swargs = swargs[0] + '.' + swargs[1]

            for k, v in dicts.items():
                obj_key = v.__class__.__name__ + '.' + v.id

                if (add_swargs == obj_key):
                    del (dicts[add_swargs])
                    storage.save()
                    return

            print('** no instance found **')

    def do_all(self, arg):
        """prints all string representation of all
        instances based or not on the class name
        ex: all BaseModel or all
        """
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = storage.all()
        elif args[0] in BudgetrCommand.classes:
            obj_dict = storage.all(BudgetrCommand.classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

        """
        open_b = '["'
        close_b = '"]'

        if len(arg) == 0 or arg in self.__lists:
            print(open_b, end="")

            dicts = storage.all()

            for k, v in dicts.items():
                obj_key = v.__class__.__name__ + '.' + v.id
                print(dicts[obj_key], end="")
            print(close_b)

        elif arg not in self.__lists:
            print('** class doesn\'t exist **')
        """
    def do_update(self, arg):
        """Updates an instance based on the class name
        and id by adding or updating attribute
        Ex: $ update BaseModel 1234-1234-1234
        email "aibnb@mail.com"
        All other arguments should not be used
        Ex: $ update BaseModel 1234-1234-1234 email
        "aibnb@mail.com" first_name "Betty" =
        update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        swargs = arg.split()
        """add_swargs = swargs[0] + '.' + swargs[1]"""
        dicts = storage.all()
        """lists = ['BaseModel', 'User']"""

        if len(swargs) == 0:
            print('** class name missing **')

        elif swargs[0] not in self.__lists:
            print('** class doesn\'t exist **')

        elif len(swargs) == 1:
            print('** instance id missing **')

        else:
            add_swargs = swargs[0] + '.' + swargs[1]

            if add_swargs not in dicts:
                print('** no instance found **')

            elif len(swargs) == 2:
                print('** attribute name missing **')

            elif len(swargs) == 3:
                print('** value missing **')

            else:
                attri = swargs[2]
                val = swargs[3].strip('"\'')
                obj = dicts[add_swargs]

                obj.__dict__[attri] = val
                storage.save()

    def do_count(self, arg):
        """to retrieve the number of instances of a class
        ex: User.count()
        """
        if arg in self.__lists:
            counts = 0
            dicts = storage.all()

            for k, v in dicts.items():
                obj_name = v.__class__.__name__

                if (arg == obj_name):
                    counts += 1
            print(counts)



if __name__ == '__main__':
    BudgetrCommand().cmdloop()
