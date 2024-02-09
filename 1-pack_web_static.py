#!/usr/bin/python3
''' a Fabric script that generates a .tgz archive
from the contents of the web_static folder of your AirBnB Clone repo,
using the function do_pack. '''

from fabric.api import local
from datetime import datetime
from os.path import exists


def do_pack():
    ''' generates a .tgz archive from the contents of the web_static folder
    of your AirBnB Clone repo '''

    # name of archive web_static_<year><month><day><hour><minute><second>.tgz
    time = datetime.now()
    str_time = time.strftime("%Y%m%d%H%M%S")
    arch_name = f"web_static_{str_time}.tgz"

    if not exists('./versions'):
        if local("mkdir versions").failed:
            return None

    if local(f"tar -cvzf versions/{arch_name} web_static").failed:
        return None

    return arch_name
