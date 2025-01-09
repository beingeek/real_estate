import frappe


def setup():
	create_party_types()


def create_party_types():
	for party_type in ["Real Estate Investor", "Real Estate Contractor"]:
		if not frappe.db.exists("Party Type", party_type):
			party = frappe.new_doc("Party Type")
			party.party_type = party_type
			party.insert()
