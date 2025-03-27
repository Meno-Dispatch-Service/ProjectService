from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import String, Integer, JSON
from core.database.project import Base


class Project(Base):

    title: Mapped[str] = mapped_column(String, nullable=False)
    participants_id: Mapped[list[int]] = mapped_column(MutableList.as_mutable(JSON), default=[])
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    meeting_days: Mapped[str] = mapped_column(
        String,
        default="Monday",
    )


### Нужно ещё создать project-static микросервис

#### Она отвечает за успевайемость проекта, кто сколько тасков выполнил и так далее
