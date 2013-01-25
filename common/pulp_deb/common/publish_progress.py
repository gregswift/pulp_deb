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
Contains classes and functions related to tracking the progress of a package
distributor.
"""

from pulp_deb.common import reporting
from pulp_deb.common.constants import STATE_NOT_STARTED, STATE_SUCCESS


class PublishProgressReport(object):
    """
    Used to carry the state of the publish run as it proceeds. This object is used
    to update the on going progress in Pulp at appropriate intervals through
    the update_progress call. Once the publish is finished, this object should
    be used to produce the final report to return to Pulp to describe the
    result of the operation.
    """

    @classmethod
    def from_progress_dict(cls, report):
        """
        Parses the output from the build_progress_report method into an instance
        of this class. The intention is to use this client-side to reconstruct
        the instance as it is retrieved from the server.

        The build_final_report call on instances returned from this call will
        not function as it requires the server-side conduit to be provided.
        Additionally, any exceptions and tracebacks will be a text representation
        instead of formal objects.

        :param report: progress report retrieved from the server's task
        :type  report: dict
        :return: instance populated with the state in the report
        :rtype:  PublishProgressReport
        """

        r = cls(None)

        m = report['packages']
        r.packages_state = m['state']
        r.packages_execution_time = m['execution_time']
        r.packages_total_count = m['total_count']
        r.packages_finished_count = m['finished_count']
        r.packages_error_count = m['error_count']
        r.packages_individual_errors = m['individual_errors']
        r.packages_error_message = m['error_message']
        r.packages_exception = m['error']
        r.packages_traceback = m['traceback']

        m = report['metadata']
        r.metadata_state = m['state']
        r.metadata_execution_time = m['execution_time']
        r.metadata_error_message = m['error_message']
        r.metadata_exception = m['error']
        r.metadata_traceback = m['traceback']

        m = report['publishing']
        r.publish_http = m['http']
        r.publish_https = m['https']

        return r

    def __init__(self, conduit):
        self.conduit = conduit

        # Modules symlink step
        self.packages_state = STATE_NOT_STARTED
        self.packages_execution_time = None
        self.packages_total_count = None
        self.packages_finished_count = None
        self.packages_error_count = None
        self.packages_individual_errors = None # mapping of package to its error
        self.packages_error_message = None # overall execution error
        self.packages_exception = None
        self.packages_traceback = None

        # Metadata generation
        self.metadata_state = STATE_NOT_STARTED
        self.metadata_execution_time = None
        self.metadata_error_message = None
        self.metadata_exception = None
        self.metadata_traceback = None

        # Publishing
        self.publish_http = STATE_NOT_STARTED
        self.publish_https = STATE_NOT_STARTED

    def update_progress(self):
        """
        Sends the current state of the progress report to Pulp.
        """
        report = self.build_progress_report()
        self.conduit.set_progress(report)

    def build_final_report(self):
        """
        Assembles the final report to return to Pulp at the end of the run.

        :return: report to return to Pulp at the end of the publish call
        :rtype:  pulp.plugins.model.PublishReport
        """

        # Report fields
        total_execution_time = -1
        if self.metadata_execution_time is not None and self.packages_execution_time is not None:
            total_execution_time = self.metadata_execution_time + self.packages_execution_time

        summary = {
            'total_execution_time' : total_execution_time
        }

        details = {} # intentionally empty; not sure what to put in here

        # Determine if the report was successful or failed
        all_step_states = (self.metadata_state, self.packages_state)
        unsuccessful_steps = [s for s in all_step_states if s != STATE_SUCCESS]

        if len(unsuccessful_steps) == 0:
            report = self.conduit.build_success_report(summary, details)
        else:
            report = self.conduit.build_failure_report(summary, details)

        return report

    def build_progress_report(self):
        """
        Returns the actual report that should be sent to Pulp as the current
        progress of the publish.

        :return: description of the current state of the publish
        :rtype:  dict
        """

        report = {
            'packages' : self._packages_section(),
            'metadata' : self._metadata_section(),
            'publishing' : self._publishing_section(),
        }
        return report

    def add_failed_package(self, unit, traceback):
        """
        Updates the progress report that a package failed to be built to the
        repository.

        :param unit: Pulp representation of the package
        :type  unit: pulp.plugins.model.AssociatedUnit
        """
        self.packages_error_count += 1
        self.packages_individual_errors = self.packages_individual_errors or {}
        error_key = '%s-%s-%s' % (unit.unit_key['name'], unit.unit_key['version'], unit.unit_key['author'])
        self.packages_individual_errors[error_key] = reporting.format_traceback(traceback)

# -- report creation methods ----------------------------------------------

    def _packages_section(self):
        packages_report = {
            'state' : self.packages_state,
            'execution_time' : self.packages_execution_time,
            'total_count' : self.packages_total_count,
            'finished_count' : self.packages_finished_count,
            'error_count' : self.packages_error_count,
            'individual_errors' : self.packages_individual_errors,
            'error_message' : self.packages_error_message,
            'error' : reporting.format_exception(self.packages_exception),
            'traceback' : reporting.format_traceback(self.packages_traceback),
        }
        return packages_report

    def _metadata_section(self):
        metadata_report = {
            'state' : self.metadata_state,
            'execution_time' : self.metadata_execution_time,
            'error_message' : self.metadata_error_message,
            'error' : reporting.format_exception(self.metadata_exception),
            'traceback' : reporting.format_traceback(self.metadata_traceback),
            }
        return metadata_report

    def _publishing_section(self):
        publishing_report = {
            'http' : self.publish_http,
            'https' : self.publish_https,
        }
        return publishing_report