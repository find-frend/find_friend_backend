from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    """Custom pagination."""

    page_size_query_param = "limit"
    page_size = 6


class EventPagination(PageNumberPagination):
    """Custom pagination."""

    page_size_query_param = "limit"
    page_size = 4
