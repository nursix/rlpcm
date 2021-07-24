# -*- coding: utf-8 -*-
#
# Database upgrade script
#
# RLPCM Template Version 1.1.2 => 1.1.3
#
# Execute in web2py folder after code upgrade like:
# python web2py.py -S eden -M -R applications/eden/modules/templates/BRCMS/RLP/upgrade/1.1.2-1.1.3.py
#
import sys
from uuid import uuid4

#from gluon.storage import Storage
#from gluon.tools import callback
from s3 import S3Duplicate

# Override auth (disables all permission checks)
auth.override = True

# Failed-flag
failed = False

# Info
def info(msg):
    sys.stderr.write("%s" % msg)
def infoln(msg):
    sys.stderr.write("%s\n" % msg)

# Load models for tables
#ftable = s3db.org_facility

IMPORT_XSLT_FOLDER = os.path.join(request.folder, "static", "formats", "s3csv")
TEMPLATE_FOLDER = os.path.join(request.folder, "modules", "templates", "BRCMS")

# -----------------------------------------------------------------------------
# Deploy task to update overview
#
if not failed:
    info("Deploy task to update overview")

    task_id = current.s3task.schedule_task("settings_task",
                                           ["overview_stats_update"],
                                           {},
                                           repeats = 0,
                                           period = 300,
                                           timeout = 60,
                                           )
    if task_id:
        infoln("...done (task ID %s)" % task_id)
    else:
        failed = True
        infoln("failed!")

# -----------------------------------------------------------------------------
# Initialize overview data
#
if not failed:
    info("Initialize overview data")

    from templates.BRCMS.RLP.helpers import OverviewData
    OverviewData.update_data()

    infoln("...done")

# -----------------------------------------------------------------------------
# Finishing up
#
if failed:
    db.rollback()
    infoln("UPGRADE FAILED - Action rolled back.")
else:
    db.commit()
    infoln("UPGRADE SUCCESSFUL.")
