import sys
import os
import ocrmypdf
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QComboBox

class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.selected_files = []  # To store selected files
        self.output_path = None
        self.mode = 'single'  # 'single' or 'multiple'

    def init_ui(self):
        self.setWindowTitle('OCR My PDF')
        self.setGeometry(100, 100, 400, 250)

        # Create widgets
        self.label_input = QLabel('Input Path: Not Selected', self)
        self.label_output = QLabel('Output Path: Not Selected', self)

        # Dropdown for choosing single or multiple files
        self.combo_mode = QComboBox(self)
        self.combo_mode.addItems(['Single File', 'Folder'])
        self.combo_mode.currentIndexChanged.connect(self.change_mode)

        self.btn_upload = QPushButton('Upload PDF', self)
        self.btn_upload.clicked.connect(self.upload_files)

        self.btn_output = QPushButton('Select Output Path', self)
        self.btn_output.clicked.connect(self.select_output_path)

        self.btn_process = QPushButton('Process PDF', self)
        self.btn_process.clicked.connect(self.process_files)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_input)
        layout.addWidget(self.combo_mode)
        layout.addWidget(self.btn_upload)
        layout.addWidget(self.label_output)
        layout.addWidget(self.btn_output)
        layout.addWidget(self.btn_process)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def change_mode(self):
        self.mode = 'multiple' if self.combo_mode.currentIndex() == 1 else 'single'
        self.selected_files = []  # Clear selected files when changing mode
        self.label_input.setText('Input Path: Not Selected')

    def upload_files(self):
        if self.mode == 'single':
            options = QFileDialog.Options()
            file, _ = QFileDialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
            if file:
                self.selected_files = [file]
                self.label_input.setText(f'Input Path: {file}')
                self.btn_output.setEnabled(True)
                self.btn_process.setEnabled(True)
        else:
            options = QFileDialog.Options()
            folder = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
            if folder:
                self.selected_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.pdf')]
                if self.selected_files:
                    self.label_input.setText(f'Input Path: {len(self.selected_files)} files selected')
                    self.btn_output.setEnabled(True)
                    self.btn_process.setEnabled(True)

    def select_output_path(self):
        options = QFileDialog.Options()
        self.output_path = QFileDialog.getExistingDirectory(self, "Select Output Directory", options=options)
        if self.output_path:
            self.label_output.setText(f'Output Path: {self.output_path}')

    def process_files(self):
        if self.selected_files and self.output_path:
            for selected_file in self.selected_files:
                base_name = os.path.splitext(os.path.basename(selected_file))[0]
                output_dir = os.path.join(self.output_path, base_name)
                ocr_pdf_dir = os.path.join(output_dir, 'ocr_pdf')
                os.makedirs(ocr_pdf_dir, exist_ok=True)
                output_file = os.path.join(ocr_pdf_dir, os.path.basename(selected_file))

                try:
                    # Perform OCR
                    ocrmypdf.ocr(selected_file, output_file)
                    self.show_message('Success', f'OCR complete for {selected_file}. Saved to {output_file}')

                    # Create a 'chapters' folder
                    chapters_dir = os.path.join(output_dir, 'chapters')
                    os.makedirs(chapters_dir, exist_ok=True)

                    # Divide into chapters based on "Chapter" keyword
                    self.split_into_chapters(output_file, chapters_dir)
                except Exception as e:
                    self.show_message('Error', f'An error occurred with file {selected_file}: {e}')

    def split_into_chapters(self, pdf_path, chapters_dir):
        try:
            pdf_document = fitz.open(pdf_path)
            chapter_start_pages = []

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text = page.get_text("text")

                if text:
                    first_word = text.split()[0].lower()
                    if first_word == 'chapter':
                        chapter_start_pages.append(page_num)

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
