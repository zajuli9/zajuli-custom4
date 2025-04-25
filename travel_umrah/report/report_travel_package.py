from odoo import api, fields, models
from datetime import datetime

 
class TravelPackageXlsx(models.AbstractModel):
    _name = 'report.travel_umrah.report_travel'
    _inherit = 'report.report_xlsx.abstract'
 
    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('Manifest %s' % obj.sale_id.name)
        text_top_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'white', 'bg_color': '#b904bf', 'valign': 'vcenter', 'text_wrap': True})
        text_header_style = workbook.add_format({'font_size': 12, 'bold': True ,'font_color' : 'white', 'bg_color': '#b904bf', 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        text_style = workbook.add_format({'font_size': 12, 'valign': 'vcenter', 'text_wrap': True, 'align': 'center'})
        number_style = workbook.add_format({'num_format': '#,##0', 'font_size': 12, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True})
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy', 'font_size': 12, 'align': 'center'})


        sheet.merge_range(1, 3, 1, 3, "Manifest", text_top_style)
        sheet.write(1, 4, obj.ref)
        
        row = 3
        header = ['No', 'TITLE', 'GENDER', 'FULL NAME', 'TEMPAT LAHIR','TANGGAL LAHIR', 'NO. PASSPOR', 'PASSPOR ISSUED','PASSPOR EXPIRED','IMIGRASI','MAHROM','USIA','NIK','ORDER','ROOM TYPE','ROOM LEADER','NO. ROOM','ALAMAT']
        sheet.write_row(row, 0, header, text_header_style)

        no_list = []
        title = []
        gender = []
        full_name = []
        tempat_lahir = []
        tanggal_lahir = []
        no_passpor = []
        tanggal_berlaku = []
        tanggal_expired = []
        imigrasi = []
        mahrom = []
        umur = []
        no_nik = []
        sale_order_id = []
        tipe_kamar = []
        agent = []
        no_room = []
        alamat = []
 
        no = 1
        for x in obj.manifest_line_ids:
             no_list.append(no)
             title.append(x.title.name if x.title else '')
             gender.append(x.gender or '')
             full_name.append(x.nama_jamaah.name if x.nama_jamaah else '')
             tempat_lahir.append(x.nama_jamaah.tempat_lahir if x.nama_jamaah else '')
             tanggal_lahir.append(x.nama_jamaah.tanggal_lahir or '')
             no_passpor.append(x.nama_jamaah.no_passpor or '')
             tanggal_berlaku.append(x.nama_jamaah.tanggal_berlaku or '')
             tanggal_expired.append(x.nama_jamaah.tanggal_expired or '')
             imigrasi.append(x.nama_jamaah.imigrasi or '')
             mahrom.append(x.mahrom.name if x.mahrom.name else '')
             umur.append(x.umur or '')
             no_nik.append(x.nama_jamaah.no or '')
             sale_order_id.append(x.sale_order_id.name or '')
             tipe_kamar.append(x.tipe_kamar or '')
             agent.append(x.agent or '')
             no_room.append(x.no_room or '')
             alamat.append(x.nama_jamaah.city or '')
             no+=1
 
        row += 1
        sheet.write_column(row, 0, no_list, text_style)
        sheet.write_column(row, 1, title, text_style)
        sheet.write_column(row, 2, gender, text_style)
        sheet.write_column(row, 3, full_name, text_style)
        sheet.write_column(row, 4, tempat_lahir, text_style)
        sheet.write_column(row, 5, tanggal_lahir, date_format)
        sheet.write_column(row, 6, no_passpor, text_style)
        sheet.write_column(row, 7, tanggal_berlaku, date_format)
        sheet.write_column(row, 8, tanggal_expired, date_format)
        sheet.write_column(row, 9, imigrasi, text_style)
        sheet.write_column(row, 10, mahrom, text_style)
        sheet.write_column(row, 11, umur, text_style)
        sheet.write_column(row, 12, no_nik, text_style)
        sheet.write_column(row, 13, sale_order_id, text_style)
        sheet.write_column(row, 14, tipe_kamar, text_style)
        sheet.write_column(row, 15, agent, text_style)
        sheet.write_column(row, 16, no_room, text_style)
        sheet.write_column(row, 17, alamat, text_style)



        row2 = 8
        header2 = ['No','AIRLINE','DEPARTURE DATE','DEPARTURE CITY','ARRIVAL CITY']
        sheet.write_row(row2, 2, header2, text_header_style)
        no_list = []
        airline = []
        departure_date = []
        departure_city = []
        arrival_city = []

        no = 1
        for x in obj.airlines_line_ids:
             no_list.append(no)
             airline.append(x.airlines_id.name or '')
             departure_date.append(x.tanggal_berangkat_line or '')
             departure_city.append(x.kota_asal or '')
             arrival_city.append(x.kota_tujuan or '')
             no +=1

        row2 += 1
        sheet.write_column(row2, 2, no_list, text_style)
        sheet.write_column(row2, 3, airline, text_style)
        sheet.write_column(row2, 4, departure_date, date_format)
        sheet.write_column(row2, 5, departure_city, text_style)
        sheet.write_column(row2, 6, arrival_city, text_style)
