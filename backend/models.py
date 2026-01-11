"""SQLAlchemy models for the Pupil Development Tracker."""
from datetime import date
from sqlalchemy import (
    Column, Integer, String, Date, Boolean, Text, ForeignKey
)
from sqlalchemy.orm import relationship
from database import Base


class SchoolYear(Base):
    """Model for school years."""
    __tablename__ = "school_years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=False)

    classes = relationship("Class", back_populates="school_year")


class Class(Base):
    """Model for classes."""
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    school_year_id = Column(Integer, ForeignKey("school_years.id"))

    school_year = relationship("SchoolYear", back_populates="classes")
    pupils = relationship("Pupil", back_populates="class_")


class Pupil(Base):
    """Model for pupils."""
    __tablename__ = "pupils"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))

    class_ = relationship("Class", back_populates="pupils")
    entries = relationship("Entry", back_populates="pupil")


class Category(Base):
    """Model for entry categories."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name_de = Column(String(100), nullable=False)
    name_en = Column(String(100), nullable=False)
    is_predefined = Column(Boolean, default=False)

    entries = relationship("Entry", back_populates="category")


class Entry(Base):
    """Model for pupil entries."""
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    pupil_id = Column(Integer, ForeignKey("pupils.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    text = Column(Text, nullable=False)
    grade = Column(String(10), nullable=True)
    subject = Column(String(100), nullable=True)

    pupil = relationship("Pupil", back_populates="entries")
    category = relationship("Category", back_populates="entries")
