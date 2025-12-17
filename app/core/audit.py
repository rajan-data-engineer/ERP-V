def log_event(action: str, user_id: int, details: str, session: Session | None = None):

    close_session = False
    if session is None:
        session = next(get_session())
        close_session = True

    entry = AuditLog(
        action=action,
        user_id=user_id,
        details=details,
        timestamp=datetime.utcnow()
    )

    session.add(entry)
    session.commit()

    if close_session:
        session.close()

    return entry.id
