#!/usr/bin/python3
''' module contain do_pack, do_deploy, deploy '''

from fabric.api import local, put, run, env
from datetime import datetime
from os.path import exists, basename

# deploy it on your servers: xx-web-01 and xx-web-02
env.hosts = ['54.157.131.239', '34.202.157.240']
env.user = 'ubuntu'


def do_pack():
    ''' generates a .tgz archive from the contents of the web_static folder
    of your AirBnB Clone repo '''

    # name of archive web_static_<year><month><day><hour><minute><second>.tgz
    time = datetime.now()
    str_time = time.strftime("%Y%m%d%H%M%S")
    arch_name = f"web_static_{str_time}.tgz"
    arch_path = f"versions/{arch_name}"

    if not exists('./versions'):
        if local("mkdir versions").failed:
            return None

    if local(f"tar -cvzf {arch_path} web_static").failed:
        return None

    return arch_path


def do_deploy(archive_path):
    ''' distributes an archive to my web servers '''

    file_name = basename(archive_path)
    dir_name = file_name.rstrip('.tgz')

    remote_tmp = f"/tmp/{file_name}"
    extract_path = f"/data/web_static/releases/{dir_name}"
    link_path = "/data/web_static/current"

    if put(archive_path, remote_tmp).failed:
        return False

    if run(f"mkdir -p {extract_path}").failed:
        return False

    if run(f"tar -xzf {remote_tmp} -C {extract_path}").failed:
        return False

    if run(f"rm {remote_tmp}").failed:
        return False

    if run(f"mv {extract_path}/web_static/* {extract_path}").failed:
        return False

    if run(f"rm -rf {extract_path}/web_static").failed:
        return False

    if run(f"rm -rf {link_path}").failed:
        return False

    if run(f"ln -s {extract_path} {link_path}").failed:
        return False

    return True


def deploy():
    ''' creates and distributes an archive to your web servers '''
    archive_path = do_pack()

    if archive_path is None:
        return False

    return do_deploy(archive_path)
