#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.core.management import execute_from_command_line
import os
import sys


__author__ = "Zeinab Abbasimazar -> https://github.com/zeinababbasi"


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    execute_from_command_line(sys.argv)
