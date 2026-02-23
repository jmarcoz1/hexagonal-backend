"""Database engine and session management."""

import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    """Manages the SQLAlchemy engine and session factory."""

    def __init__(
        self,
        db_url: str,
        pool_size: int = 5,
        max_overflow: int = 10,
        echo: bool = False,
    ) -> None:
        self._engine = create_engine(
            db_url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=echo,
        )
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    def create_database(self) -> None:
        """Create all tables. Use only for testing; prefer Alembic for production."""
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self):
        """Provide a transactional session scope."""
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback due to exception")
            session.rollback()
            raise
        finally:
            session.close()
