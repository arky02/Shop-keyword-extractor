import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
a = ["a","v","d","s","f","g","d","s","f","d"]
b = ["d","d","f"]
sheet.append(a)
sheet.append(b)
wb.save('keyword_list.xlsx')