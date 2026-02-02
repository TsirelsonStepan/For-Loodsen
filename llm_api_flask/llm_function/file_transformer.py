import io
from pypdf import PdfReader
from docx import Document
from werkzeug.datastructures import FileStorage


# Problems:
#   Cant find text in docx with table
#   file.content_type for docx is too long


def GetTextFromBinary(file: FileStorage) -> str:
	data = file.read()
	text = ""
	match file.content_type:
		case "application/pdf":
			pdf_reader = PdfReader(io.BytesIO(data))
			for page in pdf_reader.pages:
				text += page.extract_text()
			return text
		case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
			word_doc = Document(io.BytesIO(data))
			for paragraph in word_doc.paragraphs:
				text += paragraph.text
			return text
