from django.test import RequestFactory

import pulse.components.form_field  # noqa: F401 ensures component registration
from pulse.views import components as component_views


def render_form_field(**params):
    rf = RequestFactory()
    request = rf.get("/c/form_field/", params)
    response = component_views.component(request, "form_field")
    return response.content.decode()


def test_aria_describedby_omitted_when_no_help_or_error():
    html = render_form_field(name="field")
    assert "aria-describedby" not in html


def test_aria_describedby_includes_help_and_error():
    html = render_form_field(name="field", help_text="hint", error="oops")
    assert 'aria-describedby="field-help field-error"' in html


def test_aria_describedby_only_help():
    html = render_form_field(name="field", help_text="hint")
    assert 'aria-describedby="field-help"' in html
    assert "field-error" not in html
