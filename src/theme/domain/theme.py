# Domain model
from shared.id import Id

from .item import Item


class Theme:
    """
    Theme is a domain class that represents a theme in the application.
    A theme is a collection of items that are related to a specific topic.
    It has a name, a description, an image, and a background associated,

    Image and background are filenames that can be used to retrieve the
    actual content from a storage service.
    """

    id: Id
    name: str
    description: str
    image: str
    items: list[Item]
    background: str

    def __init__(
        self,
        name: str,
        description: str,
        image: str,
        background: str,
        items: list[Item] = [],
        id: Id = None,
    ):
        """
        Creates a new instance of Theme with the specified attributes. If an identifier is provided,
        it is used to uniquely identify the theme, otherwise a new identifier is generated.

        :param id: The identifier of the theme.
        :param name: The name of the theme.
        :param description: The description of the theme.
        :param image: The image associated with the theme.
        :param background: The background image associated with the theme.
        :param items: The list of items associated with the theme.
        """

        self.id = id if isinstance(id, Id) else Id()
        self.name = name
        self.description = description
        self.image = image
        self.items = items
        self.background = background

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Theme) and value.id == self.id
