# Copyright (C) 2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import unittest

from pulp_deb.plugins.importers import importer
from pulp_deb.plugins.importers.importer import PackageImporter


class TestImporter(unittest.TestCase):
    def test_entry_point(self):
        ret = importer.entry_point()
        self.assertEqual(ret[0], PackageImporter)
        self.assertTrue(isinstance(ret[1], dict))
