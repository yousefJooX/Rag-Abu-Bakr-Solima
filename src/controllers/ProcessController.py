"""Load saved files and split their text into smaller documents for RAG."""

from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import  PyMuPDFLoader
from models  import ProcessingEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ProcessController(BaseController):
    """Read and chunk files from a single project's upload folder."""

    def __init__(self, project_id: str):
        """Set up processing with the storage path for the given project ID."""
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str) -> str:
        """Return the suffix, such as .pdf, used to select a file loader."""
        return os.path.splitext(file_id)[-1]

    def  get_file_loader(self , file_id: str):
        """Choose a LangChain loader for UTF-8 text or PDF files.

        Return None if the file is missing from the project or has an
        unsupported extension so the route can reject the request.
        """
        if os.path.basename(file_id) != file_id:
            return None

        project_path = os.path.realpath(self.project_path)
        file_path = os.path.realpath(os.path.join(project_path, file_id))
        if os.path.dirname(file_path) != project_path or not os.path.isfile(file_path):
            return None

        file_extension = self.get_file_extension(file_id = file_id)

        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        elif file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        return None

    def get_file_content(self, file_id: str):
        """Load the file into LangChain documents with text and metadata.

        Return None when the project has no supported file with this ID.
        """
        loader = self.get_file_loader(file_id=file_id)
        if loader is None:
            return None
        return loader.load()

    def  process_file_content(self,
                            file_content: list,
                            file_id: str,
                            chunk_size: int = 100,
                            overlap_size: int = 20):
        """Split loaded documents into overlapping chunks measured in characters.

        Overlap carries context across chunk boundaries. Each chunk keeps the
        source document's metadata so it can be traced back to its source.
        """
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
