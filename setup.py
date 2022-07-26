# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# SPDX-License-Identifier: BSD-3-Clause-Clear
# Copyright (c) 2022 BigML, Inc
#

import subprocess


from setuptools import setup
from setuptools.command.install import install


class NPMInstall(install):

    def run(self):
        subprocess.check_output("npm install xmlhttprequest", shell=True)
        install.run(self)

with open('README.md') as f:
    readme = f.read()

setup(
    name='whizzml_kernel',
    version='0.1.1',
    packages=['whizzml_kernel', 'whizzml', 'magics'],
    package_data={'whizzml':['whizzml_node.js']},
    description='Simple WhizzML kernel for Jupyter',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='BigML Team',
    author_email='bindings@bigml.com',
    url='https://github.com/whizzml/whizzml_kernel',
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel', 'javascript', 'bigml', 'notebook'
    ],
    cmdclass={
        'install': NPMInstall
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
