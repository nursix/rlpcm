# -*- coding: utf-8 -*-
#
# Database upgrade script
#
# RLPCM Template Version 1.2.2 => 1.2.3
#
# Execute in web2py folder after code upgrade like:
# python web2py.py -S eden -M -R applications/eden/modules/templates/BRCMS/RLP/upgrade/1.2.2-1.2.3.py
#
import sys
from uuid import uuid4

#from gluon.storage import Storage
#from gluon.tools import callback
#from s3 import S3Duplicate

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
ltable = s3db.gis_location

IMPORT_XSLT_FOLDER = os.path.join(request.folder, "static", "formats", "s3csv")
TEMPLATE_FOLDER = os.path.join(request.folder, "modules", "templates", "BRCMS")

# -----------------------------------------------------------------------------
# Remove default owner group of locations
#
if not failed:
    info("Remove default owner group of locations")

    query = (ltable.owned_by_group != None) & \
            (ltable.deleted == False)
    updated = db(query).update(owned_by_group=None)

    infoln("...done (%s records updated)" % updated)

# -----------------------------------------------------------------------------
# Finishing up
#
if failed:
    db.rollback()
    infoln("UPGRADE FAILED - Action rolled back.")
else:
    db.commit()
    infoln("UPGRADE SUCCESSFUL.")
