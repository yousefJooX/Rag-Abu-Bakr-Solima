"""Store chunk records in MongoDB."""

from bson import ObjectId
from pymongo import InsertOne

from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum


class ChunkModel(BaseDataModel):
    """Handle database operations for the MongoDB chunks collection.

    Look up the collection name in DataBaseEnum, where the app keeps its
    MongoDB collection names.
    """

    def __init__(self, db_client: object):
        """Use the shared database handle to select the chunks collection."""
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self, chunk: DataChunk):
        """Insert a new chunk and return it with its MongoDB ID.

        Convert the Chunk object to a dictionary, save it in the chunks
        collection, and set the inserted ID on the original object.
        """
        result = await self.collection.insert_one(
            chunk.model_dump(by_alias=True, exclude_unset=True)
        )
        chunk.id = result.inserted_id
        return chunk

    async def get_chunk_by_id(self, chunk_id: str):
        """Retrieve a specific chunk by its ID."""
        result = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if result is not None:
            return DataChunk(**result)
        return None

    async def insert_chunks_bulk(self, chunks: list[DataChunk], batch_size: int = 1000) -> int:
        """Insert chunks in batches and return the number MongoDB inserted.

        1 -> Split the chunks into batches to limit the size of each write.
        2 -> Turn each Pydantic model into a document with model_dump().
        3 -> Send one bulk write per batch and add up the inserted counts.
        """
        if batch_size < 1:
            raise ValueError("batch_size must be at least 1")

        inserted_count = 0
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            operations = [
                InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]
            result = await self.collection.bulk_write(operations)
            inserted_count += result.inserted_count
        return inserted_count

    async def delete_chunk_by_project_id(self, project_id: ObjectId) -> int:
        """Delete a project's chunks and return how many were removed.

        1 -> Match chunk_project_id against the project's MongoDB ObjectId.
        2 -> Delete the matching documents and use MongoDB's deleted count.
        """
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count
