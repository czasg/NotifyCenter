# coding: utf-8
import pywss

from .label import register as register_label
from .notify import register as register_notify
from .user import register as register_user


def register(app: pywss.App):
    register_label(app.party("/label"))
    register_notify(app.party("/notify"))
    register_user(app.party("/user"))
