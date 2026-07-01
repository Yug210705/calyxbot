from app.modules.audit.repositories import (
    AuditLogRepository,
    SQLAlchemyAuditLogRepository,
)


def test_audit_log_immutability():
    """
    Verify that AuditLogRepository only exposes create methods
    and explicitly does NOT expose update or delete methods,
    guaranteeing audit log immutability by design.
    """
    # Check abstract base class
    methods = [func for func in dir(AuditLogRepository) if callable(getattr(AuditLogRepository, func)) and not func.startswith("__")]

    assert "create" in methods, "AuditLogRepository must expose create()"

    # Assert no update or delete methods exist
    forbidden_prefixes = ["update", "delete", "remove", "edit", "modify"]

    for method in methods:
        for prefix in forbidden_prefixes:
            assert not method.startswith(prefix), f"AuditLogRepository must not expose '{method}' to guarantee immutability"

    # Check concrete implementation
    methods_concrete = [func for func in dir(SQLAlchemyAuditLogRepository) if callable(getattr(SQLAlchemyAuditLogRepository, func)) and not func.startswith("__")]

    for method in methods_concrete:
        for prefix in forbidden_prefixes:
            assert not method.startswith(prefix), f"SQLAlchemyAuditLogRepository must not expose '{method}' to guarantee immutability"
