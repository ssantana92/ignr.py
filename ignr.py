#! /usr/bin/env python

import argparse, os, sys
import gitignoreio_api as api

def get_usage_msg(name=None):                                                            
    return '''
    
    ignr.py [-h] (--list | --new TECH [TECH ...] [--preview])

          Python-based CLI tool for gitignore.io

    --help,    -h             show this message and exit
    --list,    -l             list all available .gitignore templates
    --new,     -n TECH ...    space-separated list of technologies to include
    --preview, -p             (use with --new ) preview .gitignore contents

    '''

def user_choice(query):
    while (True):
        choice = raw_input(query + " (y/n) ").lower()
        if choice in ['yes', 'y', 'yep', 'yup']:
           return True
        elif choice in ['no', 'n', 'nope', 'nah']:
           return False
        else:
           print "Please respond with 'y' or 'n'."

parser = argparse.ArgumentParser(usage=get_usage_msg())

# Accept list instruction, search instruction, OR create instruction
list_or_search = parser.add_mutually_exclusive_group(required=True)
list_or_search.add_argument('--list', '-l', action='store_true')
list_or_search.add_argument('--new', '-n', dest='gi_stack', metavar='TECH', nargs='+')
# Optional output preview flag (manually checked)
parser.add_argument('--preview', '-p', action='store_true')

args = parser.parse_args()

if args.list:
    template_list = api.get_template_list()
    print '\n'.join(template_list)

else:
    try:
        ignr_file = api.get_gitignore(args.gi_stack)
    except ValueError as ve:
        print "ERROR: " + ve.args[0] + " is invalid or is not supported on gitignore.io."
        sys.exit(1)

    if args.preview:
        print ignr_file

    else:
        if os.path.isfile('.gitignore'):
            overwrite = user_choice(".gitignore exists in current directory. Overwrite?")

            if overwrite is False:
                print "Ok. Exiting..."
                sys.exit(0)

            elif overwrite is True:
                if user_choice("Back up current .gitignore?") is True:
                    print "Backing up .gitignore as 'OLD_gitignore'..."
                    os.rename('.gitignore', 'OLD_gitignore')

        with open('.gitignore', 'w') as f:
            f.write("# File generated by ignr.py (github.com/Antrikshy/ignr)\n{0}".format(ignr_file))

        print "New .gitignore file generated for " + ", ".join(args.gi_stack) + "."

sys.exit(0)
