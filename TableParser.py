from openpyxl import load_workbook

class TableParser:
    def __init__(self, config):
        self.config = config
        wb = load_workbook(config.table_path)
        ws = wb.active
        print(ws[config.reasons_location].fill)
        # wb.save(config.table_path)

    
    # def find_reasons(self, work):