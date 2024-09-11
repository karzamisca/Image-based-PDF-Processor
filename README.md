### Image-based PDF Processor

Classes and Functions
class OCRApp(QMainWindow)

Purpose: This is the main class for the application, responsible for handling the GUI and the logic for the PDF processing and comparison.
__init__(self)

Purpose: Initializes the GUI and sets up default values for the application, such as selected files, output paths, and processing modes.
init_ui(self)

Purpose: Sets up the user interface components (buttons, labels, text editors, etc.) and organizes them in a structured layout for the main window.
change_mode(self)

Purpose: Switches between 'single' and 'multiple' file modes. Resets the selected files when the mode is changed.
upload_files(self)

Purpose: Opens a file dialog for selecting a PDF file (in single mode) or a folder containing multiple PDFs (in multiple mode).
select_output_path(self)

Purpose: Opens a file dialog for selecting the output directory where processed files will be saved.
process_files(self)

Purpose: Main function for processing the selected PDF(s). It performs the following:

    Runs OCR on image-based PDFs.
    Splits PDFs into chapters.
    Converts OCR PDFs to DOCX.
    Compares the text from OCR PDF and DOCX and displays results.

is_text_based(self, pdf_path)

Purpose: Checks if the given PDF is text-based or image-based by scanning each page for any extractable text.
split_into_chapters(self, pdf_path, chapters_dir)

Purpose: Splits the provided PDF into separate chapters based on the presence of the word "Chapter" at the start of a page. Saves each chapter as a separate PDF.
convert_to_docx(self, pdf_path, docx_output_path)

Purpose: Converts the provided PDF to a DOCX file by extracting text from each page and saving it into a DOCX document.
compare_and_show(self, original_pdf, ocr_pdf, docx_file)

Purpose: Performs a visual and textual comparison between the original PDF, the OCR-processed PDF, and the DOCX file. Displays the results in the application.
display_pdf_images(self, pdf_path)

Purpose: Displays images of all pages from the provided PDF file in a scrollable area. This is mainly used for image-based PDFs.
extract_text_from_pdf(self, pdf_path)

Purpose: Extracts the text content from the provided PDF file and returns it as a string.
extract_text_from_docx(self, docx_path)

Purpose: Extracts the text content from the provided DOCX file and returns it as a string.
show_comparison(self, text1, text2)

Purpose: Displays a side-by-side comparison of the text extracted from the OCR-processed PDF and the DOCX file in the application.
show_message(self, title, message)

Purpose: Displays a message box with a given title and message. Used to show success or error messages.
