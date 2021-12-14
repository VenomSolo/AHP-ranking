import AHP_App

available_commands = ["help", "check", "take", "quit"]
comm_dict = {
    "help": lambda x: Help(x),
    "check": lambda x: CheckForms(x),
    "take": lambda x: TakeForm(x),
    "quit": lambda x: quit()
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
    for comm in available_commands:
        print(comm)


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
