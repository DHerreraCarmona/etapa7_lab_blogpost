from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class CustomPagination(PageNumberPagination):
    page_size = 10                                      
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        total_pages = math.ceil(self.page.paginator.count / self.page_size)
        return Response({
            'pagination':{      
            "total_count": self.page.paginator.count,    
            "total_pages": total_pages,                  
            "current_page": self.page.number,     
            "first_elem": self.page.start_index(),       
            "last_elem": self.page.end_index(),       
            },
            "results": data,
        })
    
#Pagination classes ---------------------------------------------------------------------
class PostListPagination(CustomPagination):
            page_size = 10

class CommentsListPagination(CustomPagination):
        page_size = 5

class LikeListPagination(CustomPagination):
    page_size = 15

