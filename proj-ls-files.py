#!/usr/bin/python3
import subprocess
import os

LINE_FORMAT = '\033[33m{prefix} \033[37m{path}\033[0m{base}'

def get_files(cmd, prefix):
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        encoding='utf8',
    )
    try:
        for line in p.stdout:
            line = line.strip()
            base = os.path.basename(line)
            path = os.path.dirname(line)
            if path:
                path += "/"
            print(LINE_FORMAT.format(prefix=prefix, path=path, base=base))
    finally:
        p.wait()


def get_git_files(git_root):
    get_files(['git', 'ls-files', '-c', git_root], 'git')
    get_files(
        ['git', 'ls-files', '-o', '--exclude-standard', git_root],
        'git-other',
    )
    if os.path.exists('.gitmodules'):
        mod_prefixes = subprocess.check_output(['git', 'config', '--file', '.gitmodules', '--get-regexp', 'path'])
        mod_prefixes = [l.decode('utf8') for l in mod_prefixes.split()]
        get_files(['git', 'ls-files', '--recurse-submodules'] + mod_prefixes, 'git-submodules')


def get_find_files():
    get_files(['find', '-type', 'f', '-follow'], 'find')


def main():
    # Get rid of all stderr output
    os.close(2)
    try:
        git_root = subprocess.check_output(
            ('git', 'rev-parse', '--show-toplevel')
        ).strip()
    except subprocess.CalledProcessError:
        git_root = None

    if git_root is not None:
        get_git_files(git_root)
    else:
        get_find_files()


if __name__ == '__main__':
    main()
