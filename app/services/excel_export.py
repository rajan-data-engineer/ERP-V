# app/services/excel_export.py

import pandas as pd
from sqlmodel import Session, select


class ExcelExportService:

    @staticmethod
    def export_table(model, session: Session, file_path: str):
        rows = session.exec(select(model)).all()

        if not rows:
            return None

        df = pd.DataFrame([r.dict() for r in rows])
        df.to_excel(file_path, index=False)

        return file_path
