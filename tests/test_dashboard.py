from src.dashboard.navigation import NAVIGATION_ITEMS


def test_dashboard_navigation_contains_expected_pages():
    page_keys = {
        item.key
        for item in NAVIGATION_ITEMS
    }

    assert page_keys == {
        "dashboard",
        "onboarding",
        "employees",
        "analytics",
        "data_preview",
    }


def test_dashboard_navigation_has_unique_keys():
    page_keys = [
        item.key
        for item in NAVIGATION_ITEMS
    ]

    assert len(page_keys) == len(set(page_keys))


def test_dashboard_navigation_has_labels():
    for item in NAVIGATION_ITEMS:
        assert item.label
        assert item.icon
        assert item.key