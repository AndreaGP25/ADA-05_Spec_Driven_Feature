"""Unit tests for CustomerSearchService."""

import time

from src.domain.models import Customer
from src.repository.customer_repository import InMemoryCustomerRepository
from src.services.search_service import CustomerSearchService


def test_search_partial_match_by_name() -> None:
    """TS-01: Searching 'mar' returns 'Maria Garcia' and 'Omar Lopez'."""
    service = CustomerSearchService()
    results = service.search("mar")

    result_names = [c.name for c in results]
    assert "Maria Garcia" in result_names
    assert "Omar Lopez" in result_names


def test_search_partial_match_by_email() -> None:
    """TS-02: Searching 'gmail' returns all customers with @gmail.com addresses."""
    service = CustomerSearchService()
    results = service.search("gmail")

    assert len(results) >= 2
    for customer in results:
        assert "gmail" in customer.email.lower()


def test_search_case_insensitivity() -> None:
    """TS-03 & AC-02: Case-insensitive searching ('JOHNDOE' matches 'johndoe@example.com')."""
    service = CustomerSearchService()
    results = service.search("JOHNDOE")

    assert len(results) == 1
    assert results[0].name == "John Doe"
    assert results[0].email == "johndoe@example.com"


def test_search_case_insensitivity_mixed_casing() -> None:
    """Search matches regardless of query or record casing."""
    service = CustomerSearchService()
    results = service.search("aLiCe")

    assert len(results) == 1
    assert results[0].name == "Alice Smith"


def test_search_matches_both_name_and_email() -> None:
    """AC-01: Searching 'ana' matches both names ('Ana Silva') and emails ('juliana@example.com')."""
    service = CustomerSearchService()
    results = service.search("ana")

    result_names = [c.name for c in results]
    assert "Ana Silva" in result_names
    assert "Juliana Costa" in result_names


def test_search_no_match_returns_empty_list() -> None:
    """TS-04 & AC-04: Valid queries with no matches return empty list []."""
    service = CustomerSearchService()
    results = service.search("xyz123")

    assert results == []


def test_search_leading_trailing_whitespace_trimmed() -> None:
    """TS-07: Query with leading/trailing whitespace is trimmed and matches properly."""
    service = CustomerSearchService()
    results = service.search("  ana  ")

    result_names = [c.name for c in results]
    assert "Ana Silva" in result_names
    assert "Juliana Costa" in result_names


def test_search_performance_under_100ms() -> None:
    """NFR-01 & AC-05: Search executes and returns in less than 100 ms."""
    service = CustomerSearchService()
    start_time = time.perf_counter()
    results = service.search("ana")
    duration_ms = (time.perf_counter() - start_time) * 1000

    assert duration_ms < 100
    assert len(results) > 0


def test_search_with_custom_repository() -> None:
    """Verify CustomerSearchService with an injected custom repository."""
    custom_records = [
        Customer(id="101", name="Grace Hopper", email="grace@navy.mil"),
        Customer(id="102", name="Ada Lovelace", email="ada@analytical.org"),
    ]
    repo = InMemoryCustomerRepository(customers=custom_records)
    service = CustomerSearchService(repository=repo)

    results = service.search("hopper")
    assert len(results) == 1
    assert results[0].name == "Grace Hopper"

    results_none = service.search("maria")
    assert results_none == []


def test_search_special_characters_email_domain() -> None:
    """AC-06: Searching with special characters like '@' and '.' matches appropriately."""
    service = CustomerSearchService()
    results = service.search("@gmail.com")

    assert len(results) >= 2
    for customer in results:
        assert customer.email.endswith("@gmail.com")


def test_search_special_characters_dots_and_subdomain() -> None:
    """AC-06: Searching with '.' and hyphen or specific characters matches email addresses."""
    service = CustomerSearchService()
    results = service.search(".com")

    assert len(results) > 0
    for customer in results:
        assert ".com" in customer.email

