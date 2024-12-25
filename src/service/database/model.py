from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class SocialMediaData(Base):
    __tablename__ = "social_media_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String)
    data_id: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    author_id: Mapped[str] = mapped_column(String)
    data_created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    input_data: Mapped[str] = mapped_column(String)

    def __str__(self):
        return f"SocialMediaData(id={self.id}, source={self.source}, data_id={self.data_id}, text={self.text}, author_id={self.author_id}, data_created_at={self.data_created_at}, input_data={self.input_data})"
