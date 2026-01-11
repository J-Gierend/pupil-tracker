"""Tests for SQLAlchemy models."""
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import SchoolYear, Class, Pupil, Category, Entry


def test_school_year_creation(test_db):
    """Test creating a school year."""
    school_year = SchoolYear(
        name="2024/2025",
        start_date=date(2024, 9, 1),
        end_date=date(2025, 7, 31),
        is_active=True
    )
    test_db.add(school_year)
    test_db.commit()

    result = test_db.query(SchoolYear).first()
    assert result.name == "2024/2025"
    assert result.is_active is True


def test_class_creation(test_db):
    """Test creating a class linked to school year."""
    school_year = SchoolYear(
        name="2024/2025",
        start_date=date(2024, 9, 1),
        end_date=date(2025, 7, 31)
    )
    test_db.add(school_year)
    test_db.commit()

    class_ = Class(name="Class 1A", school_year_id=school_year.id)
    test_db.add(class_)
    test_db.commit()

    result = test_db.query(Class).first()
    assert result.name == "Class 1A"
    assert result.school_year.name == "2024/2025"


def test_pupil_creation(test_db):
    """Test creating a pupil linked to class."""
    school_year = SchoolYear(
        name="2024/2025",
        start_date=date(2024, 9, 1),
        end_date=date(2025, 7, 31)
    )
    test_db.add(school_year)
    test_db.commit()

    class_ = Class(name="Class 1A", school_year_id=school_year.id)
    test_db.add(class_)
    test_db.commit()

    pupil = Pupil(first_name="Max", last_name="Mustermann", class_id=class_.id)
    test_db.add(pupil)
    test_db.commit()

    result = test_db.query(Pupil).first()
    assert result.first_name == "Max"
    assert result.class_.name == "Class 1A"


def test_category_creation(test_db):
    """Test creating a category."""
    category = Category(
        name_de="Arbeitsverhalten",
        name_en="Work Behavior",
        is_predefined=True
    )
    test_db.add(category)
    test_db.commit()

    result = test_db.query(Category).first()
    assert result.name_de == "Arbeitsverhalten"
    assert result.is_predefined is True


def test_entry_creation(test_db):
    """Test creating an entry with all relationships."""
    school_year = SchoolYear(
        name="2024/2025",
        start_date=date(2024, 9, 1),
        end_date=date(2025, 7, 31)
    )
    test_db.add(school_year)
    test_db.commit()

    class_ = Class(name="Class 1A", school_year_id=school_year.id)
    test_db.add(class_)
    test_db.commit()

    pupil = Pupil(first_name="Max", last_name="Mustermann", class_id=class_.id)
    category = Category(name_de="Test", name_en="Test", is_predefined=False)
    test_db.add_all([pupil, category])
    test_db.commit()

    entry = Entry(
        pupil_id=pupil.id,
        category_id=category.id,
        date=date.today(),
        text="Good progress",
        grade="A",
        subject="Math"
    )
    test_db.add(entry)
    test_db.commit()

    result = test_db.query(Entry).first()
    assert result.text == "Good progress"
    assert result.pupil.first_name == "Max"
    assert result.category.name_en == "Test"
