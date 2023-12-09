from rest_framework.pagination import PageNumberPagination


class StandartResultPaginator(PageNumberPagination):
    page_size = 10
    max_page_size = 20


class BookPaginator(PageNumberPagination):
    page_size = 8
    max_page_size = 30
