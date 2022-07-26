# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# SPDX-License-Identifier: BSD-3-Clause-Clear
# Copyright (c) 2022 BigML, Inc
#


import re
import requests
import json

from subprocess import check_output

from IPython.core.magic import (Magics, magics_class, line_magic,
    cell_magic)
from ipykernel import get_connection_file

from requests.compat import urljoin
from notebook.notebookapp import list_running_servers

from whizzml_kernel.interpreter import Interpreter
from IPython import get_ipython
from bigml.api import BigML



EXPORT_CODE_STR = "jupyter nbconvert --RegexRemovePreprocessor.patterns='^%%.*' --RegexRemovePreprocessor.patterns='^!.*' --to script %s"

DFT_METADATA = {
    "name": "my script",
    "description": "my description"}


def get_kernel_id():
    """Gets the current kernel ID """
    connection_file = get_connection_file()
    kernel_id = re.search('kernel-(.*).json',
                          connection_file).group(1)
    return kernel_id


def get_notebook_name(kernel_id):
    """ Retrieving notebook name from kernel_id """
    servers = list(list_running_servers())
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                params={'token': ss.get('token', '')})
        try:
            for nn in json.loads(response.text):
                if nn['kernel']['id'] == kernel_id:
                    relative_path = nn['path']
                    return relative_path
        except:
            pass
    return None


def create_metadata(inputs, outputs):
    """Populates the metadata dictionary needed to create the script """
    metadata = DFT_METADATA
    inputs_list = []
    outputs_list = []
    for input_item in inputs:
        input_def = {"name": input_item,
                     "type": "numeric",
                     "default": 0,
                     "description": "my %s input" % input_item}
        inputs_list.append(input_def)
    for output_item in outputs:
        output_def = {"name": output_item,
                      "type": "numeric"}
        outputs_list.append(output_def)
    if inputs:
        metadata.update({"inputs": inputs_list})
    if outputs:
        metadata.update({"outputs": outputs_list})
    return metadata


@magics_class
class WhizzMLMagic(Magics):

    @line_magic
    def wstore(self, line):
        """Retrieves the contents of the current notebook and extracts only
        WhizzML inputs. Generates the corresponding meta file with default
        choices and adds a new input where that dictionary can be modified and
        a WhizzML script can be created.
        """
        notebook_path = get_notebook_name(get_kernel_id())
        whizzml_path = notebook_path.replace(".ipynb", ".whizzml")
        command = EXPORT_CODE_STR % notebook_path
        check_output(command, shell=True)
        with open(whizzml_path) as whizzml_source:
            whizzml_code = whizzml_source.read()
        self.ip = get_ipython()
        self.ip.user_ns["_whizzml_file"] = whizzml_path
        self.ip.user_ns["_whizzml_meta_file"] = whizzml_path.replace(".whizzml",
                                                                     ".json")
        self.ip.user_ns["_whizzml_code"] = whizzml_code
        inputs = self.ip.interpreter.inputs(whizzml_code)
        outputs = self.ip.interpreter.outputs(whizzml_code)
        metadata = create_metadata(inputs, outputs)
        self.ip.set_next_input("%%%%wscript\r\n%s" % json.dumps(metadata, indent=4))
        return metadata

    @cell_magic
    def wscript(self, line, cell):
        """The modified meta information is stored in the corresponding file
        and a WhizzML script is created
        """
        try:
            with open(self.ip.user_ns["_whizzml_meta_file"], "w") as metafile:
                metafile.write(cell)
            api = BigML()
            script = api.create_script(
                self.ip.user_ns["_whizzml_code"], args=json.loads(cell))
            return script["resource"]
        except:
            return "No previously stored WhizzML code"

    @line_magic
    def wsource(self, line):
        """Shows the stored WhizzML code """
        try:
            return self.ip.user_ns["_whizzml_code"]
        except:
            return "No previously stored WhizzML code."

    @line_magic
    def wreset(self, line):
        """Deletes the stored WhizzML information """
        if not hasattr(self, "ip") or self.ip is None:
            return "No previously stored WhizzML information was found."
        self.ip = None
        return "New WhizzML environment."
