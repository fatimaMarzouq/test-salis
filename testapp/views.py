from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from testapp.models import OdooModel
from testproject.settings import odoo


def sync_data_view(request):
    # # Get field information for the model
    # fields_info = odoo.env['account.move'].fields_get()
    #
    # # Print the field names
    # for field_name in fields_info:
    #     print(field_name)

    record_ids = odoo.env['account.move'].search([])

    # Read data for all records
    odoo_model_data = odoo.env['account.move'].read(record_ids, ['name', "invoice_partner_display_name", "date", "payment_state"])
    print(odoo_model_data)
    # Save data in Django models
    # for data in odoo_model_data:
    #     OdooModel.objects.create(name=data['name'])
    return HttpResponse("Data synchronized successfully!")
