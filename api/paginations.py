from rest_framework.pagination import PageNumberPagination

class DefaulPagination(PageNumberPagination):
	page_size = 2