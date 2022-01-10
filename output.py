import os
import fitz


class PdfOut:
    def __init__(self, panda, temp_path, current_path, type, airport, pub_date):
        self.panda = panda
        self.file_out = f"{airport}_{type}_{pub_date}.pdf"
        self.dir_in = temp_path
        self.dir_out = current_path
        self.writePDF()

    def writePDF(self):
        new_toc = []
        composite_pdf = fitz.open()
        for index, row in self.panda.iterrows():
            new_page = fitz.open(os.path.join(self.dir_in, row.File))
            composite_pdf.insert_pdf(new_page)
            new_page.close()
            new_toc.append((1, row.Title, index + 1))
        composite_pdf.set_toc(new_toc)
        composite_pdf.save(os.path.join(self.dir_out, self.file_out), deflate=True, garbage=3)
        composite_pdf.close()
