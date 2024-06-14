from shared.id import Id


class Item:
    """
    Item is a domain class that represents an item in the theme.
    An item is a word or content that is part of a theme. It has
    a name, an image, and a sound associated, which can be used to
    present the item in the application.

    Image and sound are filenames that can be used to retrieve the
    actual content from a storage service.
    """

    id: Id
    name: str
    image: str
    sound: str

    def __init__(self, name: str, image: str, sound: str, id: Id = None):
        """
        Creates a new instance of Item with the provided name, image, and sound.
        If an identifier is provided, it is used to uniquely identify the item,
        otherwise a new identifier is generated.

        :param name: The name of the item.
        :param image: The image associated with the item.
        :param sound: The sound associated with the item.
        :param id: The identifier of the item.
        """
        self.id = id if isinstance(id, Id) else Id(id)
        self.name = name
        self.image = image
        self.sound = sound

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Item) and value.id == self.id
