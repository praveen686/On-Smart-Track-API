from django.db import models
from django.db.models import Q

from ontrack.utils.datetime import DateTimeHelper as dt


class BaseQuerySet(models.QuerySet):
    def search_old_records(self, days_count):
        threshold = dt.get_past_date(days=days_count)
        return self.filter(updated_at__lt=threshold)


class BaseEntityQuerySet(BaseQuerySet):
    def unique_entity(self, uid):
        if uid is None:
            return self.none()

        lookups = Q(id=uid)

        return self.filter(lookups)

    def unique_search(self, symbol=None, name=None):
        if symbol is None and name is None:
            return self.none()

        if symbol is not None:
            lookups = Q(symbol__iexact=symbol)

        if name is not None:
            lookups = Q(name__iexact=name)

        return self.filter(lookups)

    def search_old_records(self, days_count):
        threshold = dt.get_past_date(days=days_count)
        return self.filter(date__lt=threshold)

    def search_records_after_date(self, date):
        return self.filter(date__gte=date)

    def get_records_after_date(self, query, days_count):
        if query is None:
            return self.none()

        date = query["date"]
        average_date = dt.get_past_date(date, days=days_count)
        lookups = (
            Q(date__gte=average_date)
            & Q(date__lt=query["date"])
            & Q(entity__symbol=query["symbol"])
        )
        return self.filter(lookups)


class EntityDataQuerySet(BaseEntityQuerySet):
    def unique_search(self, date, entity_id=None, entity_symbol=None):
        if entity_id is None and entity_symbol is None:
            return self.none()

        if date is None:
            return self.none()

        lookups = Q(date=date)

        if entity_id is not None:
            lookups = lookups & Q(entity_id=entity_id)
        else:
            lookups = lookups & Q(entity__symbol=entity_symbol)

        return self.filter(lookups)


class EntityDerivativeQuerySet(BaseEntityQuerySet):
    def unique_search(
        self,
        date,
        instrument,
        expiry_date,
        entity_id=None,
        entity_symbol=None,
        strike_price=None,
        option_type=None,
    ):

        if entity_id is None and entity_symbol is None:
            return self.none()

        lookups = Q(date=date)

        if entity_id is not None:
            lookups = lookups & Q(entity_id=entity_id)
        else:
            lookups = lookups & Q(entity__symbol__iexact=entity_symbol)

        lookups = (
            lookups & Q(instrument__iexact=instrument) & Q(expiry_date=expiry_date)
        )

        if strike_price is not None and option_type is not None:
            lookups = (
                lookups
                & Q(strike_price=strike_price)
                & Q(option_type__iexact=option_type)
            )

        return self.filter(lookups)
