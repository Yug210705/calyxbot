import abc

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit.models import AuditLog


class AuditLogRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, audit_log: AuditLog) -> AuditLog:
        pass

class SQLAlchemyAuditLogRepository(AuditLogRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, audit_log: AuditLog) -> AuditLog:
        self.session.add(audit_log)
        await self.session.flush()
        await self.session.refresh(audit_log)
        return audit_log
