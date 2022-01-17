import AHP_App

available_commands = ["help", "check", "take", "quit"]
comm_dict = {
    "help": lambda x: Help(x),
    "check": lambda x: CheckForms(x),
    "take": lambda x: TakeForm(x),
    "quit": lambda x: quit()
}

syntax_dict = {
    "help": "help [command]",
    "check": "check",
    "take": "take [form name]",
    "quit": "quit"
}

desc_dict = {
    "help": "Shows syntax and description of chosen command",
    "check": "Lists all forms available on server",
    "take": "Take form with given name",
    "quit": "Quit program"
}


def _check_arg_number(arg, num):
    return len(arg) == num


def CheckForms(args):
    if not _check_arg_number(args, 0):
        return
    for title in AHP_App.check_forms(server):
        print(title)


def TakeForm(args):
    if not _check_arg_number(args, 1):
        return
    AHP_App.take_form(server, args[0], username)


def Help(args):
    if not _check_arg_number(args, 1):
        for comm in available_commands:
            print(comm)
        return
    comm = args[0]
    print("NAME")
    print(comm)
    print("SYNTAX")
    print(syntax_dict[comm])
    print("DESCRIPTION")
    print(desc_dict[comm])


username = input("Username: ")
server = input("Server: ")

while True:

    command = input(">>")

    comm, args = command.split(" ")[0], command.split(" ")[1:]
    if comm in available_commands:
        comm_dict[comm](args)
    else:
        print(
            "Command not found. Try 'help' for list of available commands.\n")
