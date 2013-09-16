__author__ = 'tinyms'

import json
from tinyms.core.common import Utils
from tinyms.core.web import IAuthRequest
from tinyms.core.point import route,ajax,auth

@ajax("OrgEdit")
class OrgEdit():
    __export__ = []