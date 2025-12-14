from sqlmodel import Session, select
from openpyxl import Workbook
from fastapi.responses import StreamingResponse
from io import BytesIO

class ExportService:

    @staticmethod
    def export_table(session: Session, model):
        data = session.exec(select(model)).all()
        wb = Workbook()
        ws = wb.active
        ws.title = "Export"

        if not data:
            ws.append(["No data"])
        else:
            # Header
            headers = data[0].dict().keys()
            ws.append(headers)

            # Rows
            for row in data:
                ws.append(list(row.dict().values()))

        stream = BytesIO()
        wb.save(stream)
        stream.seek(0)

        return StreamingResponse(
            stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=export.xlsx"},
        )
