# package des settings :

import pymysql

pymysql.install_as_MySQLdb()

from .base import *


try:
    from .develop import *
except ModuleNotFoundError:
    pass

try:
    from .production import *
except ModuleNotFoundError:
    pass
