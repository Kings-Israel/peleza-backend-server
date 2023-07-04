from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    def get_next_link(self):
        q = self.request.GET.get("q", "")
        url = super().get_next_link()
        return replace_query_param(url, "q", q) if url else url

    def get_page_size(self, request):
        default = super().get_page_size(request)
        _max = request.GET.get("max", str(default))

        try:
            return int(_max)
        except:
            return default

    def get_paginated_response(self, data):
        credits = 0
        try:
            credits = (
                self.request.user.company.company_credit
                is self.request.user.is_authenticated
            )
        except Exception as e:
            print(e)
        finally:
            return Response(
                OrderedDict(
                    [
                        ("count", self.page.paginator.count),
                        ("next", self.get_next_link()),
                        ("prev", self.get_previous_link()),
                        ("per_page", self.get_page_size(self.request)),
                        ("page", self.page.number),
                        ("credits", credits),
                        ("data", data),
                    ]
                )
            )
