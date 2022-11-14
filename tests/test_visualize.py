import pytest

from scraper.domains import SUPPORTED_DOMAINS
from scraper.constants import WEBSITE_COLORS


@pytest.mark.parametrize("domain", SUPPORTED_DOMAINS.keys())
def test_get_website_color_for_supported_domain(domain: str) -> None:
    color = WEBSITE_COLORS.get(domain, None)
    assert color is not None
