// Copyright (c) 2025, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Backdate Setting", {
	refresh(frm) {
        set_date_field_value(frm);
	},
    backdate_doc(frm){
        set_date_field_value(frm);
    }
});



function set_date_field_value(frm){
	if (!frm.doc.backdate_doc) return;

	frappe.model.with_doctype(frm.doc.backdate_doc, () => {
		const fields = frappe.meta.get_docfields(frm.doc.backdate_doc);

		const date_fields = fields
			.filter(df => ["Date", "Datetime"].includes(df.fieldtype))
			.map(df => df.fieldname);

		if (!date_fields.includes("creation")) date_fields.push("creation");
		if (!date_fields.includes("modified")) date_fields.push("modified");

		const df = frm.fields_dict.date_field;
		if (df) {
			df.df.options = date_fields.join("\n");
			df.refresh();
		}

		if (!frm.doc.date_field && date_fields.includes("creation")) {
			frm.set_value("date_field", "creation");
		}
	});
}