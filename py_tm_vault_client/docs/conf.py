# -*- coding: utf-8 -*-

import datetime
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = u'Thought Machine Vault Client for Python'
year = datetime.datetime.now().year
copyright = u'%d Thought Machine' % year
author = u'Thought Machine'

# The short X.Y version
version = u'0.1.0'
# The full version, including alpha/beta/rc tags
release = u'0.1.0'


# -- General configuration ---------------------------------------------------

needs_sphinx = '2.3'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx_rtd_theme',
]

autodoc_mock_imports = ["dateutil", "requests", 'confluent_kafka']

templates_path = ['_templates']

source_suffix = ['.rst', '.md']

master_doc = 'index'

language = None

exclude_patterns = [u'_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'tmvault-client-pythondoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        'ThoughtMachineVaultClient.tex',
        u'Thought Machine Vault Client Documentation',
        u'Thought Machine',
        'manual'
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        'thoughtmachinevaultclient',
        u'Thought Machine Vault Client Documentation',
        [author],
        1
    )
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [

    (
        master_doc,
        'ThoughtMachineVaultClient',
        u'Thought Machine Vault Client Documentation',
        author,
        'ThoughtMachineVaultClient',
        'One line description of project.',
        'Miscellaneous'
    ),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

html_show_sourcelink = False

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
