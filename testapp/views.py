from django.shortcuts import render
from django.http import HttpResponse
from testapp.models import OdooModel
from testapp.odoo import authenticate_odoo_user
from testproject.settings import odoo


def sync_data_view(request):
    # # Get field information for the model
    # fields_info = odoo.env['account.move'].fields_get()
    #
    # # Print the field names
    # for field_name in fields_info:
    #     print(field_name)

    # record_ids = odoo.env['account.move'].search([])
    #
    # # Read data for all records
    # odoo_model_data = odoo.env['account.move'].read(record_ids, ['name', "invoice_partner_display_name", "date", "payment_state"])
    # print(odoo_model_data)
    # Save data in Django models
    # for data in odoo_model_data:
    #     OdooModel.objects.create(name=data['name'])
    # Prepare data for creating an invoice
    invoice_data = {
        # 'state': 'posted',  # throw an error
        'partner_id': 1,  # ID of the customer/partner
        'date': '2023-05-18',  # Invoice date
        'invoice_line_ids': [
            (0, 0, {
                'product_id': 1,  # ID of the product
                'name': 'Product Name',  # Name of the product
                'quantity': 2,  # Quantity
                'price_unit': 50.0,  # Unit price
                'account_id': 1,
            }),
        ],
        # Add other field values as needed
    }

    # Create an invoice in the Odoo model 'account.move'
    # new_invoice_id = odoo.env['account.move'].create(invoice_data)
    # # Post the invoice
    # odoo.env['account.move'].browse(new_invoice_id).post()
    # # Print the ID of the newly created invoice
    # print("New invoice ID:", new_invoice_id)

    # invoice = odoo.env['account.move'].browse([0])
    # print(invoice)
    # Update the invoice fields
    # invoice.write({
    #     'state': 'posted',  # Update the invoice date
    #     # 'payment_state': 'paid',  # Update the payment state
    #     # Update other fields as needed
    # })

    # Read data for all records
    record_ids = odoo.env['account.move'].search([])
    print("record_ids", record_ids)
    odoo_model_data = odoo.env['account.move'].read(record_ids, ['name', "invoice_partner_display_name", "date", "payment_state","state","auto_post","invoice_line_ids"])
    print(odoo_model_data)
    # Create the account move in the 'draft' state
    transaction_data = {
        'name': 'transaction name',
        'invoice_partner_display_name': 'partner display name',
        'date': '2023-01-01',
        'payment_state': 'paid',
        'state': 'draft',  # start in the 'draft' state
        'invoice_line_ids': [(0, 0, {
            'name': 'invoice line name',
            'quantity': 1,
            'price_unit': 100.0,
            'account_id': 1,
        })],
    }

    transaction_id = odoo.env['account.move'].create(transaction_data)
    # Print out the transaction_id
    print(f"transaction_id: {transaction_id}")

    # Check if the record was created successfully
    if not transaction_id:
        print("Record creation failed")
    else:
        # Post the move (change its state to 'posted')
        try:
            move = odoo.env['account.move'].browse(transaction_id)
            print(f"move: {move}")
            move.action_post()
        except Exception as e:
            print(f"Failed to post the record: {e}")
    return HttpResponse("Data synchronized successfully!")


def test_odoo_api_view(request):
    odoo_url = "http://fatima4.odoo.com"
    db_name = "fatima4"
    username = "fatima@softylus.com"
    password = "c69e2e6acc2e6ae990c71cbb1b9a4e7403b4087b"
    uid = authenticate_odoo_user(odoo_url, db_name, username, password)
    print(uid)
