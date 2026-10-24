from enum import Enum

class ResponseSignal(str, Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully."
    FILE_TYPE_NOT_ALLOWED = "Invalid file type. Only text, pdf, doc, and docx files are allowed."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum allowed size of {max_size} MB."
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully."
    FILE_UPLOAD_FAILED = "File upload failed. Please try again."
    FILE_PROCESSED_SUCCESSFULLY = "File processed successfully."
    FILE_PROCESSING_FAILED = "File processing failed. Please try again."