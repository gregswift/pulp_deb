# -*- coding: utf-8 -*-
#
# Copyright © 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

"""
Contains constants that are global across the entire deb plugin. Eventually,
this will be pulled into a common dependency across all of the deb
support plugins (importers, distributors, extensions).
"""

# -- ids ----------------------------------------------------------------------

# ID used to refer to the deb importer
IMPORTER_TYPE_ID = 'deb_importer'

# ID used to refer to the deb importer instance on a repository
IMPORTER_ID = IMPORTER_TYPE_ID

# ID used to refer to the deb distributor
DISTRIBUTOR_TYPE_ID = 'deb_distributor'

# ID used to refer to the deb distributor instance on a repository
DISTRIBUTOR_ID = 'deb_distributor'

# ID of the deb module type definition (must match what's in deb.json)
TYPE_DEB_MODULE = 'deb_module'

# Used as a note on a repository to indicate it is a deb repository
REPO_NOTE_KEY = '_repo-type' # needs to be standard across extensions
REPO_NOTE_DEB = 'deb-repo'

# -- storage and hosting ------------------------------------------------------

# Name of the hosted file describing the contents of the repository
REPO_METADATA_FILENAME = 'modules.json'

# File name inside of a module where its metadata is found
MODULE_METADATA_FILENAME = 'metadata.json'

# Location in the repository where a module will be hosted
# Substitutions: author first character, author
HOSTED_MODULE_FILE_RELATIVE_PATH = 'system/releases/%s/%s/'

# Name template for a module
# Substitutions: author, name, version
MODULE_FILENAME = '%s-%s-%s.tar.gz'

# Location in Pulp where modules will be stored (the filename includes all
# of the uniqueness of the module, so we can keep this flat)
# Substitutions: filename
STORAGE_MODULE_RELATIVE_PATH = '%s'

# -- progress states ----------------------------------------------------------

STATE_NOT_STARTED = 'not-started'
STATE_RUNNING = 'running'
STATE_SUCCESS = 'success'
STATE_FAILED = 'failed'
STATE_SKIPPED = 'skipped'

COMPLETE_STATES = (STATE_SUCCESS, STATE_FAILED, STATE_SKIPPED)

# -- importer configuration keys ----------------------------------------------

# Location from which to sync modules
CONFIG_URL = 'url'
CONFIG_PKG = 'packages'

# List of queries to run on the feed
CONFIG_QUERIES = 'queries'

# Whether or not to remove modules that were previously synchronized but were
# not on a subsequent sync
CONFIG_REMOVE_MISSING = 'remove_missing'
DEFAULT_REMOVE_MISSING = False

# -- distributor configuration keys -------------------------------------------

# Controls if modules will be served insecurely or not
CONFIG_SERVE_INSECURE = 'serve_https'
DEFAULT_SERVE_INSECURE = True

# Local directory the web server will serve for HTTP repositories
CONFIG_HTTP_DIR = 'http_dir'
DEFAULT_HTTP_DIR = '/var/www/pulp_deb/http/repos'

# Local directory the web server will serve for HTTPS repositories
CONFIG_HTTPS_DIR = 'https_dir'
DEFAULT_HTTPS_DIR = '/var/www/pulp_deb/https/repos'