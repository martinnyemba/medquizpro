#!/usr/bin/env python3
"""Module for Model for Study groups"""
from datetime import datetime
from app import db

# Association table for the many-to-many relationship between users and study groups
user_study_groups = db.Table('user_study_groups',
                             db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                             db.Column('study_group_id', db.Integer, db.ForeignKey('study_groups.id'), primary_key=True)
                             )


class StudyGroup(db.Model):
    """Model for study groups"""
    __tablename__ = 'study_groups'

    id = db.Column(db.Integer, primary_key=True)
    """int: Primary key for the study group"""

    name = db.Column(db.String(100), nullable=False)
    """str: Name of the study group"""

    description = db.Column(db.Text)
    """str: Description of the study group"""

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    """datetime: Timestamp when the study group was created"""

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    """datetime: Timestamp when the study group was last updated"""
