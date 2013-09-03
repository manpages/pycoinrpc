#!/usr/bin/env python

from setuptools import setup

version = "0.0.23"

setup(
    name="pycoinrpc",
    version=version,
    packages = [
      "pycoinrpc",
      "pycoinrpc.servers",
    ],
    author="Jonn Mostovoy",
    entry_points = { 'console_scripts':
            [
                'pycoincli = pycoinrpc.servers.cli:main',
                #'pycoinrpc = pycoinrpc.servers.pycoinrpc:main',
            ]
        },
    author_email="amarr.industrial@gmail.com",
    url="https://github.com/manpages/pycoinrpc",
    license="http://opensource.org/licenses/MIT",
    description="Poorly documented CLI and JSON-RPC wrappers for pycoin"
)
