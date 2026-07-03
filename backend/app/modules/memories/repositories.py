import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.memories.models import KnowledgeObject, KnowledgeRelation, KnowledgeType

class KnowledgeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_object(self, obj: KnowledgeObject) -> KnowledgeObject:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def get_object(self, org_id: uuid.UUID, canonical_key: str) -> KnowledgeObject | None:
        stmt = select(KnowledgeObject).where(
            KnowledgeObject.organization_id == org_id,
            KnowledgeObject.canonical_key == canonical_key,
            KnowledgeObject.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_objects_by_type(self, org_id: uuid.UUID, obj_type: KnowledgeType) -> list[KnowledgeObject]:
        stmt = select(KnowledgeObject).where(
            KnowledgeObject.organization_id == org_id,
            KnowledgeObject.type == obj_type,
            KnowledgeObject.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_relation(self, relation: KnowledgeRelation) -> KnowledgeRelation:
        self.session.add(relation)
        await self.session.flush()
        await self.session.refresh(relation)
        return relation

    async def get_relations_for_object(self, org_id: uuid.UUID, obj_id: uuid.UUID) -> list[KnowledgeRelation]:
        stmt = select(KnowledgeRelation).join(
            KnowledgeObject, 
            KnowledgeObject.id == KnowledgeRelation.from_node_id
        ).where(
            and_(
                KnowledgeObject.organization_id == org_id,
                KnowledgeRelation.deleted_at.is_(None),
                (KnowledgeRelation.from_node_id == obj_id) | (KnowledgeRelation.to_node_id == obj_id)
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
