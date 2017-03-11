#!/usr/bin/python3

# SteamFastLogin - Login manager for Steam, allowing fast switching between accounts
# Copyright (C) 2017 Matthew Gamble <git@matthewgamble.net>
#
# This project is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License Version 3 as published by the Free
# Software Foundation. No other version currently applies to this project. This
# project is distributed without any warranty. Please see LICENSE.txt for the
# full text of the license.

from setuptools import find_packages, setup

from steamfastlogin import __VERSION__

setup(
    name="steamfastlogin",
    version=__VERSION__,
    license="GPLv3",
    description="Login manager for Steam, allowing fast switching between accounts",
    long_description=open("README.txt").read(),
    url="https://github.com/djmattyg007/SteamFastLogin",
    author="Matthew Gamble",
    author_email="git@matthewgamble.net",
    packages=find_packages(),
    install_requires=["appdirs", "keyring", "PyQt5"],
    entry_points=dict(console_scripts=[
        "steam-fast-login = steamfastlogin.cli:main"
    ]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Games/Entertainment",
    ])
