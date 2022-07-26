# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# SPDX-License-Identifier: BSD-3-Clause-Clear
# Copyright (c) 2022 BigML, Inc
#

"""
whizzml.interpreter

User level interface to the WhizzML interpreter.


"""
import time

from javascript import require, globalThis
from bigml.util import get_exponential_wait


def prettify_error(error):
    """Removing extra properties and exposing line and column information in
    a more human-friendly way
    """
    error_str = ""
    if isinstance(error, list):
        error = error[0]
    if not isinstance(error, dict):
        error = error.valueOf()
    if error.get("message"):
        error_str = error.get("message")
    elif error.get("error"):
        error_str = error.get("error")
    else:
        error_str = "%s" % error
    if error.get("variables"):
        error_str += " [%s]" % ", ".join(error.get("variables"))
    if error.get("instruction", {}).get("source"):
        error["source"] = error.get("instruction").get("source")
    if error.get("source"):
        lines = error.get("source", {}).get("lines")
        columns = error.get("source", {}).get("columns")
        if lines[0] == lines[1]:
            lines = lines[0]
            plural_lines = ""
        else:
            plural_lines = "s"
            lines = "-".join(["%s" % line for line in lines])
        if columns[0] == columns[1]:
            columns = columns[0]
            plural_columns = ""
        else:
            plural_columns = "s"
            columns = "-".join(["%s" % column for column in columns])
        error_str += " (line%s: %s, column%s: %s)" % (
            plural_lines, lines, plural_columns, columns)
    return error_str


class Interpreter:
    """A bridge to an underlying nodejs WhizzML interpreter.

    This class uses JSPyBridge to access and execute
    WhizzML's javascript implementation and allows interaction via
    Python constructs.

    """

    __WHIZZJS = require('../whizzml/whizzml-node.js')
    whizzml = globalThis.whizzml.user

    def __init__(self, username, api_key,
                 domain="https://bigml.io",
                 version="andromeda",
                 project=None,
                 organization=None):
        self._vm = Interpreter.whizzml.make_vm(
            username, api_key, domain, version, project, organization)

    def eval(self, code):
        error = list(Interpreter.whizzml.validate(
            code,
            list(Interpreter.whizzml.environment(self._vm).valueOf().keys())))
        if error:
            raise ValueError(prettify_error(error))
        self._vm = Interpreter.whizzml.run_and_register(
            self._vm, code)
        counter = 1
        time.sleep(get_exponential_wait(0.5, counter))
        while not Interpreter.whizzml.registered_vm():
            counter += 1
            time.sleep(get_exponential_wait(2 , counter))
        self._vm = Interpreter.whizzml.registered_vm()
        return self._result()

    def inputs(self, code):
        return list(Interpreter.whizzml.undefined_identifiers
            (self._vm, code).valueOf().keys())

    def outputs(self, code):
        return list(Interpreter.whizzml.defined_non_procedure_ids
            (code).valueOf().keys())

    def _result(self):
        error = Interpreter.whizzml.last_error(self._vm)
        if error:
            raise ValueError(prettify_error(error))
        else:
            return Interpreter.whizzml.last_value_str(self._vm, 80)
