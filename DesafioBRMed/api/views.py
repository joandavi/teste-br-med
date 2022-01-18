
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from .models import CurrencyRate

from .utils import getLast5WorkinDays, updateDb

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
                    queryset = CurrencyRate.objects.all()
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
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", rates_to_add)

                    updateDb(rates_to_add)
                    queryset = CurrencyRate.objects.filter(
                        date__in=days
                    )
            
            return queryset.order_by("date")
