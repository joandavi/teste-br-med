from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from .models import CurrencyRate

from .utils import getLast5WorkinDays, updateDb, getWorkinDays

from .serializers import CurrencyRateSerializer
 

class currencyApi(ListAPIView):
        serializer_class=CurrencyRateSerializer
        
        def get_queryset(self):
            query_params = self.request.query_params
            if query_params:
                if (
                    "star_date" in query_params and
                    "end_date" in query_params
                ):
                    start_date = datetime.strptime(
                        query_params["star_date"], "%Y-%m-%d"
                    )
                    end_date = datetime.strptime(
                        query_params["end_date"], "%Y-%m-%d"
                    )
                    days = getWorkinDays(start_date, end_date)
                else:
                    raise ValidationError({
                    "message": "INVALID_DATE"
                })
            else:
                days = getLast5WorkinDays()

            queryset = CurrencyRate.objects.filter(
                date__in=days
            )
            if len(days) != queryset.count():
                rates_to_add = set(days)  - set(queryset.values_list(
                    "date", flat=True)
                )
                updateDb(rates_to_add)
                queryset = CurrencyRate.objects.filter(
                    date__in=days
                )
            
            return queryset.order_by("date")
