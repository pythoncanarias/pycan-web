import collections

from django.urls import reverse_lazy


class MenuItem:

    def __init__(self, text, link):
        self.text = text
        self.url = reverse_lazy(link)


class MenuSection:

    def __init__(self, menu, section_title):
        self.menu = menu
        self.title = section_title
        self.items = []

    def __iter__(self):
        for item in self.items:
            yield item

    def add_menu_item(self, text, link):
        new_item = MenuItem(text, link)
        self.items.append(new_item)
        return self

    def finished(self):
        return self.menu


class Menu:

    def __init__(self):
        self.sections = collections.OrderedDict({})

    def __iter__(self):
        for section in self.sections.values():
            yield section

    def __getattr__(self, name):
        if name in self.sections:
            return self.sections[name]
        else:
            raise AttributeError(
                f"Objects of class {self.__class__!r}"
                f" doesn't have attribute {name}"
                )

    def add_section(self, label, section_title):
        new_section = MenuSection(self, section_title)
        self.sections[label] = new_section
        return new_section
