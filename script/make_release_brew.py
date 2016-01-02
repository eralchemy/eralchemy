from poet.poet import formula_for
from subprocess import Popen, PIPE
from script import make_release
import os

def main():
    with open('eralchemy.template.rb') as f:
        template = f.readlines()

    formula = formula_for('eralchemy')
    with open('/usr/local/Library/Formula/eralchemy.rb', 'w+') as f:
        f.writelines(formula)
    Popen(['brew', 'update'])
    os.chdir('/usr/local')
    version_list = make_release.get_current_version()
    version = make_release.version_lst_to_str(version_list)
    Popen(['brew', 'uninstall', 'eralchemy'])
    Popen(['brew', 'install', 'eralchemy'])
    Popen(['brew', 'audit', '--strict', '--online', 'eralchemy'])
    branch_name = 'eralchemy_v{}'.format(version)
    Popen(['git', 'checkout', '-b', branch_name])
    Popen(['git', 'add', 'Library/Formula/eralchemy.rb', branch_name])
    commit_message = \
"""ERAlchemy v{version}'


Updated ERAlchemy to v{version}.
""".format(version=version)
    Popen(['git', 'commit', branch_name, '-m', commit_message])

if __name__ == '__main__':
    main()
