import pytest
from django.http import HttpRequest

from apps.events import views


@pytest.mark.django_db
def test_events_index():
    request = HttpRequest()
    response = views.index(request)
    assert response.status_code in (200, 302)


if __name__ == '__main__':
    pytest.main()
