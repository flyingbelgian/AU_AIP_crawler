import os, fitz

# ### ONLY FOR TESTING
# import parser
# dap_data = parser.DAPdata("20211202_DAP_169.html", "20211202", "YORG")

class PdfOut:
    def __init__(self,panda,temp_path,current_path,type,airport,pub_date):
        self.files = panda['File'].to_list()
        self.bookmarks = panda['Title'].to_list()
        self.file_out = f"{type}_{airport}_{pub_date}.pdf"
        self.dir_in = temp_path
        self.dir_out = current_path
        self.writePDF()

    def writePDF(self):
        # Combine individual pdfs into single merged pdf
        composite_pdf = fitz.open()
        for f in self.files:
            new_page = fitz.open(os.path.join(self.dir_in, f))
            composite_pdf.insert_pdf(new_page)
            new_page.close()
        # Generate and implement ToC (bookmarks)
        new_toc = []
        page_count = 1
        for item in self.bookmarks:
            entry = [1, item, page_count]
            new_toc.append(entry)
            page_count += 1
        composite_pdf.set_toc(new_toc)
        # Write final pdf to disk
        composite_pdf.save(os.path.join(self.dir_out, self.file_out), deflate=True, garbage=3)
        composite_pdf.close()