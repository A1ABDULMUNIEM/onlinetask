from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_order_ids = fields.One2many('sale.order', 'partner_id')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one('res.partner')

    @api.model
    def create(self, values):
        order = super(SaleOrder, self).create(values)
        self._update_customer_metrics(order.partner_id)
        return order

    def write(self, values):
        res = super(SaleOrder, self).write(values)
        for order in self:
            self._update_customer_metrics(order.partner_id)
        return res

    def _update_customer_metrics(self, partner):
        customer_metrics = self.env['res.partner.customer.metrics'].search([('customer_id', '=', partner.id)], limit=1)
        if not customer_metrics:
            customer_metrics = self.env['res.partner.customer.metrics'].create({'customer_id': partner.id})

        customer_metrics._compute_sum()
        customer_metrics._compute_orders()

class CustomerMetrics(models.Model):
    _name='res.partner.customer.metrics'
    customer_id = fields.Many2one('res.partner')
    total_sales = fields.Float(compute='_compute_sum',store=1)
    order_count = fields.Integer(compute='_compute_orders', store=1)
    @api.depends('customer_id.sale_order_ids.amount_total')
    def _compute_sum(self):
        for rec in self:
            if rec.customer_id:
                total = 0
                for order in rec.customer_id.sale_order_ids:
                    total += order.amount_total
                rec.total_sales = total
            else:
                rec.total_sales = 0.0
    @api.depends('customer_id.sale_order_ids')
    def _compute_orders(self):
        for rec in self:
            rec.order_count = len(rec.customer_id.sale_order_ids)



    def get_top_customers(self):

        top_customers = self.search([], order='total_sales desc', limit=5)

        customer_data = []
        for customer in top_customers:
            customer_data.append({
                'customer_name': customer.customer_id.name,
                'total_sales': customer.total_sales,
                'order_count': customer.order_count
            })
        return customer_data

