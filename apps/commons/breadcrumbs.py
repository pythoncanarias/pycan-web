#!/usr/bin/env python3

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class BreadCrumb:

    def __init__(self, label, url=None, parent=None, *args, **kwargs):
        self.parent = parent
        self.level = self.parent.level + 1 if self.parent else 0
        if hasattr(label, 'get_absolute_url') and not url:
            url = label.get_absolute_url()
        self.label = str(label)
        self._url = url
        self.args = args
        self.kwargs = kwargs

    def get_url(self):
        if (
            self._url
            and not self.args
            and not self.kwargs
            and hasattr(self._url, "get_absolute_url")
            and callable(self._url.get_absolute_url)
        ):
            return self._url.get_absolute_url()
        try:
            return reverse(self._url, args=self.args, kwargs=self.kwargs)
        except NoReverseMatch:
            return self._url

    url = property(get_url)

    def __getitem__(self, index):
        if index == 0:
            return self.label
        elif index == 1:
            return self._get_url()
        else:
            raise IndexError("La clase BreadCrumb solo se puede acceder con índices 0, 1")

    def __iter__(self):
        item = self
        self.chain = [item]
        while item.parent:
            item = item.parent
            self.chain.append(item)
        return self

    def __next__(self):
        while self.chain:
            item = self.chain.pop()
            return item
        raise StopIteration

    def step(self, label, url=None, *args, **kwargs):
        return BreadCrumb(label, url, self, *args, **kwargs)

    def __str__(self):
        *items, _last = list(iter(self))
        buff = []
        for item in items:
            label = item.label
            url = item.url
            buff.append(f'<a href="{url}">{label}</a>')
        buff.append(f"<strong>{label}</strong>")
        return '\n'.join(buff)
