"""Store project records in MongoDB."""

from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum


class ProjectModel(BaseDataModel):
    """Handle database operations for the MongoDB projects collection.

    Look up the collection name in DataBaseEnum, where the app keeps its
    MongoDB collection names.
    """

    def __init__(self, db_client: object):
        """Use the shared database handle to select the projects collection."""
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project: Project):
        """Insert a new project and return it with its MongoDB ID.

        Convert the Project object to a dictionary, save it in the projects
        collection, and set the inserted ID on the original object.
        """
        # Pydantic v2 uses model_dump() to convert the model to a dictionary.
        result = await self.collection.insert_one(
            project.model_dump(by_alias=True, exclude_unset=True)
        )
        project.id = result.inserted_id
        return project

    async def get_project_or_create_one(self, project_id: str):
        """Return the project with this project ID, creating it when needed.

        Convert the document returned by MongoDB into a Project so callers can
        access its fields the same way in both cases.
        """
        new_project = Project(project_id=project_id)
        record = await self.collection.find_one({"project_id": project_id})
        if record is None:
            return await self.create_project(new_project)
        return Project(**record)

    async def get_all_projects(
        self, page: int = 1, page_size: int = 10
    ) -> tuple[list[Project], int]:
        """Return one page of projects and the total number of pages.

        Pagination keeps each response small as the collection grows.

        1 -> Count the documents in the projects collection.
        2 -> Divide by the page size and round up to include a partially filled page.
        3 -> Sort by MongoDB's _id and skip the documents on earlier pages.
        4 -> Fetch up to page_size documents and convert them to Project objects.

        Args:
            page: The page number, starting at 1.
            page_size: The maximum number of projects per page.

        Returns:
            The projects on the requested page and the total number of pages.
            A page beyond the last one returns an empty list with the same total.

        Raises:
            ValueError if page or page_size is less than 1.
        """
        if page < 1 or page_size < 1:
            raise ValueError("page and page_size must be at least 1")

        total_projects = await self.collection.count_documents({})
        total_pages = (total_projects + page_size - 1) // page_size

        if page > total_pages:
            return [], total_pages

        offset = (page - 1) * page_size
        cursor = self.collection.find().sort("_id", 1).skip(offset).limit(page_size)
        projects = [Project(**document) async for document in cursor]

        return projects, total_pages
