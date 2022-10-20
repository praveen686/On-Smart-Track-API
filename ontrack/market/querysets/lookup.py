from django.db import models
from django.db.models import Q

from ontrack.utils.config import Configurations
from ontrack.utils.datetime import DateTimeHelper


class ExchangeQuerySet(models.QuerySet):
    def unique_search(self, symbol=None):
        if symbol is None:
            return self.none()

        lookups = Q(symbol__iexact=symbol)
        return self.filter(lookups)


class EquityQuerySet(models.QuerySet):
    def unique_search(self, symbol=None):
        if symbol is None:
            return self.none()

        lookups = Q(symbol__iexact=symbol)
        return self.filter(lookups)


class IndexQuerySet(models.QuerySet):
    def unique_search(self, symbol=None):
        if symbol is None:
            return self.none()

        lookups = Q(symbol__iexact=symbol)
        return self.filter(lookups)


class EquityIndexQuerySet(models.QuerySet):
    def unique_search(self, index_symbol=None, equity_symbol=None):
        if equity_symbol is None or equity_symbol is None:
            return self.none()

        lookup_equity = Q(equity__symbol__iexact=equity_symbol)
        lookup_index = Q(index__symbol__iexact=index_symbol)

        return self.filter(lookup_equity & lookup_index)

    def search_old_records(self):
        threshold = DateTimeHelper.get_past_date(
            days=Configurations.get_default_values_config()[
                "days_for_delete_lookup_data"
            ]
        )
        return self.filter(last_update_date__lt=threshold)