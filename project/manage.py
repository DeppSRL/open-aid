#!/usr/bin/env python
import os
import sys
import environ
if __name__ == "__main__":
    env = environ.Env(
        DEBUG=(bool, True),
    )
    root = environ.Path(__file__) - 2 # (/open-aid/project - 2 = /open-aid/)
    config = root('config')+"/.env"
    env.read_env(config)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", env('DJANGO_SETTINGS_MODULE'))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)