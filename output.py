import os
import fitz

def combinePDF(airport,type,listing):
    file_out = f"{airport}_{type}_{listing['date']}.pdf"
    print(f"Combining relevant pdf's into {airport}_{type}_{listing['date']}.pdf")
    dir_in = os.path.join(os.getcwd(), "pdf_archive_raw")
    dir_out = os.path.join(os.getcwd(), "pdf_latest")
    new_toc = []
    composite_pdf = fitz.open()
    index = 1
    for file in listing['files']:
        new_page = fitz.open(os.path.join(dir_in, file['file']))
        composite_pdf.insert_pdf(new_page)
        new_page.close()
        new_toc.append((1, file['name'], index))
        index += 1
    composite_pdf.set_toc(new_toc)
    composite_pdf.save(os.path.join(dir_out,file_out), deflate=True, garbage=3)
    composite_pdf.close()



# class PdfOut:
#     def __init__(self, panda, temp_path, current_path, type, airport, pub_date):
#         self.panda = panda
#         self.file_out = f"{airport}_{type}_{pub_date}.pdf"
#         self.dir_in = temp_path
#         self.dir_out = current_path
#         self.writePDF()

#     def writePDF(self):
#         new_toc = []
#         composite_pdf = fitz.open()
#         for index, row in self.panda.iterrows():
#             new_page = fitz.open(os.path.join(self.dir_in, row.File))
#             composite_pdf.insert_pdf(new_page)
#             new_page.close()
#             new_toc.append((1, row.Title, index + 1))
#         composite_pdf.set_toc(new_toc)
#         composite_pdf.save(os.path.join(self.dir_out, self.file_out), deflate=True, garbage=3)
#         composite_pdf.close()
