from odoo import api, fields, models
 
class Partner(models.Model):
    _inherit = 'res.partner'
 

    no = fields.Char('No. KTP')
    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan'),
    ], string='Jenis Kelamin')
    nama_ayah = fields.Char('Nama Ayah')
    pekerjaan_ayah = fields.Char('Pekerjaan Ayah')
    tempat_lahir = fields.Char('Tempat Lahir')
    pendidikan = fields.Selection([
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('diploma', 'Diploma'),
        ('s1', 'S1'),
        ('s2', 'S2'),
        ('s3', 'S3'),
    ], string='Pendidikan')
    status_hubungan = fields.Selection([
        ('married', 'Married'),
        ('single', 'Single'),
        ('divorce', 'Divorce'),
    ], string='Status Hubungan')
    nama_ibu = fields.Char('Nama Ibu')
    pekerjaan_ibu = fields.Char('Pekerjaan Ibu')
    tanggal_lahir = fields.Date('Tanggal Lahir')
    golongan_darah = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ], string='Golongan Darah')
    ukuran_baju = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('4l', '4L'),
    ], string='Ukuran Baju')

    no_passpor = fields.Char('No Passpor')
    tanggal_berlaku = fields.Date('Tanggal Berlaku')
    imigrasi = fields.Char('Imigrasi')
    nama_passpor = fields.Char('Nama Passpor')
    tanggal_expired = fields.Date('Tanggal Expired')
    scan_passpor = fields.Binary(string='Scan Passpor', attachment=True)
    scan_buku_nikah = fields.Binary(string='Scan Buku Nikah', attachment=True)
    scan_ktp = fields.Binary(string='Scan KTP', attachment=True)
    scan_kartu_keluarga = fields.Binary(string='Scan Kartu Keluarga', attachment=True)



    airlines = fields.Boolean(string='Airlines', readonly=True)
    hotel = fields.Boolean(string='Hotel', readonly=True)



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
        return super(Partner, self).create(vals)

