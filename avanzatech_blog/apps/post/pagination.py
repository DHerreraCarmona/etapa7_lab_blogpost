from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class CustomPagination(PageNumberPagination):
    page_size = 5  # Número de elementos por página
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.page_size)
        return Response({
            "total_count": self.page.paginator.count,  # Total de elementos
            "total_pages": total_pages,  # Total de páginas
            "current_page": self.page.number,  # Página actual
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })
    

#Pagination classes ---------------------------------------------------------------------

class PostListPagination(CustomPagination):
            page_size = 10

class CommentsListPagination(CustomPagination):
        page_size = 10

class LikeListPagination(CustomPagination):
    page_size = 20

