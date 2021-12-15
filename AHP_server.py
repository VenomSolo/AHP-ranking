import AHP_App

available_commands = ["help", "add", "remove", "check", "read", "quit"]
comm_dict = {
    "help": lambda x: Help(x),
    "check": lambda x: CheckForms(x),
    "add": lambda x: AddForm(x),
    "remove": lambda x: RemoveForm(x),
    "read": lambda x: ReadForm(x),
    "quit": lambda x: quit()
}


def _check_arg_number(arg, num):
    return len(arg) == num


def CheckForms(args):
    if not _check_arg_number(args, 0):
        return
    for title in AHP_App.check_forms(server):
        print(title)


def AddForm(args):
    if not _check_arg_number(args, 1):
        return
    AHP_App.add_form(server, args[0])


def RemoveForm(args):
    if not _check_arg_number(args, 1):
        return
    AHP_App.remove_form(server, args[0])


def ReadForm(args):
    if not _check_arg_number(args, 1):
        return
    AHP_App.read_form(server, args[0])


def Help(args):
    for comm in available_commands:
        print(comm)


server = input("Link with file: ")

while True:

    command = input(">>")

    comm, args = command.split(" ")[0], command.split(" ")[1:]
    if comm in available_commands:
        comm_dict[comm](args)
    else:
        print(
            "Command not found. Try 'help' for list of available commands.\n")
