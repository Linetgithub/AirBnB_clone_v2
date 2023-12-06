#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import local, env, run, lcd, put
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/my_ssh_private_key'


def do_pack():
    try:
        local("mkdir -p versions")
        archive_name = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".tgz"
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception as e:
        return None


def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_extension = os.path.splitext(archive_name)[0]
        release_path = "/data/web_static/releases/{}".format(archive_no_extension)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, release_path))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}/web_static/* {}".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))

        return True
    except Exception as e:
        return False


def deploy():
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    number = int(number)
    if number < 0:
        return
    elif number == 0 or number == 1:
        local("ls -1t versions | tail -n +2 | xargs -I {} rm versions/{}")
        run("ls -1t /data/web_static/releases | tail -n +2 | xargs -I {} rm -rf /data/web_static/releases/{}")
    else:
        local("ls -1t versions | tail -n +{} | xargs -I {} rm versions/{}"
              .format(number + 1, "{}"))
        run("ls -1t /data/web_static/releases | tail -n +{} | xargs -I {} rm -rf /data/web_static/releases/{}"
            .format(number + 1, "{}"))

