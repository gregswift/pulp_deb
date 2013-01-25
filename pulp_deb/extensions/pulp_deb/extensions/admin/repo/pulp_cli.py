# -*- coding: utf-8 -*-
#
# Copyright © 2012 Bouvet ASA
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.


from pulp.client.commands.repo import cudl as base_cudl, sync_publish, upload
from pulp.client.extensions.decorator import priority
from pulp.client.upload.manager import UploadManager

from pulp_deb.extensions.admin import structure
from pulp_deb.extensions.admin.repo import (cudl, copy_package, packages,
        publish_schedules, remove, status, sync_schedules)


@priority()
def initialize(context):
    structure.ensure_repo_structure(context.cli)

    renderer = status.StatusRenderer(context)

    repo_section = structure.repo_section(context.cli)
    repo_section.add_command(cudl.CreateRepositoryCommand(context))
    repo_section.add_command(cudl.UpdateRepositoryCommand(context))
    repo_section.add_command(base_cudl.DeleteRepositoryCommand(context))
    repo_section.add_command(cudl.ListRepositoriesCommand(context))
    repo_section.add_command(cudl.SearchRepositoriesCommand(context))

    repo_section.add_command(packages.PackagesCommand(context))
    repo_section.add_command(copy_package.PackageCopyCommand(context))

    sync_section = structure.repo_sync_section(context.cli)
    sync_section.add_command(sync_publish.RunSyncRepositoryCommand(context, renderer))
    sync_section.add_command(sync_publish.SyncStatusCommand(context, renderer))

    sync_schedules_section = structure.repo_sync_schedules_section(context.cli)
    sync_schedules_section.add_command(sync_schedules.CreateScheduleCommand(context))
    sync_schedules_section.add_command(sync_schedules.UpdateScheduleCommand(context))
    sync_schedules_section.add_command(sync_schedules.DeleteScheduleCommand(context))
    sync_schedules_section.add_command(sync_schedules.ListScheduleCommand(context))
    sync_schedules_section.add_command(sync_schedules.NextRunCommand(context))


def __upload_manager(context):
    """
    Instantiates and configures the upload manager. The context is used to
    access any necessary configuration.

    :return: initialized and ready to run upload manager instance
    :rtype:  pulp.client.upload.manager.UploadManager
    """
    upload_working_dir = context.config['deb']['upload_working_dir']
    upload_working_dir = os.path.expanduser(upload_working_dir)
    chunk_size = int(context.config['deb']['upload_chunk_size'])
    upload_manager = UploadManager(upload_working_dir, context.server, chunk_size)
    upload_manager.initialize()
    return upload_manager
