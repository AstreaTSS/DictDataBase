from . reading import  multiread, subread
from . writing import session, multisession, subsession
from . models import SubModel, DDBMethodChooser


def at(*path):
    return DDBMethodChooser(*path)
