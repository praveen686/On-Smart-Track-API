import pytest

from ontrack.market.api.data.index_equity import PullEquityIndexData
from ontrack.market.api.logic.lookup import MarketLookupData
from ontrack.market.models.lookup import Equity, EquityIndex, Exchange, Index
from ontrack.utils.config import Configurations


class TestPullEquityIndexData:
    @pytest.fixture(autouse=True)
    def injector(self):
        self.exchange_qs = Exchange.backend.get_queryset()
        self.index_qs = Index.backend.get_queryset()
        self.equity_qs = Equity.backend.get_queryset()
        self.equityindex_qs = EquityIndex.backend.get_queryset()

    @pytest.fixture(autouse=True)
    def equity_index_data_fixture(self, exchange_fixture):
        self.marketlookupdata = MarketLookupData(exchange_fixture.symbol)
        self.marketlookupdata.load_equity_data()
        self.marketlookupdata.load_index_data()

    def __pull_indices_market_cap(self, index_symbol):
        urls = Configurations.get_urls_config()

        datapull_obj = PullEquityIndexData(
            self.exchange_qs, self.index_qs, self.equity_qs, self.equityindex_qs
        )
        indices_percentage_urls = urls["indices_percentage"]
        record = [x for x in indices_percentage_urls if x["symbol"] == index_symbol][0]
        weightage_obj = datapull_obj.pull_indices_market_cap(record)

        if "url" not in record:
            assert weightage_obj is None

        else:
            assert weightage_obj is not None
            assert len(weightage_obj) == 2

            records = datapull_obj.parse_indices_market_cap(
                record["symbol"], weightage_obj[0]
            )
            assert records is not None
            assert len(records) > 0

    @pytest.mark.lookup_data
    @pytest.mark.integration
    @pytest.mark.slow
    def test_pull_indices_market_cap_all(self):
        urls = Configurations.get_urls_config()

        indices_percentage_urls = urls["indices_percentage"]
        for record in indices_percentage_urls:
            self.__pull_indices_market_cap(record["symbol"])