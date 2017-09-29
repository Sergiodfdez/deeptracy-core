# -*- coding: utf-8 -*-

import deeptracy_core.dal.project.manager as project_manager
from unittest.mock import MagicMock
from deeptracy_core.dal.project.model import Project
from tests.unit.base_test import BaseDeeptracyTest
from tests.unit.mock_db import MockDeeptracyDBEngine


class TestProjectManager(BaseDeeptracyTest):
    """Test methods in project manager"""

    @classmethod
    def setUpClass(cls):
        """Mock the database engine for all tests"""
        project_manager.db = MockDeeptracyDBEngine()
        cls.db = project_manager.db

    def setUp(self):
        self.db.Session.query._ret_val = None

    def test_get_project_invalid_id(self):
        with self.assertRaises(ValueError):
            project_manager.get_project(None, self.db.Session())

    def test_get_project_not_found(self):
        with self.assertRaises(ValueError):
            project_manager.get_project('123', self.db.Session())

    def test_get_project_found(self):
        # mock the return value
        self.db.Session.query._ret_val = Project(id='123', repo='repo')

        project = project_manager.get_project('123', self.db.Session())
        assert project is not None
        assert project.repo == 'repo'

    def test_add_project_valid_repo(self):
        repo_url = 'http://repo.com'
        session = MagicMock()
        project = project_manager.add_project(repo_url, session)
        assert isinstance(project, Project)
        assert project.repo == repo_url
        assert session.add.called

    def test_add_project_missing_repo(self):
        session = MagicMock()
        with self.assertRaises(AssertionError):
            project_manager.add_project(None, session)

        assert not session.add.called