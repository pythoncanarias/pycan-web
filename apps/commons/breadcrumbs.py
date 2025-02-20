#!/usr/bin/env python3

from typing import Any

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class BreadCrumb():

    def __init__(self, label, url=None, *args, **kwargs):
        self.parent = None
        if hasattr(label, 'get_absolute_url') and not url:
            url = label.get_absolute_url()
        self.label = str(label)
        self._url = url
        self.args = args
        self.kwargs = kwargs

    def __len__(self) -> int:
        counter = 1
        current = self
        while current.parent is not None:
            counter += 1
            current = current.parent
        return counter

    def _get_url(self) -> str:
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

    url = property(_get_url)

    def __getitem__(self, index: int) -> Any:
        if index == 0:
            return self.label
        elif index == 1:
            return self.url
        else:
            raise IndexError("BreadCrumb solo contiene los índices 0 y 1")

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
            return (item.label, item.url)
        raise StopIteration

    def step(self, label, url=None, *args, **kwargs):
        new_breadcrumb = BreadCrumb(label, url, *args, **kwargs)
        new_breadcrumb.parent = self
        return new_breadcrumb

    def __str__(self):
        *items, last = list(iter(self))
        buff = []
        for label, url in items:
            buff.append(f'<a href="{url}">{label}</a>')
        buff.append(f"<strong>{label}</strong>")
        return '\n'.join(buff)


HOMEPAGE = BreadCrumb('Inicio', '/')
