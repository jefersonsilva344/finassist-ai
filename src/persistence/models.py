from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.persistence.database import Base


class MessageRole(str, Enum):
    """
    Representa o papel de uma mensagem na conversa.
    """

    USER = "user"
    ASSISTANT = "assistant"


class User(Base):
    """
    Representa o proprietário dos dados financeiros.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    external_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # User 1 -> N Session
    sessions: Mapped[list["Session"]] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        external_id: str,
        **kwargs,
    ):
        now = datetime.now(timezone.utc)

        super().__init__(
            external_id=external_id,
            created_at=now,
            updated_at=now,
            **kwargs,
        )


class Session(Base):
    """
    Representa uma sessão de utilização do FinAssist AI.
    """

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # N Session -> 1 User
    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions",
    )

    # Session 1 -> N FinancialPeriod
    financial_periods: Mapped[list["FinancialPeriod"]] = relationship(
        "FinancialPeriod",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    # Session 1 -> N ConversationMessage
    conversation_messages: Mapped[list["ConversationMessage"]] = relationship(
        "ConversationMessage",
        back_populates="session",
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        user_id: int,
        **kwargs,
    ):
        now = datetime.now(timezone.utc)

        super().__init__(
            user_id=user_id,
            created_at=now,
            last_activity_at=now,
            **kwargs,
        )


class FinancialPeriod(Base):
    """
    Representa o período financeiro de um determinado mês.
    """

    __tablename__ = "financial_periods"

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "year",
            "month",
            name="uq_financial_period_session_year_month",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    income: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    total_expenses: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # N FinancialPeriod -> 1 Session
    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="financial_periods",
    )

    # FinancialPeriod 1 -> N Expense
    expenses: Mapped[list["Expense"]] = relationship(
        "Expense",
        back_populates="period",
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        session_id: int,
        year: int,
        month: int,
        income: Decimal | None = None,
        total_expenses: Decimal | None = None,
        **kwargs,
    ):
        if not 1 <= month <= 12:
            raise ValueError(
                "O mês deve estar entre 1 e 12."
            )

        if year < 1:
            raise ValueError(
                "O ano deve ser maior que zero."
            )

        if income is not None and income <= 0:
            raise ValueError(
                "A renda deve ser maior que zero."
            )

        if total_expenses is not None and total_expenses < 0:
            raise ValueError(
                "O total de despesas não pode ser negativo."
            )


        super().__init__(
            session_id=session_id,
            year=year,
            month=month,
            income=income,
            total_expenses=total_expenses,
            **kwargs,
        )


class Expense(Base):
    """
    Representa uma despesa financeira individual.
    """

    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    period_id: Mapped[int] = mapped_column(
        ForeignKey("financial_periods.id"),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # N Expense -> 1 FinancialPeriod
    period: Mapped["FinancialPeriod"] = relationship(
        "FinancialPeriod",
        back_populates="expenses",
    )

    def __init__(
        self,
        period_id: int,
        category: str,
        amount: Decimal,
        description: str | None = None,
        **kwargs,
    ):
        if not category.strip():
            raise ValueError(
                "A categoria da despesa é obrigatória."
            )

        if amount <= 0:
            raise ValueError(
                "O valor da despesa deve ser maior que zero."
            )

        super().__init__(
            period_id=period_id,
            category=category,
            amount=amount,
            description=description,
            **kwargs,
        )


class ConversationMessage(Base):
    """
    Representa uma mensagem persistida de uma conversa.
    """

    __tablename__ = "conversation_messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )

    role: Mapped[MessageRole] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # N ConversationMessage -> 1 Session
    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="conversation_messages",
    )

    def __init__(
        self,
        session_id: int,
        role: MessageRole,
        content: str,
        **kwargs,
    ):
        if not content.strip():
            raise ValueError(
                "O conteúdo da mensagem é obrigatório."
            )

        super().__init__(
            session_id=session_id,
            role=role,
            content=content,
            **kwargs,
        )