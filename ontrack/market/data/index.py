from django.utils.text import slugify

from ontrack.market.querysets.index import (
    IndexDerivativeEndOfDayQuerySet,
    IndexEndOfDayQuerySet,
)
from ontrack.market.querysets.lookup import ExchangeQuerySet, IndexQuerySet
from ontrack.utils.base.enum import InstrumentType
from ontrack.utils.config import Configurations
from ontrack.utils.datetime import DateTimeHelper as dt
from ontrack.utils.filesystem import FileSystemHelper
from ontrack.utils.logger import ApplicationLogger
from ontrack.utils.logic import LogicHelper
from ontrack.utils.numbers import NumberHelper as nh
from ontrack.utils.string import StringHelper

from .common import CommonData


class PullIndexData:
    def __init__(
        self,
        exchange_symbol: str,
        exchange_qs: ExchangeQuerySet = None,
        index_qs: IndexQuerySet = None,
        index_eod_qs: IndexEndOfDayQuerySet = None,
        index_derivative_eod_qs: IndexDerivativeEndOfDayQuerySet = None,
    ):
        self.logger = ApplicationLogger()
        self.exchange_qs = exchange_qs
        self.index_qs = index_qs
        self.index_eod_qs = index_eod_qs
        self.index_derivative_eod_qs = index_derivative_eod_qs
        self.exchange_symbol = exchange_symbol

        self.exchange = self.exchange_qs.unique_search(self.exchange_symbol).first()
        self.urls = Configurations.get_urls_config()

    def __parse_lookup_data(self, record):
        # remove extra spaces in the dictionaty keys
        record = {k.strip(): v for (k, v) in record.items()}
        symbol = record["symbol"].strip().lower()
        strike_diff = (
            record["strike_difference"] if "strike_difference" in record else 0
        )
        chart_symbol = record["chart_symbol"] if "chart_symbol" in record else symbol

        pk = None
        existing_entity = self.index_qs.unique_search(symbol).first()
        if existing_entity is not None:
            pk = existing_entity.id

        lot_size = 0
        mcr = [x for x in self.market_cap_records if x["symbol"] == symbol]
        if len(mcr) > 0:
            lot_size_str = mcr[0]["lot_size"].strip()
            lot_size = nh.str_to_float(lot_size_str)

        entity = {}
        entity["id"] = pk
        entity["exchange"] = self.exchange
        entity["name"] = record["name"]
        entity["symbol"] = symbol
        entity["lot_size"] = lot_size
        entity["chart_symbol"] = chart_symbol

        entity["ordinal"] = record["ordinal"]
        entity["slug"] = slugify(f"{self.exchange_symbol}_{symbol}")
        entity["is_sectoral"] = record["is_sector"]
        entity["is_active"] = record["is_active"]
        entity["strike_difference"] = strike_diff
        entity["updated_at"] = dt.current_date_time()

        return entity

    def __parse_eod_data(self, record):
        # remove extra spaces in the dictionaty keys
        record = {k.strip(): v for (k, v) in record.items()}
        index_name = record["Index Name"].strip().lower()
        date = dt.string_to_datetime(record["Index Date"], "%d-%m-%Y")

        index = self.index_qs.unique_search(name=index_name).first()
        if index is None:
            return None

        pk = None
        existing_entity = self.index_eod_qs.unique_search(
            date, index_id=index.id
        ).first()
        if existing_entity is not None:
            pk = existing_entity.id

        open_price = nh.str_to_float(record["Open Index Value"])
        high_price = nh.str_to_float(record["High Index Value"])
        low_price = nh.str_to_float(record["Low Index Value"])
        last_price = nh.str_to_float(record["Closing Index Value"])
        close_price = nh.str_to_float(record["Closing Index Value"])
        avg_price = (high_price + low_price) / 2
        price_change = nh.str_to_float(record["Points Change"])
        prev_close = close_price - price_change
        percentage_change = nh.str_to_float(record["Change(%)"])
        traded_quantity = nh.str_to_float(record["Volume"])
        traded_value = nh.str_to_float(record["Turnover (Rs. Cr.)"])
        number_of_trades = None
        quantity_per_trade = None

        index_pe = nh.str_to_float(record["P/E"])
        index_pb = nh.str_to_float(record["P/B"])
        index_div_yield = nh.str_to_float(record["Div Yield"])

        entity = {}
        entity["id"] = pk
        entity["index"] = index
        entity["prev_close"] = prev_close
        entity["open_price"] = open_price
        entity["high_price"] = high_price
        entity["low_price"] = low_price
        entity["last_price"] = last_price
        entity["close_price"] = close_price
        entity["avg_price"] = avg_price
        entity["point_changed"] = price_change
        entity["percentage_changed"] = percentage_change

        entity["traded_quantity"] = traded_quantity
        entity["traded_value"] = traded_value
        entity["number_of_trades"] = number_of_trades
        entity["quantity_per_trade"] = quantity_per_trade

        entity["index_pe"] = index_pe
        entity["index_pb"] = index_pb
        entity["index_div_yield"] = index_div_yield

        entity["date"] = date
        entity["pull_date"] = dt.current_date_time()
        entity["updated_at"] = dt.current_date_time()

        return entity

    def __parse_derivative_eod_data(self, record):
        # remove extra spaces in the dictionaty keys
        record = {k.strip(): v for (k, v) in record.items()}
        symbol = record["SYMBOL"].strip().lower()
        date = dt.string_to_datetime(record["TIMESTAMP"], "%d-%b-%Y")
        expiry_date = dt.string_to_datetime(record["EXPIRY_DT"], "%d-%b-%Y")
        instrument = record["INSTRUMENT"].strip().lower()

        if instrument != InstrumentType.FUTIDX.lower():
            return None

        index = self.index_qs.unique_search(symbol).first()
        if index is None:
            return None

        pk = None
        existing_entity = self.index_derivative_eod_qs.unique_search(
            date, index_id=index.id, expiry_date=expiry_date
        ).first()
        if existing_entity is not None:
            pk = existing_entity.id

        open_price = nh.str_to_float(record["OPEN"])
        high_price = nh.str_to_float(record["HIGH"])
        low_price = nh.str_to_float(record["LOW"])
        last_price = nh.str_to_float(record["SETTLE_PR"])
        prev_close = 0
        close_price = nh.str_to_float(record["CLOSE"])
        avg_price = (high_price + low_price) / 2
        price_change = 0
        percentage_change = 0
        strike_price = None
        option_type = None
        no_of_contracts = nh.str_to_float(record["CONTRACTS"])
        value_of_contracts = nh.str_to_float(record["VAL_INLAKH"])
        open_interest = nh.str_to_float(record["OPEN_INT"])
        change_in_open_interest = nh.str_to_float(record["CHG_IN_OI"])

        entity = {}
        entity["id"] = pk
        entity["index"] = index
        entity["prev_close"] = prev_close
        entity["open_price"] = open_price
        entity["high_price"] = high_price
        entity["low_price"] = low_price
        entity["last_price"] = last_price
        entity["close_price"] = close_price
        entity["avg_price"] = avg_price
        entity["point_changed"] = price_change
        entity["percentage_changed"] = percentage_change

        entity["instrument"] = instrument
        entity["expiry_date"] = expiry_date
        entity["strike_price"] = strike_price
        entity["option_type"] = option_type
        entity["no_of_contracts"] = no_of_contracts
        entity["value_of_contracts"] = value_of_contracts
        entity["open_interest"] = open_interest
        entity["change_in_open_interest"] = change_in_open_interest

        entity["date"] = date
        entity["pull_date"] = dt.current_date_time()
        entity["updated_at"] = dt.current_date_time()

        return entity

    def pull_and_parse_lookup_data(self):
        self.logger.log_debug("Started with indices.")

        indices_percentage_records = self.urls["indices_percentage"]

        market_cap_url = self.urls["fo_marketlot"]
        commonobj = CommonData()
        self.market_cap_records = commonobj.pull_marketlot_data(market_cap_url)

        if self.exchange is None:
            self.logger.log_warning(f"Exchange '{self.exchange_symbol}' doesn't exists")
            return None

        if indices_percentage_records is None or len(indices_percentage_records) == 0:
            self.logger.log_warning("No index records exists.")
            return None

        entities = []
        for record in indices_percentage_records:
            entity = self.__parse_lookup_data(record)
            entities.append(entity)

        return entities

    def pull_parse_eod_data(self, date):
        url_record = self.urls["index_bhavcopy"]
        url = StringHelper.format_url(url_record, date)
        self.logger.log_debug(f"Started with {url}.")

        if self.exchange is None:
            self.logger.log_warning(f"Exchange '{self.exchange_symbol}' doesn't exists")
            return None

        # pull csv containing all the listed equities from web
        data = LogicHelper.reading_csv_pandas_web(url=url)

        # remove extra spaces from the column names and data
        StringHelper.whitespace_remover(data)

        entities = []
        for _, record in data.iterrows():
            entity = self.__parse_eod_data(record)

            if entity is not None:
                entities.append(entity)

        return entities

    def pull_parse_derivative_eod_data(self, date):
        url_record = self.urls["fo_bhavcopy"]
        url = StringHelper.format_url(url_record, date)
        self.logger.log_debug(f"Started with {url}.")

        if self.exchange is None:
            self.logger.log_warning(f"Exchange '{self.exchange_symbol}' doesn't exists")
            return None

        temp_folder = FileSystemHelper.create_temp_folder("fo")
        file_name = FileSystemHelper.download_extract_zip(url, temp_folder)
        path = temp_folder / file_name

        # pull csv containing all the listed equities from web
        data = LogicHelper.reading_csv_pandas(path=path)

        # remove extra spaces from the column names and data
        StringHelper.whitespace_remover(data)

        entities = []
        for _, record in data.iterrows():
            entity = self.__parse_derivative_eod_data(record)

            if entity is not None:
                entities.append(entity)

        return entities
