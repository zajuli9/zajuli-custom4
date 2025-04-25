from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import date




#transaction
class TransactionTravelPackage(models.Model):
    _name = 'transaction.travel.package'
    _description = 'Transaction Travel Package'

    @api.depends('ref', 'sale_id')
    def _compute_display_name(self):
        for account in self:
            account.display_name = f"{account.ref} - {account.sale_id.name}"


    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('seq_transaction.travel.package')
        return super(TransactionTravelPackage, self).create(vals)


    ref = fields.Char(string='Kode Travel', readonly=True, default='/')
    sale_id = fields.Many2one('product.product', string='Sale', help="Pilih Produk")
    tanggal_berangkat = fields.Date('Tanggal Berangkat')
    tanggal_kembali = fields.Date('Tanggal Kembali')
    quota = fields.Integer('Quota')
    remaining_quota = fields.Integer('Remaining Quota', readonly=True)
    quota_progress = fields.Integer(string="Quota Progress", compute='_compute_quota_progress')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done')], string='Status', readonly=True, default='draft')
    total_cost = fields.Float(string='Total Cost', compute='_compute_total_cost', store=True, readonly=True)
    mahrom = fields.Many2one('manifest.line',string="Mahrom")

    product_id = fields.Many2one('product.product',string="Package")
    
    package_line_ids = fields.One2many(
        'hpp.line', 'parent_id', string="HPP Lines", compute='_compute_package_lines', store=True
    )

   


    hotel_line_ids = fields.One2many('hotel.line', 'travel_package_id')
    airlines_line_ids = fields.One2many('airlines.line', 'travel_package_id')
    schedule_line_ids = fields.One2many('schedule.line', 'travel_package_id')
    manifest_line_ids = fields.One2many('manifest.line', 'travel_package_id', readonly=True)

    sale_order_line_ids = fields.One2many('sale.order', 'travel_package_id')


    @api.depends('product_id')
    def _compute_package_lines(self):
        for record in self:
            lines = []
            if record.product_id and record.product_id.bom_ids:
                for bom in record.product_id.bom_ids:
                    for line in bom.bom_line_ids:
                        lines.append((0, 0, {
                            'product_id': line.product_id.id,
                            'product_qty': line.product_qty,
                            'product_uom_id': line.product_uom_id.id,
                            'standard_price': line.standard_price,
                            'subtotal': line.product_qty * line.standard_price,
                        }))
            record.package_line_ids = lines
            #  print("====================",item.product_id.name)
            #  print("====================",item.product_qty)
            #  print("====================",item.standard_price)


    @api.depends('package_line_ids.subtotal')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(record.package_line_ids.mapped('subtotal'))

    

    @api.onchange('quota')
    def _onchange_quota(self):
        if self.quota:
            self.remaining_quota = self.quota

    def action_confirm(self):
        self.write({'state': 'confirm'})
      
    def action_cancel(self):
        self.write({'state': 'draft'})
      
    def action_close(self):
        self.write({'state': 'done'}) 

    @api.depends('quota', 'manifest_line_ids')
    def _compute_quota_progress(self):
        """Menghitung persentase pemakaian kuota"""
        for record in self:
            total_manifest = len(record.manifest_line_ids)
            record.remaining_quota = max(record.quota - total_manifest, 0)
            if record.quota > 0:
                record.quota_progress = ((total_manifest / record.quota) * 100)
            else:
                record.quota_progress = 0

    def action_update_jamaah(self):
        """Tombol Update Jamaah akan mengambil manifest dari Sale Order"""
        for package in self:
            sale_orders = self.env['sale.order'].search([('travel_package', '=', package.id), ('state', '=', 'sale')])
            all_manifest_lines = sale_orders.mapped('manifest_line_ids')
            package.write({
                'manifest_line_ids': [(5, 0, 0)] + [(4, manifest.id) for manifest in all_manifest_lines]
            })
            package._compute_quota_progress()
    
    def action_print_travel_package(self):
        return self.env.ref('travel_umrah.report_travel_package_action').report_action(self)

class HppLine(models.Model):
    _name = 'hpp.line'
    _description = 'Hpp Line'

    parent_id = fields.Many2one('transaction.travel.package', string="Parent", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product")
    product_qty = fields.Float(string="Quantity")
    product_uom_id = fields.Many2one('uom.uom', string="Unit of Measure")
    standard_price = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal')
        
    


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    # One2many ke mrp.bom.line (sudah ada di default Odoo)
    bom_line_ids = fields.One2many(
        'mrp.bom.line', 'bom_id'
    )   

    total_cost = fields.Float(
        string='Total Cost',
        compute='_compute_total_cost',
        store=True,
        readonly=True
    )

    @api.depends('bom_line_ids.subtotal')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(record.bom_line_ids.mapped('subtotal'))

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    standard_price = fields.Float(string='Standard Price', compute='_compute_standard_price', store=True, readonly=True)
    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
        readonly=True
    )

    @api.depends('product_qty', 'standard_price')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = (record.product_qty or 0.0) * (record.standard_price or 0.0)

    @api.depends('product_id')
    def _compute_standard_price(self):
        for record in self:
            record.standard_price = float(record.product_id.standard_price or 0.0)



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_print_custom_manifest(self):
        return self.env.ref('travel_umrah.action_print_custom').report_action(self)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def teswidget(self):
        print("=========================",self.invoice_payments_widget["content"])

    def action_print_custom_invoice(self):
        return self.env.ref('travel_umrah.action_print_invoice').report_action(self)
    
    
class HotelLine(models.Model):
    _name = 'hotel.line'
    _description = 'Hotel Line'

    travel_package_id = fields.Many2one('transaction.travel.package', string="Travel Package")
    hotel_id = fields.Many2one('res.partner', string='Nama Hotel')
    check_in_hotel = fields.Date('Check In Hotel')
    check_out_hotel = fields.Date('Check Out Hotel')
    kota = fields.Char(string="Kota", related='hotel_id.city', store=True)

class AirlinesLine(models.Model):
    _name = 'airlines.line'

    travel_package_id = fields.Many2one('transaction.travel.package', string="Travel Package")
    airlines_id = fields.Many2one('res.partner', "Nama Airline")
    tanggal_berangkat_line = fields.Date('Tanggal Berangkat')
    kota_asal = fields.Char('Kota Asal')
    kota_tujuan = fields.Char('Kota Tujuan')

class ScheduleLine(models.Model):
    _name = 'schedule.line'
    _description = 'Schedule Line'

    travel_package_id = fields.Many2one('transaction.travel.package', string="Travel Package")
    kegiatan = fields.Char('Nama Kegiatan')
    tanggal_kegiatan = fields.Date('Tanggal Kegiatan')

    
class ManifestLine(models.Model):
    _name = 'manifest.line'
    _description = 'Manifest Line'

    travel_package_id = fields.Many2one('transaction.travel.package', string="Travel Package")
    title = fields.Many2one('res.partner.title', readonly=True, store=True, related='nama_jamaah.title')
    nama_passpor = fields.Char(related='nama_jamaah.nama_passpor', store=True, string="Nama Passpor", readonly=True)
    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ], string='Jenis Kelamin', related='nama_jamaah.gender')
    no = fields.Char(related='nama_jamaah.no',string="No. KTP", store=True, readonly=True)
    no_passpor = fields.Char(related='nama_jamaah.no_passpor', store=True, string="No. Passpor", readonly=True)
    tanggal_lahir = fields.Date(related='nama_jamaah.tanggal_lahir', store=True, string="Tanggal Lahir", readonly=True)
    tempat_lahir = fields.Char(related='nama_jamaah.tempat_lahir', store=True, string="Tempat Lahir", readonly=True)
    tanggal_berlaku = fields.Date(related='nama_jamaah.tanggal_berlaku', store=True, string="Tanggal Berlaku", readonly=True)
    tanggal_expired = fields.Date(related='nama_jamaah.tanggal_expired', store=True, string="Tanggal Expired", readonly=True)
    imigrasi = fields.Char(related='nama_jamaah.imigrasi', store=True, string="Imigrasi", readonly=True)
    tipe_kamar = fields.Selection([
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quad', 'Quad'),
        ],string="Tipe Kamar")
    umur = fields.Char(string='Umur', compute='_compute_age', store=True)
    mahrom = fields.Many2one('res.partner','Mahrom')
    agent = fields.Char(related='nama_jamaah.create_uid.name', string="Agent")
    no_room = fields.Char('No Room')

    sale_order_id = fields.Many2one('sale.order', string="Sales Order")
    nama_jamaah = fields.Many2one('res.partner','Nama Jamaah')
    note = fields.Char('Notes')


    scan_passpor = fields.Binary(string='Scan Passpor', attachment=True)
    scan_buku_nikah = fields.Binary(string='Scan Buku Nikah', attachment=True)
    scan_ktp = fields.Binary(string='Scan KTP', attachment=True)
    scan_kartu_keluarga = fields.Binary(string='Scan Kartu Keluarga', attachment=True)
    
    file_name_passpor = fields.Char(string='Nama Dokumen', required=True)
    file_name_ktp = fields.Char(string='Nama Dokumen', required=True)
    file_name_buku_nikah = fields.Char(string='Nama Dokumen', required=True)
    file_name_kartu_keluarga = fields.Char(string='Nama Dokumen', required=True)
    file_name = fields.Char(string='Nama File')

    @api.model
    def create(self, vals):
        vals['file_name_passpor'] = vals.get('file_name', 'New Document')
        vals['file_name_ktp'] = vals.get('file_name', 'New Document')
        vals['file_name_buku_nikah'] = vals.get('file_name', 'New Document')
        vals['file_name_kartu_keluarga'] = vals.get('file_name', 'New Document')
        return super(ManifestLine, self).create(vals)


    @api.depends('tanggal_lahir')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.tanggal_lahir:
                birth_date = record.tanggal_lahir
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.umur = f"{age}"
            else:
                record.umur = "N/A"  # Jika tidak ada tanggal lahir

    

    