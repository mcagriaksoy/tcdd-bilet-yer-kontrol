# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from flet import DataTable, DataColumn, DataRow, DataCell, Text, border, colors

def list2dt(veriler:list) -> DataTable:
    anahtarlar = list(veriler[0].keys())
    kolonlar   = [DataColumn(Text(anahtar)) for anahtar in anahtarlar]

    return DataTable(
        border            = border.all(2),
        border_radius     = 10,
        vertical_lines    = border.BorderSide(3),
        horizontal_lines  = border.BorderSide(1),
        heading_row_color = colors.BLACK12,
        divider_thickness = 1,
        data_row_height   = 85,

        columns = kolonlar,
        rows    = [
            DataRow(
                cells=[DataCell(Text(veri[anahtar])) for anahtar in anahtarlar]
            )
              for veri in veriler
        ]
    )