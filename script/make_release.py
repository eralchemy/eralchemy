import argparse
import os
import sys
from getpass import getpass
from shutil import rmtree
from subprocess import PIPE, Popen

# inspired by https://github.com/mitsuhiko/flask/blob/master/scripts/make-release.py
from poetry.poetry import Poetry

def set_filename_version(filename, version_number):
    with open(filename, "w+") as f:
        f.write("version = '{}'\n".format(version_number))


def set_init_version(version_str):
    info("Setting __init__.py version to %s", version_str)
    set_filename_version("eralchemy2/version.py", version_str)


def rm(filename):
    info("Delete {}".format(filename))
    rmtree(filename, ignore_errors=True)


def build_and_upload():
    rm("eralchemy2.egg-info")
    rm("build")
    rm("dist")
    Popen(["poetry", "build"]).wait()
    pypi_pwd = getpass(prompt="Pypi Password: ")
    Popen(["poetry", "publish", "-u", "maurerle", "-p", pypi_pwd]).wait()
    Popen(["open", "https://pypi.org/project/eralchemy2/"])
    Popen(["git", "tag"], stdout=PIPE).communicate()[0].splitlines()
    Popen(["git", "push", "--tags"]).wait()

def fail(message, *args):
    print("Error:", message % args, file=sys.stderr)
    sys.exit(1)


def info(message, *args):
    print("Error:", message % args, file=sys.stderr)


def git_is_clean():
    return Popen(["git", "diff", "--quiet"]).wait() == 0


def make_git_commit(message, *args):
    message = message % args
    Popen(["git", "commit", "-am", message]).wait()


def make_git_tag(tag):
    info('Tagging "%s"', tag)
    Popen(["git", "tag", tag]).wait()


def version_str_to_lst(v):
    return [int(s) for s in v.split(".")]


def version_lst_to_str(v):
    return ".".join(str(n) for n in v)


def parse_args():
    """Parse the args, returns if the type of update:
    Major, minor, fix
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-M", action="store_true")
    parser.add_argument("-m", action="store_true")
    parser.add_argument("-f", action="store_true")
    args = parser.parse_args()
    major, minor, fix = args.M, args.m, args.f
    if major + minor + fix != 1:
        fail("Please select one and only one action.")
    return major, minor, fix


def get_current_version():
    from importlib.metadata import version
    return version_str_to_lst(version("eralchemy2"))


def get_git_tags():
    return set(Popen(["git", "tag"], stdout=PIPE).communicate()[0].splitlines())


def get_next_version(major, minor, fix, current_version):
    if major:
        return [current_version[0] + 1, 0, 0]
    if minor:
        return [current_version[0], current_version[1] + 1, 0]
    if fix:
        return [current_version[0], current_version[1], current_version[2] + 1]
    raise UserWarning()


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    Popen(["poetry", "install"]).wait()
    current_version = get_current_version()
    major, minor, fix = parse_args()
    next_version = get_next_version(major, minor, fix, current_version)
    next_version_str = version_lst_to_str(next_version)
    tags = get_git_tags()

    if next_version_str in tags:
        fail('Version "%s" is already tagged', next_version_str)

    #if not git_is_clean():
    #    fail("You have uncommitted changes in git")

    Popen(["poetry", "version", next_version_str]).wait()
    make_git_commit("Bump version number to %s", next_version_str)
    make_git_tag("v" + next_version_str)
    build_and_upload()


if __name__ == "__main__":
    main()
