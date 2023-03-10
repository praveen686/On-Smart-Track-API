from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from ontrack.lookup.api.logic.settings import SettingLogic
from ontrack.market.api.logic.endofdata import EndOfDayData
from ontrack.market.api.logic.lookup import MarketLookupData
from ontrack.market.api.logic.screener import Screener
from ontrack.market.models.lookup import Equity, Exchange, Index
from ontrack.utils.base.enum import AdminSettingKey as sk
from ontrack.utils.base.enum import ExchangeType, SettingKeyType
from ontrack.utils.config import Configurations as conf
from ontrack.utils.datetime import DateTimeHelper as dt


class TestLogicLookup:
    @pytest.fixture(autouse=True)
    def injector(self):
        self.exchange_qs = Exchange.backend.get_queryset()

    @pytest.fixture(autouse=True)
    def equity_index_data_fixture(self, market_lookup_data_fixture: MarketLookupData):
        self.marketlookupdata = market_lookup_data_fixture
        records = self.marketlookupdata.load_equity_data()
        self.marketlookupdata.create_or_update(records, Equity)

        records = self.marketlookupdata.load_index_data()
        self.marketlookupdata.create_or_update(records, Index)

        self.settings = SettingLogic()

    @pytest.mark.unittest
    def test_execute_market_lookup_data_task_2(self):
        obj = EndOfDayData(ExchangeType.NSE)
        last_excution_date = dt.get_date_time(2022, 8, 1, 0, 0, 0)
        current_date = dt.get_date_time(2022, 8, 2, 0, 0, 0)
        obj.load_equity_eod_data = MagicMock(return_value=None)
        obj.load_equity_corporate_action = MagicMock(return_value=None)
        obj.load_equity_derivative_eod_data = MagicMock(return_value=None)
        result = obj.execute_equity_eod_data_task(last_excution_date, current_date)
        assert result is not None

    @pytest.mark.unittest
    def test_execute_market_lookup_data_task_Exchange_None(self):
        obj = EndOfDayData("Not-Existing-Exchange")
        obj.load_equity_eod_data = MagicMock(return_value=None)
        obj.load_equity_corporate_action = MagicMock(return_value=None)
        obj.load_equity_derivative_eod_data = MagicMock(return_value=None)
        result = obj.execute_equity_eod_data_task()
        assert result is not None

    @pytest.mark.unittest
    def test_execute_market_lookup_data_task_Date_1(self):
        last_excution_date = dt.get_date_time(2022, 10, 19, 0, 0, 0)
        current_date = dt.get_date_time(2022, 10, 27, 15, 30, 0)
        end_date = dt.get_date_time(2022, 10, 20, 15, 30, 0)

        key = sk.DATAPULL_EQUITY_EOD_LAST_PULL_DATE
        self.settings.save_setting(key, None, SettingKeyType.EXECUTION_TIME)
        with freeze_time(current_date):
            obj = EndOfDayData(ExchangeType.NSE)
            obj.can_execute_task = MagicMock(
                return_value=(True, None, last_excution_date)
            )
            obj.load_equity_eod_data = MagicMock(return_value=None)
            obj.load_equity_corporate_action = MagicMock(return_value=None)
            obj.load_equity_derivative_eod_data = MagicMock(return_value=None)
            result = obj.execute_equity_eod_data_task(None, end_date)
            assert result is not None
            assert len(result) == 2
            assert "message" in result[1]
            assert obj.load_equity_eod_data.call_count == 1

            obj = EndOfDayData(ExchangeType.NSE)
            obj.load_equity_eod_data = MagicMock(return_value=None)
            obj.load_equity_corporate_action = MagicMock(return_value=None)
            obj.load_equity_derivative_eod_data = MagicMock(return_value=None)
            result = obj.execute_equity_eod_data_task()
            assert result is not None
            assert len(result) == 1
            assert "message" in result[0]
            obj.load_equity_eod_data.assert_not_called()

            obj = EndOfDayData(ExchangeType.NSE)
            obj.load_equity_eod_data = MagicMock(return_value=None)
            obj.load_equity_corporate_action = MagicMock(return_value=None)
            obj.load_equity_derivative_eod_data = MagicMock(return_value=None)
            result = obj.execute_equity_eod_data_task(last_excution_date, end_date)
            assert result is not None
            assert len(result) == 2
            assert "message" in result[1]
            assert obj.load_equity_eod_data.call_count == 1

            obj = EndOfDayData(ExchangeType.NSE)
            obj.can_execute_task = MagicMock(
                return_value=(True, None, last_excution_date)
            )
            obj.load_equity_eod_data = MagicMock(return_value=None)
            obj.load_equity_corporate_action = MagicMock(return_value=None)
            obj.load_equity_derivative_eod_data = MagicMock(return_value=None)
            result = obj.execute_equity_eod_data_task()
            assert result is not None
            assert len(result) == 9
            assert "message" in result[3]
            assert "message" in result[4]
            assert "message" in result[7]
            assert "message" in result[8]
            assert obj.load_equity_eod_data.call_count == 5

            obj = EndOfDayData(ExchangeType.NSE)
            obj.load_equity_eod_data = MagicMock(return_value=None)
            obj.load_equity_corporate_action = MagicMock(return_value=None)
            obj.load_equity_derivative_eod_data = MagicMock(return_value=None)
            result = obj.execute_equity_eod_data_task()
            assert result is not None
            assert len(result) == 1
            assert "message" in result[0]
            obj.load_equity_eod_data.assert_not_called()

        current_date = dt.get_date_time(2022, 10, 27, 22, 15, 0)
        with freeze_time(current_date):
            obj = EndOfDayData(ExchangeType.NSE)
            obj.load_equity_eod_data = MagicMock(return_value=None)
            obj.load_equity_corporate_action = MagicMock(return_value=None)
            obj.load_equity_derivative_eod_data = MagicMock(return_value=None)
            result = obj.execute_equity_eod_data_task()
            assert result is not None
            assert len(result) == 1
            assert obj.load_equity_eod_data.call_count == 1

    @pytest.mark.unittest
    def test_get_queryset_stocks_by_index(self):
        index = conf.get_default_value_by_key("default_index_symbol")

        obj = obj = Screener(ExchangeType.NSE)
        qs = obj.get_queryset_stocks_by_index(index, only_fno=True)
        assert qs.count() > 0
        assert qs.count() < 250

    # @pytest.mark.unittest
    # def test_calculated_eod_data(self):
    #     d = dt.get_date_time(2022, 11, 7)
    #     obj = obj = Screener(ExchangeType.NSE)
    #     obj.stock_screener_hidden_move(d, 50)
