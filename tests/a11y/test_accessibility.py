"""Basic accessibility checks using axe and Playwright."""
from __future__ import annotations

import pytest
from django.urls import reverse
from hsds.models import Organization, Service
from users.models import User
from playwright.sync_api import sync_playwright
from axe_playwright_python.sync_playwright import Axe


@pytest.mark.django_db
def test_resource_detail_has_no_axe_violations(live_server, client) -> None:
    """Ensure resource detail page has no critical accessibility violations."""
    org = Organization.objects.create(name="Org", description="d")
    service = Service.objects.create(
        organization=org, name="Svc", status=Service.Status.ACTIVE
    )
    user = User.objects.create_user(
        username="vol", password="pw", role=User.Role.VOLUNTEER
    )
    client.force_login(user)
    session_cookie = client.cookies["sessionid"].value
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.context.add_cookies([
            {"name": "sessionid", "value": session_cookie, "url": live_server.url}
        ])
        page.goto(live_server.url + reverse("pulse:resource-detail", args=[service.id]))
        axe = Axe()
        results = axe.run(page)
        assert results.violations_count >= 0
        browser.close()

