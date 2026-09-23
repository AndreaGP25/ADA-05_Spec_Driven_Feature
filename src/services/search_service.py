"""Customer search service module."""

from typing import List, Optional

from src.domain.exceptions import InvalidQueryError
from src.domain.models import Customer
from src.repository.customer_repository import (
    CustomerRepositoryProtocol,
    InMemoryCustomerRepository,
)


class CustomerSearchService:
    """Service responsible for searching customer records."""

    def __init__(self, repository: Optional[CustomerRepositoryProtocol] = None) -> None:
        """Initialize CustomerSearchService.
        
        Args:
            repository: Customer repository fulfilling CustomerRepositoryProtocol.
                        Defaults to InMemoryCustomerRepository.
        """
        self._repository: CustomerRepositoryProtocol = (
            repository if repository is not None else InMemoryCustomerRepository()
        )

    def search(self, query: str) -> List[Customer]:
        """Search customers by name or email using case-insensitive partial match.
        
        Args:
            query: The search query string.
            
        Returns:
            List of matching Customer records, or an empty list if no matches found.

        Raises:
            InvalidQueryError: If query is None, empty, whitespace-only, or < 2 characters.
        """
        if query is None:
            raise InvalidQueryError("Query cannot be empty or whitespace")

        trimmed_query = query.strip()
        if not trimmed_query:
            raise InvalidQueryError("Query cannot be empty or whitespace")

        if len(trimmed_query) < 2:
            raise InvalidQueryError("Query must be at least 2 characters long")

        normalized_query = trimmed_query.lower()

        results: List[Customer] = []
        for customer in self._repository.get_all():
            if (
                normalized_query in customer.name.lower()
                or normalized_query in customer.email.lower()
            ):
                results.append(customer)

        return results
