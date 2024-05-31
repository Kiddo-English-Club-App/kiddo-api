from theme.domain.theme import Theme


def mock_theme():
    return Theme(
        name="Theme",
        image="image.jpg",
        description="Description",
        background="background.jpg"
    )