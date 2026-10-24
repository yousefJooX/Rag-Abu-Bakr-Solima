from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import  PyMuPDFLoader
from models  import ProcessingEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str) -> str:
        """Get the file extension from the file name."""
        return os.path.splitext(file_id)[-1]

    def  get_file_loader(self , file_id: str):
        """Get the appropriate file loader based on the file extension."""
        file_extension = self.get_file_extension(file_id = file_id)
        file_path = os.path.join(self.project_path, file_id)

        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        elif file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        return None  # unsupported extension -> the route returns 400

    def get_file_content(self, file_id: str):
        """Get the content of the file using the appropriate loader."""
        loader = self.get_file_loader(file_id=file_id)
        if loader is None:
            return None
        return loader.load() # list of object document

    def  process_file_content(self,
                            file_content: list,
                            file_id: str,
                            chunk_size: int = 100,
                            overlap_size: int = 20):
        """Process the file content by splitting it into chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )
        file_content_texts = [
            rec.page_content 
            for rec in file_content
        ]
        file_content_metadata = [
            rec.metadata 
            for rec in file_content
        ]
        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )
        return chunks