import stripe
import csv


stripe.api_key = "pk_test_GPJYkcGIFtW7mRsAbbHsVnUG" # PLEASE CHANGE TO SECRET KEY ONCE IN PRIVATE REPO 


#Use Unix calculator such as http://www.aelius.com/njh/unixtime/ to determine unix time

# Gets all invoices from Stripe API for the month of May
# input start unix time as the value for "gte" and end unix time as value for "lte"
may_invoices = stripe.Invoice.all(date={"gte":1430434800, "lte":1433026800 }) 


num_of_invoices = len(may_invoices)
itemized_invoices = {}

# Function to determine invoice line items
def calc_invoices():
	for num in range(0, num_of_invoices):
		num_of_lineitems = len(may_invoices["data"][num]["lines"]["data"])
		invoice = []
		invoice_timestamp = may_invoices["data"][num]["date"]
		customer_id = may_invoices["data"][num]["customer"]
		subscription_amount = 0
		overage_charges = 0
		total = may_invoices["data"][num]["amount_due"]

		# need to iterate because invoice line items are in a list and there are not always overage charges
		for line in range(0, num_of_lineitems):
			if may_invoices["data"][num]["lines"]["data"][line].get("description", 0) == "overage charges":
				overage_charges = may_invoices["data"][num]["lines"]["data"][line]["amount"]
			else:
				subscription_amount = may_invoices["data"][num]["lines"]["data"][line]["amount"]

		invoice = [invoice_timestamp, customer_id, subscription_amount/100.00, overage_charges/100.00, total/100.00]
		itemized_invoices[num] = invoice
	return itemized_invoices

calc_invoices()

# Creates CSV file of month invoice data
col_header = ["invoice_timestamp", "customer_id", "subscription_amount", "overage_charges", "total"]

with open("mayinvoice.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(col_header)
   writer.writerows(itemized_invoices.values())