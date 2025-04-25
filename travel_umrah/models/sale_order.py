from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    travel_package = fields.Many2one('transaction.travel.package', string='Paket Perjalanan', domain=[('state', '=', 'confirm')])
   

    manifest_line_ids = fields.One2many('manifest.line', 'sale_order_id', string="Manifest Lines")

    travel_package_id = fields.Many2one('transaction.travel.package', string="Travel Package")
  


    # @api.depends("travel_package")    
    # @api.onchange("travel_package")
    # def _compute_bom_lines(self):
    #     """Mengisi Order Lines dari BoM saat memilih Travel Package"""
    #     for record in self:
    #         record.order_line = [(5, 0, 0)]  # Hapus data lama
    #         if record.travel_package:
                
    #             bom = self.env['product.product'].search([
    #                 ('name', '=', record.travel_package.sale_id.name)
                    
    #             ], limit=1)
                

    #             if bom:
    #                 lines = []
    #                 for line in bom:
    #                     lines.append((0, 0, {
    #                          # Ada di sale.order.line
    #                         'product_id': line.id,
    #                         'product_uom_qty': 1,
    #                         'price_unit': line.list_price,
    #                         'order_id': record.id,  # Hubungkan ke order
    #                     }))
    #                 record.order_line = lines  # Mengisi One2many order_line

    @api.onchange('travel_package')
    def _onchange_(self):
        """Mengisi Order Lines dari BoM saat memilih Travel Package"""
        for record in self:
            record.order_line = [(5, 0, 0)]  # Hapus data lama
            if record.travel_package:
                
                bom = self.env['product.product'].search([
                    ('name', '=', record.travel_package.sale_id.name)
                    
                ], limit=1)
                

                if bom:
                    lines = []
                    for line in bom:
                        lines.append((0, 0, {
                             # Ada di sale.order.line
                            'product_id': line.id,
                            'product_uom_qty': 1,
                            'price_unit': line.list_price,
                            'order_id': record.id,  # Hubungkan ke order
                        }))
                    record.order_line = lines  # Mengisi One2many order_line