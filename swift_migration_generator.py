"""swift_migration_generator.py
Generate a database migration file for the
SQLiteMigrationManager.swift framework.
"""
import os
import time
import click
import string


class SimpleFormatter(string.Formatter):
    """A very simple formatter for templating source files.
    https://github.com/ebrehault/superformatter/blob/master/engine.py
    """
    def format_field(self, value, spec):
        if spec.startswith('repeat'):
            template = spec.partition(':')[-1]
            if type(value) is dict:
                value = value.items()
            return ''.join([template.format(item=item) for item in value])
        elif spec == 'call':
            return value()
        elif spec.startswith('if'):
            return (value and spec.partition(':')[-1]) or ''
        else:
            return super(SimpleFormatter, self).format_field(value, spec)


def toLowerFirst(s):
    """Takes a string and makes the first character lower-case.
    :param s: The string to modify.
    :returns: `s` with an lower first character.
    """
    return s[0].lower() + ''.join(s[1:])


def toUpperFirst(s):
    """Takes a string and makes the first character upper-case.
    :param s: The string to modify.
    :returns: `s` with an upper first character.
    """
    return s[0].upper() + ''.join(s[1:])


def toCamel(s):
    """Take a word or space-separated phrase and convert to a
    camel case string (i.e., `camelCase`).
    :param s: The word or phrase to convert.
    :returns: `s` in camel case.
    """
    # split on spaces
    components = s.split(' ')
    # leave the first word, and capitalize all the following words
    camel = toLowerFirst(components[0]) + ''.join(toUpperFirst(x) for x in components[1:])
    return camel


def toPascal(s):
    """Take a word or space-separated phase and convert to a
    pascal case string (i.e., `PascalCase`).
    :param s: The word or phrase to convert.
    :returns: `s` in pascal case.
    """
    # make the name camel
    camel = toCamel(s)
    # make the first character upper-case
    return toUpperFirst(camel)


def getTimeString():
    """Get the current time string intended for the version int"""
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


template = '''
import Foundation
import SQLiteMigrationManager
import SQLite

struct {name}: Migration {{

    var version: Int64 = {time}

    func migrateDatabase(_ db: Connection) throws {{

        // TODO: Perform the migration here

    }}
}}
'''


def createMigration(name, dst):
    # prepare our migration struct name
    n = toPascal(name)
    filepath = os.path.join(dst, '%s.swift' % n)
    # prepare our time string
    t = getTimeString()
    # run the formatter on the template
    sf = SimpleFormatter()
    out = sf.format(template, name=n, time=t)
    # save the file
    with open(filepath, 'w') as output:
        output.write(out)


@click.command()
@click.argument('name', nargs=1)
@click.argument('dst', nargs=1)
def main(name, dst):
    createMigration(name, dst)


if __name__ == '__main__':
    main()

