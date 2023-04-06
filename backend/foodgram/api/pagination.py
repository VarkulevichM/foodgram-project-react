from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """Пагинатор для определения количества элементов на странице."""
    page_size_query_param = "limit"
