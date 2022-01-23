import AHP_App

available_commands = [
    "help", "add", "remove", "check", "read", "quit", "rank", "inconsistency",
    "experts"
]
comm_dict = {
    "help": lambda x: Help(x),
    "check": lambda x: CheckForms(x),
    "add": lambda x: AddForm(x),
    "remove": lambda x: RemoveForm(x),
    "read": lambda x: ReadForm(x),
    "rank": lambda x: RankForm(x),
    "inconsistency": lambda x: CheckInconsistency(x),
    "experts": lambda x: ListExperts(x),
    "quit": lambda x: quit()
}

syntax_dict = {
    "help": "help [command]",
    "check": "check",
    "add": "add [form name]",
    "remove": "remove [form name]",
    "read": "read [form name]",
    "rank": "rank [form name] [method]",
    "inconsistency": "inconsistency [form name] [expert name]",
    "experts": "experts [form name]",
    "quit": "quit"
}

desc_dict = {
    "help": "Shows syntax and description of chosen command",
    "check": "Lists all forms available on server",
    "add": "Adds new form with given name to the list of available forms",
    "remove": "Removes form with given name from the list of available forms",
    "read":
    """Lists experts that have taken form with given name with their respective
results presented in low-level notation""",
    "rank": """Calculates ranking of form with given name using chosen method:
EVM - Eigenvalue Method,
GMM - Geometrical Mean Method""",
    "inconsistency":
    """Calculates inconsistency index and ratio of chosen expert
who has taken form with given name""",
    "experts": "Lists all experts who have taken form with given name",
    "quit": "Quit program"
}


def _check_arg_number(arg, num):
    return len(arg) == num


def CheckForms(args):
    if not _check_arg_number(args, 0):
        return
    for title in AHP_App.check_forms(server):
        print(title)


def ListExperts(args):
    if not _check_arg_number(args, 1):
        return
    AHP_App.get_experts(server, args[0])


def CheckInconsistency(args):
    if not _check_arg_number(args, 2):
        return
    AHP_App.check_consistency(server, args[0], '$' + args[1])


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
    try:
        AHP_App.read_form(server, args[0])
    except FileNotFoundError:
        print("Form results not found")
        pass


def RankForm(args):
    if not _check_arg_number(args, 2):
        return
    AHP_App.rank_form(server, args[0], args[1])


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


server = input("Link with file: ")

while True:

    command = input(">>")

    comm, args = command.split(" ")[0], command.split(" ")[1:]
    if comm in available_commands:
        comm_dict[comm](args)
    else:
        print(
            "Command not found. Try 'help' for list of available commands.\n")
