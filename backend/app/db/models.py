from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
    Table,
    Time,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    reads = relationship("WeatherData", secondary="users_reads", back_populates="users")

    settings = relationship(
        "UserSettings", back_populates="user", uselist=False, lazy="joined"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


users_reads = Table(
    "users_reads",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("weather_data_id", Integer, ForeignKey("weather_data.id"), primary_key=True),
)


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now(datetime.timezone.utc))

    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)

    users = relationship("User", secondary="users_reads", back_populates="reads")


class UserSettings(Base):

    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True)

    # notificating
    device_token = Column(String, nullable=True)
    notifications = Column(Boolean, default=True)
    notify_by_email = Column(Boolean, default=False)

    read_times = relationship("ReadTimes", back_populates="user_settings")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="settings")


class ReadTimes(Base):

    __tablename__ = "read_times"

    id = Column(Integer, primary_key=True)

    time = Column(Time, nullable=False)

    user_settings_id = Column(Integer, ForeignKey("user_settings.id"), nullable=False)
    user_settings = relationship("UserSettings", back_populates="read_times")
