"""
    this is just an EXAMPLE
    you may change anything you want here !
"""

from app.api.control import ControlLogsFile
from app.api.syntax import logsSyntax

def paidFunction(number):
    return getNumberProvider(number)

def getNumberProvider(number):
    provider = "something"
    return logsSyntax(number,provider),provider