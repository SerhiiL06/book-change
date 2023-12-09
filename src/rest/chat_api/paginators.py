from rest_framework.pagination import PageNumberPagination


class MessagePaginator(PageNumberPagination):
    page_size = 20
    max_page_size = 50
