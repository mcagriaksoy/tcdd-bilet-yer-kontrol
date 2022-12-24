# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from flet import DataTable, DataColumn, DataRow, DataCell, Text, border, colors

def list2df(veriler:list) -> DataTable:
    anahtarlar = list(veriler[0].keys())
    kolonlar   = [DataColumn(Text(anahtar)) for anahtar in anahtarlar]

    return DataTable(
        border_radius     = 10,
        border            = border.all(2),
        vertical_lines    = border.BorderSide(3),
        horizontal_lines  = border.BorderSide(1),
        heading_row_color = colors.BLACK12,
        data_row_color    = {"hovered": "0x30FF0000"},
        divider_thickness = 0,
        data_row_height   = 85,

        columns = kolonlar,
        rows    = [
            DataRow(
                cells=[DataCell(Text(veri[anahtar])) for anahtar in anahtarlar]
            )
              for veri in veriler
        ]
    )