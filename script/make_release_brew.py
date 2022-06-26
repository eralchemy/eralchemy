from poet.poet import formula_for
from subprocess import Popen
from script import make_release
import os


def main():
    with open('eralchemy2.template.rb') as f:
        f.readlines()

    formula = formula_for('eralchemy2')
    with open('/usr/local/Library/Formula/eralchemy2.rb', 'w+') as f:
        f.writelines(formula)
    Popen(['brew', 'update'])
    os.chdir('/usr/local')
    version_list = make_release.get_current_version()
    version = make_release.version_lst_to_str(version_list)
    Popen(['brew', 'uninstall', 'eralchemy2'])
    Popen(['brew', 'install', 'eralchemy2'])
    Popen(['brew', 'audit', '--strict', '--online', 'eralchemy2'])
    branch_name = 'eralchemy2{}'.format(version)
    Popen(['git', 'checkout', '-b', branch_name])
    Popen(['git', 'add', 'Library/Formula/eralchemy2.rb', branch_name])
    commit_message = \
        """eralchemy2 v{version}'


Updated eralchemy2 to v{version}.
""".format(version=version)
    Popen(['git', 'commit', branch_name, '-m', commit_message])


if __name__ == '__main__':
    main()
