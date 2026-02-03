from __future__ import annotations
from typing import Any, Dict, List, Optional


class FakeInsertOneResult:
    def __init__(self, inserted_id: Any):
        self.inserted_id = inserted_id


class FakeUpdateResult:
    def __init__(self, matched_count: int = 0, modified_count: int = 0, upserted_id: Any = None):
        self.matched_count = matched_count
        self.modified_count = modified_count
        self.upserted_id = upserted_id


class FakeCollection:
    """
    Super simple in-memory collection.
    Only implements things you’re likely to use:
    - find_one
    - insert_one
    - update_one (with $set and $setOnInsert)
    - delete_many
    - find (very basic)
    - create_index (no-op)
    """

    def __init__(self, name: str):
        self.name = name
        self._docs: List[Dict[str, Any]] = []
        self._id_counter = 0

    async def find_one(self, query: Dict[str, Any], *args, **kwargs) -> Optional[Dict[str, Any]]:
        for doc in self._docs:
            if all(doc.get(k) == v for k, v in query.items()):
                return doc
        return None

    async def insert_one(self, doc: Dict[str, Any],*args, **kwargs) -> FakeInsertOneResult:
        self._id_counter += 1
        # mimic Mongo _id assignment if not provided
        if "_id" not in doc:
            doc = {**doc, "_id": self._id_counter}
        self._docs.append(doc)
        return FakeInsertOneResult(inserted_id=doc["_id"])

    async def update_one(self, filter: Dict[str, Any], update: Dict[str, Any], upsert: bool = False) -> FakeUpdateResult:
        # very simplified behaviour, only handles $set and $setOnInsert
        matched = None
        for doc in self._docs:
            if all(doc.get(k) == v for k, v in filter.items()):
                matched = doc
                break

        if matched is not None:
            if "$set" in update:
                matched.update(update["$set"])
            # ignoring $setOnInsert when doc exists
            return FakeUpdateResult(matched_count=1, modified_count=1)

        if upsert:
            new_doc = dict(filter)
            if "$setOnInsert" in update:
                new_doc.update(update["$setOnInsert"])
            if "$set" in update:
                new_doc.update(update["$set"])
            res = await self.insert_one(new_doc)
            return FakeUpdateResult(matched_count=0, modified_count=0, upserted_id=res.inserted_id)

        return FakeUpdateResult()

    async def delete_many(self, _filter: Dict[str, Any]) -> None:
        # blunt hammer: if filter is {}, delete all
        if not _filter:
            self._docs.clear()
            return

        remaining = []
        for doc in self._docs:
            if not all(doc.get(k) == v for k, v in _filter.items()):
                remaining.append(doc)
        self._docs = remaining

    async def find(self, query: Dict[str, Any] | None = None):
        # very crude; ignores projection, sorting, etc.
        query = query or {}
        result = [doc for doc in self._docs if all(doc.get(k) == v for k, v in query.items())]

        # mimic Motor's async iterator:
        class _Cursor:
            def __init__(self, docs):
                self._docs = docs
                self._idx = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self._idx >= len(self._docs):
                    raise StopAsyncIteration
                doc = self._docs[self._idx]
                self._idx += 1
                return doc

        return _Cursor(result)

    async def create_index(self, *args, **kwargs):
        # no-op in fake DB
        return None
    
    async def clear(self):
        self._docs.clear()


class FakeDB:
    """
    Mimics your db = client[MONGO_DB_NAME] object.
    Provides:
      - db["users"], db["meal_logs"], ...
      - db.users, db.meal_logs, ...
    """
    def __init__(self):
        self._collections: dict[str, FakeCollection] = {}

        for name in [
            "users",
            "meal_logs",
            "ingredients_collection",
            "user_settings",
            "optimized_weights_collection",
            "optimized_macros_collection",
            "user_ingredients_collection",
            "user_meals_collection",
        ]:
            coll = FakeCollection(name)
            self._collections[name] = coll
            setattr(self, name, coll)  # so db.user_settings and db["user_settings"] share the same object

    def __getitem__(self, name: str) -> FakeCollection:
        # always return the same instance
        if name not in self._collections:
            coll = FakeCollection(name)
            self._collections[name] = coll
            setattr(self, name, coll)
        return self._collections[name]

    def __getattr__(self, name: str) -> FakeCollection:
        if name.startswith("_"):
            raise AttributeError
        return self[name]
    