# Copyright (c) 2025, DAS and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import today, getdate
from frappe.model.document import Document

class BackdateSetting(Document):
	pass

def _get_setting(doctype):
    return frappe.get_all(
        "Backdate Setting",
        filters={"backdate_doc": doctype},
        fields=["date_field", "max_days", "block_create", "block_validate"],
        limit=1
    )

def _check(doc, mode):
    setting = _get_setting(doc.doctype)
    if not setting:
        return

    setting = setting[0]
    date_field = setting.date_field
    max_days = setting.max_days

    doc_date = doc.get(date_field)
    if not doc_date:
        return

    diff = (getdate(today()) - getdate(doc_date)).days

    if mode == "create" and setting.block_create:
        if diff > max_days:
            frappe.throw(f"Tanggal {doc_date} melebihi batas backdate {max_days} hari")

    if mode == "validate" and setting.block_validate:
        if diff > max_days:
            frappe.throw(f"Tanggal {doc_date} melebihi batas backdate {max_days} hari")

def check_backdate_create(doc, method):
    _check(doc, "create")

def check_backdate_validate(doc, method):
    _check(doc, "validate")
