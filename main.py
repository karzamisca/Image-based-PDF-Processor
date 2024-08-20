import sys
import os
import ocrmypdf
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox

class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.selected_file = None
        self.output_path = None

    def init_ui(self):
        self.setWindowTitle('OCR My PDF')
        self.setGeometry(100, 100, 400, 200)

        # Create widgets
        self.label_input = QLabel('Input Path: Not Selected', self)
        self.label_output = QLabel('Output Path: Not Selected', self)
        
        self.btn_upload = QPushButton('Upload PDF', self)
        self.btn_upload.clicked.connect(self.upload_pdf)

        self.btn_output = QPushButton('Select Output Path', self)
        self.btn_output.clicked.connect(self.select_output_path)

        self.btn_process = QPushButton('Process PDF', self)
        self.btn_process.clicked.connect(self.process_pdf)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_input)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.label_output)
        layout.addWidget(self.btn_output)
        layout.addWidget(self.btn_process)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def upload_pdf(self):
        options = QFileDialog.Options()
        self.selected_file, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if self.selected_file:
            self.label_input.setText(f'Input Path: {self.selected_file}')
            self.btn_output.setEnabled(True)
            self.btn_process.setEnabled(True)

    def select_output_path(self):
        options = QFileDialog.Options()
        self.output_path = QFileDialog.getExistingDirectory(self, "Select Output Directory", options=options)
        if self.output_path:
            self.label_output.setText(f'Output Path: {self.output_path}')

    def process_pdf(self):
        if self.selected_file and self.output_path:
            # Create output directory based on input file name
            base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
            output_dir = os.path.join(self.output_path, base_name)
            ocr_pdf_dir = os.path.join(output_dir, 'ocr_pdf')
            os.makedirs(ocr_pdf_dir, exist_ok=True)
            output_file = os.path.join(ocr_pdf_dir, os.path.basename(self.selected_file))

            # Perform OCR
            try:
                ocrmypdf.ocr(self.selected_file, output_file)
                self.show_message('Success', f'OCR complete. Saved to {output_file}')

                # Create a 'chapters' folder
                chapters_dir = os.path.join(output_dir, 'chapters')
                os.makedirs(chapters_dir, exist_ok=True)

                # Divide into chapters based on "Chapter" keyword
                self.split_into_chapters(output_file, chapters_dir)
            except Exception as e:
                self.show_message('Error', f'An error occurred: {e}')

    def split_into_chapters(self, pdf_path, chapters_dir):
        try:
            # Open the OCR-processed PDF
            pdf_document = fitz.open(pdf_path)
            chapter_start_pages = []

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text = page.get_text("text")

                if text:
                    first_word = text.split()[0].lower()
                    if first_word == 'chapter':
                        chapter_start_pages.append(page_num)

            # Create separate PDFs for each chapter
            for i, start_page in enumerate(chapter_start_pages):
                end_page = chapter_start_pages[i + 1] if i + 1 < len(chapter_start_pages) else len(pdf_document)
                chapter_pdf_path = os.path.join(chapters_dir, f'{os.path.basename(pdf_path).replace(".pdf", f"_chapter_{i+1}.pdf")}')
                chapter_pdf = fitz.open()
                for page_num in range(start_page, end_page):
                    chapter_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
                chapter_pdf.save(chapter_pdf_path)
                chapter_pdf.close()

            pdf_document.close()
            self.show_message('Success', 'Chapters divided and saved successfully.')
        except Exception as e:
            self.show_message('Error', f'An error occurred while splitting chapters: {e}')

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec_())
