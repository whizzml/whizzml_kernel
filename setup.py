#!/usr/bin/env python
#
# Copyright 2022 BigML, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import subprocess


from distutils.core import setup
from distutils.command.build import build


class NPMInstall(build):

    def run(self):
        build.run(self)
        subprocess.check_output("npm install xmlhttprequest", shell=True)

with open('README.md') as f:
    readme = f.read()

setup(
    name='whizzml_kernel',
    version='0.1',
    packages=['whizzml_kernel', 'whizzml', 'magics'],
    package_data={'whizzml':['whizzml_node.js']},
    description='Simple WhizzML kernel for Jupyter',
    long_description=readme,
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
