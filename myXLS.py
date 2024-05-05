#-------------------------------------------------------------------------------
# Name:        fast_openpyxl
# Created By: CAS
#-------------------------------------------------------------------------------
import openpyxl
import time, sys
from pprint import pprint
# ---------------------------------------------------------------------------
# read_xls_file and retunn list of sheets and dict of data
# return (status, )
# ---------------------------------------------------------------------------
excel_file = 'xxxxxxxx.xlsx'

##--------------------------------------------------------------------------------------------------------------------------------------
def fast_openpyxl(excel_file):
    ## return dict, each key will be sheet, and data of sheet in list[dict] format of that sheet, row 0 will be key element.
    ## len(list) -> number of rows or recoords.
##    start_time = time.time()
    try:
        workbook = openpyxl.load_workbook(excel_file, data_only=True,read_only=True)
        wb = {}
        for sheet in workbook.sheetnames:
            header = []
            sheet_list = []
            sheet_name = "sheet_" + sheet.replace(' ','_')
            sheet = workbook[sheet]
            for rowidx,row in enumerate(sheet.rows):
                new_entry = {}
                for colidx,cell in enumerate(row):
                    value = cell.value
                    if rowidx == 0:
                        if value is None: break ## no value at row 0, col 0
                        header.append(value)
                    else:
                        if value is None:
                            try: ## data must start from row 1 and col A
                                new_entry[header[colidx]] = ""
                            except IndexError:
                                return (1, "IndexError value None in input file: {} @sheet {}".format(excel_file, sheet_name))
                                break
                        else:
                            try:
                                new_entry[header[colidx]] = value
                            except IndexError:
                                return (1, "IndexError on value input file: {} @sheet {}".format(excel_file, sheet_name))
                                break
                if rowidx != 0:
                    sheet_list.append(new_entry)
                wb.setdefault(sheet_name, sheet_list)
    except IOError:
        return (1, "IOError on input file:%s" % excel_file)
##    print(f'{sys._getframe().f_code.co_name} Done! Completed in {round(time.time()-start_time,2)} seconds.')
    return (0, wb)

##--------------------------------------------------------------------------------------------------------------------------------------

##def main():
##    start_time = time.time()
##    print(fast_openpyxl(excel_file))
##    print(f'{sys._getframe().f_code.co_name} Done! Completed in {round(time.time()-start_time,2)} seconds.')
##    pass
##
##if __name__ == '__main__':
##    main()