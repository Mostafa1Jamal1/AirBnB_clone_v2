#!/usr/bin/python3
''' a Fabric script that that distributes an archive to your web servers,
using the function do_deploy '''

from fabric.api import put, run, env
from os.path import basename

# deploy it on your servers: xx-web-01 and xx-web-02
env.hosts = ['54.157.131.239', '34.202.157.240']
env.user = 'ubuntu'


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
