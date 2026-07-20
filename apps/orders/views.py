from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiTypes
from .services import get_orders_statistics

class OrderStatisticsView(APIView):
    @extend_schema(
        summary="Отримати статистику замовлень",
        description="Повертає загальну кількість замовлень та суму продажів.",
        responses={200: OpenApiTypes.OBJECT}
    )
    def get(self, request):
        return Response(get_orders_statistics())