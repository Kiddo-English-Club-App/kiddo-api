import unittest
from unittest.mock import Mock
from uuid import uuid4, UUID
from theme.domain.theme import Theme
from theme.application.theme_service import ThemeService
from shared import exceptions
from ..mocks import mock_app_context


def mock_theme(id: UUID):
    return Theme(
        id = id,
        name="Test Theme", 
        description="Test Description", 
        image="Test Image", 
        background="Test Background")

def mock_theme_repository(mock, mocked_theme):
    mock.find_by_id.return_value = mocked_theme
    return mock


class TestGetTheme(unittest.TestCase):

    def test_get_theme(self):
        theme_id = uuid4()
        mocked_theme = mock_theme(theme_id)
        mock = Mock()
        mock = mock_theme_repository(mock, mocked_theme)
        mock = mock_app_context(mock, uuid4(), "admin")

        theme_service = ThemeService(mock, mock)

        theme = theme_service.get_theme(theme_id)
        self.assertEqual(theme.id, mocked_theme.id)
        self.assertEqual(theme.name, mocked_theme.name)
        self.assertEqual(theme.description, mocked_theme.description)
        self.assertEqual(theme.image, mocked_theme.image)
        self.assertEqual(theme.background, mocked_theme.background)
    
    def test_get_theme_not_found(self):
        theme_id = uuid4()
        mock = Mock()
        mock = mock_theme_repository(mock, None)
        mock = mock_app_context(mock, uuid4(), "admin")
        theme_service = ThemeService(mock, mock)

        with self.assertRaises(exceptions.NotFound):
            theme_service.get_theme(theme_id)

    def test_get_theme_unauthorized(self):
        mock = Mock()
        mock = mock_app_context(mock, None, None, False)

        theme_service = ThemeService(mock, mock)

        with self.assertRaises(exceptions.Unauthorized):
            theme_service.get_theme(uuid4())


class TestListThemes(unittest.TestCase):

    def test_list_themes(self):
        theme_id = uuid4()
        mocked_theme = mock_theme(theme_id)
        mock = Mock()
        mock.find_all.return_value = [mocked_theme]
        mock = mock_app_context(mock, uuid4(), "admin")

        theme_service = ThemeService(mock, mock)

        themes = theme_service.get_themes()
        self.assertEqual(len(themes), 1)
        theme = themes[0]
        self.assertEqual(theme.id, mocked_theme.id)
        self.assertEqual(theme.name, mocked_theme.name)
        self.assertEqual(theme.description, mocked_theme.description)
        self.assertEqual(theme.image, mocked_theme.image)
        self.assertEqual(theme.background, mocked_theme.background)
    
    def test_list_themes_unauthorized(self):
        mock = Mock()
        mock = mock_app_context(mock, None, None, False)

        theme_service = ThemeService(mock, mock)

        with self.assertRaises(exceptions.Unauthorized):
            theme_service.get_themes()
