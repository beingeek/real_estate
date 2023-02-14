frappe.listview_settings['Property Unit'] = {
	add_fields: ["booking_status"],
	get_indicator: function(doc) {
		if(doc.booking_status == "Booked") {
			return [__(doc.booking_status), "green", "booking_status,=," + doc.booking_status];
		} else if (doc.booking_status == "Available") {
			return [__(doc.booking_status), "blue", "booking_status,=," + doc.booking_status];
		}
	}
};
