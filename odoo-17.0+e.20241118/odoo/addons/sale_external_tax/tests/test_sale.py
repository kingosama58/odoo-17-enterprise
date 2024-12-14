# Part of Odoo. See LICENSE file for full copyright and licensing details.
from unittest.mock import patch

from odoo.tests import tagged
from odoo.addons.sale.tests.common import SaleCommon
from odoo import Command


@tagged('post_install', '-at_install')
class TestSaleExternalTaxesSale(SaleCommon):

    def test_01_send_locked_order(self):
        """ Ensure locked sale orders with external taxes can be sent without tax recomputation """
        order = self.env['sale.order'].create({
            'name': 'test',
            'partner_id': self.partner.id,
            'date_order': '2023-01-01',
            'order_line': [
                Command.create({
                    'product_id': self.consumable_product.id,
                    'price_unit': 100.0,
                }),
            ],
        })

        order.action_confirm()
        order.action_lock()

        def _get_and_set_external_taxes_on_eligible_records(self):
            self.order_line.write({'tax_id': [Command.clear()]})

        def _compute_is_tax_computed_externally(self):
            self.is_tax_computed_externally = True

        TaxMixin = self.env.registry['account.external.tax.mixin']
        with (
            patch.object(TaxMixin, '_get_and_set_external_taxes_on_eligible_records', _get_and_set_external_taxes_on_eligible_records),
            patch.object(TaxMixin, '_compute_is_tax_computed_externally', _compute_is_tax_computed_externally),
        ):
            order.action_quotation_send()
