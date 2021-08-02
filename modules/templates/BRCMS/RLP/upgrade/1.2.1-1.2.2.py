# -*- coding: utf-8 -*-
#
# Database upgrade script
#
# RLPCM Template Version 1.2.1 => 1.2.2
#
# Execute in web2py folder after code upgrade like:
# python web2py.py -S eden -M -R applications/eden/modules/templates/BRCMS/RLP/upgrade/1.2.1-1.2.2.py
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
#aotable = s3db.br_assistance_offer

IMPORT_XSLT_FOLDER = os.path.join(request.folder, "static", "formats", "s3csv")
TEMPLATE_FOLDER = os.path.join(request.folder, "modules", "templates", "BRCMS")

# -----------------------------------------------------------------------------
# Deploy shelter types
#
if not failed:
    info("Deploy Shelter Types")

    # Import new templates
    stylesheet = os.path.join(IMPORT_XSLT_FOLDER, "cr", "shelter_type.xsl")
    filename = os.path.join(TEMPLATE_FOLDER, "RLP", "cr_shelter_type.csv")

    # Import, fail on any errors
    try:
        with open(filename, "r") as File:
            resource = s3db.resource("cr_shelter_type")
            resource.import_xml(File, format="csv", stylesheet=stylesheet)
    except:
        infoln("...failed")
        infoln(sys.exc_info()[1])
        failed = True
    else:
        if resource.error:
            infoln("...failed")
            infoln(resource.error)
            failed = True
        else:
            infoln("...done")

# -----------------------------------------------------------------------------
# Deploy shelter services
#
if not failed:
    info("Deploy Shelter Services")

    # Import new templates
    stylesheet = os.path.join(IMPORT_XSLT_FOLDER, "cr", "shelter_service.xsl")
    filename = os.path.join(TEMPLATE_FOLDER, "RLP", "cr_shelter_service.csv")

    # Import, fail on any errors
    try:
        with open(filename, "r") as File:
            resource = s3db.resource("cr_shelter_service")
            resource.import_xml(File, format="csv", stylesheet=stylesheet)
    except:
        infoln("...failed")
        infoln(sys.exc_info()[1])
        failed = True
    else:
        if resource.error:
            infoln("...failed")
            infoln(resource.error)
            failed = True
        else:
            infoln("...done")

# -----------------------------------------------------------------------------
# Deploy new CMS items
#
if not failed:
    info("Deploy new CMS items")

    # File and Stylesheet Paths
    stylesheet = os.path.join(IMPORT_XSLT_FOLDER, "cms", "post.xsl")
    filename = os.path.join(TEMPLATE_FOLDER, "RLP", "cms_post.csv")

    # Only import relevant CMS posts, do not update any existing ones
    def cms_post_duplicate(item):
        name = item.data.get("name")
        if name in ("OfferDetailsIntro",
                    ):
            S3Duplicate(noupdate=True)(item)
        else:
            item.skip = True

    # Import, fail on any errors
    try:
        with open(filename, "r") as File:
            resource = s3db.resource("cms_post")
            resource.configure(deduplicate = cms_post_duplicate)
            resource.import_xml(File,
                                format = "csv",
                                stylesheet = stylesheet,
                                )
    except:
        infoln("...failed")
        infoln(sys.exc_info()[1])
        failed = True
    else:
        if resource.error:
            infoln("...failed")
            infoln(resource.error)
            failed = True
        else:
            infoln("...done")

# -----------------------------------------------------------------------------
# Upgrade user roles
#
if not failed:
    info("Upgrade user roles")

    auth.s3_delete_role("CASE_MANAGER")

    bi = s3base.S3BulkImporter()
    filename = os.path.join(TEMPLATE_FOLDER, "RLP", "auth_roles.csv")

    with open(filename, "r") as File:
        try:
            bi.import_role(filename)
        except Exception as e:
            infoln("...failed")
            infoln(sys.exc_info()[1])
            failed = True
        else:
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
