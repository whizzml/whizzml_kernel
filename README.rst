whizzml_kernel
==============

``whizzml_kernel`` is a simple Jupyter kernel that allows you to run WhizzML
code in a Jupyter Notebook.

Installation
------------
 ''
Node.js and npm are needed for the install and development process to work
properly. Detailed information for that can be found `here<https://docs.npmjs.com/downloading-and-installing-node-js-and-npm>`_. The rest of dependencies will automatically
be installed when installing ``whizzml_kernel`` from PyPI::

    pip install whizzml_kernel
    python -m whizzml_kernel.install


WhizzML credentials
-------------------

In order to access BigML using WhizzML, you'll need to provide your
credentials. Currently, the credentials are extracted from the existing
environment variables: BIGML_USERNAME, BIGML_API_KEY, BIGML_DOMAIN,
BIGML_API_VERSION, BIGML_PROJECT and BIGML_ORGANIZATION. The first two are
mandatory, while the rest can be missing. If so, BIGML_DOMAIN will be
set to https://bigml.io, the BIGML_API_VERSION will be set to the latest
version and no project or organization will be used. In order to set or
change those, you'll need to use the ``%env`` magic command, as you would
using the Python kernel.

Using the WhizzML kernel
------------------------
**Notebook**: The *New* menu in the notebook should show an option for a WhizzML notebook.

**Console frontends**: To use it with the console frontends, add ``--kernel whizzml`` to
their command line arguments.

The goal of this kernel is providing a REPL to use `WhizzML<https://bigml.com/whizzml>`_.
As an example, you can try basic WhizzML operations, like defining a variable:

.. image:: docs/imgs/variable_def.png
   :alt: WhizzML variable definition
   :align: center

defining a function:

.. image:: docs/imgs/function_def.png
   :alt: WhizzML function definition
   :align: center

calling the function on two numbers:

.. image:: docs/imgs/function_call.png
   :alt: Calling a WhizzML function
   :align: center

creating a source in BigML from some data:

.. image:: docs/imgs/source_creation.png
   :alt: Creating a source with WhizzML
   :align: center

Summarizing and storing your WhizzML
------------------------------------

Some magics have been added to the currently available ``Python`` magics as
utilities that can help you store your WhizzML code and create a script from
it. The steps to do so are:

- Saving the notebook, so that the corresponding ``.ipynb`` file contains
  the current version of the code.
- Using the ``%wstore`` magic command in a separated input cell. The command
  will call ``nbconvert`` to extract from the stored notebook the WhizzML code
  and will create a ``.whizzml`` file with it. After that, a new cell will be
  added to your notebook containing the ``%%wscript`` magic command and the
  JSON needed to define the name, description, inputs and outputs of the
  script. Inputs and outputs will be pre-populated by analizing the WhizzML
  variables, but their type and defaults should be modified at will.
- Running the ``%%wscript`` command with the correctly formatted JSON will
  create a script from the code and the metadata.


If you want to see the WhizzML code retrieved from your input cells, you can
use the magic command ``%wsource``, that will output that for you.

Also, if you want your environment (credentials, stored WhizzML code, etc.) to
be removed, you can use ``%wreset`` that will clear all the stored information
without affecting the code in the input cells of your notebook.
