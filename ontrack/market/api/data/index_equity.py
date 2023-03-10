import array
import json
from urllib.request import urlopen

import yaml

from ontrack.lookup.api.logic.settings import SettingLogic
from ontrack.market.models.lookup import Exchange
from ontrack.utils.base.tasks import TaskProgressStatus
from ontrack.utils.config import Configurations
from ontrack.utils.datetime import DateTimeHelper as dt
from ontrack.utils.filesystem import FileSystemHelper


class PullEquityIndexData:
    def __init__(
        self,
        exchange: Exchange = None,
        equity_dict: dict = None,
        index_dict: dict = None,
        equityindex_dict: dict = None,
        tp: TaskProgressStatus = None,
    ):
        self.exchange = exchange
        self.timezone = exchange.timezone_name
        self.urls = Configurations.get_urls_config()
        self.settings = SettingLogic()

        self.index_dict = index_dict
        self.equity_dict = equity_dict
        self.equityindex_dict = equityindex_dict
        self.tp = tp

    def __get_name_from_label(self, label: str) -> str:
        # remove only the last instance of space
        result = label.rsplit(" ", 1)
        return result[0].strip()

    def __process_record(
        self, index_symbol: str, record: dict, parent: dict = None
    ) -> dict:

        equity_symbol = self.__get_name_from_label(record["label"])
        weight = record["weight"]

        index = [e for e in self.index_dict if e.symbol.lower() == index_symbol.lower()]
        if len(index) == 0:
            self.tp.log_warning(f"Index '{index_symbol}' doesn't exists")
            return None
        index = index[0]

        equity = [
            e for e in self.equity_dict if e.symbol.lower() == equity_symbol.lower()
        ]
        if len(equity) == 0:
            self.tp.log_warning(f"Equity '{equity_symbol}' doesn't exists")
            return None
        equity = equity[0]

        pk = None
        existing_entity = [
            e
            for e in self.equityindex_dict
            if e.index.symbol.lower() == index_symbol.lower()
            and e.equity.symbol.lower() == equity_symbol.lower()
        ]
        if len(existing_entity) > 0:
            pk = existing_entity[0].id

        entity = {}
        entity["id"] = pk
        entity["index"] = index
        entity["equity"] = equity
        entity["equity_weightage"] = weight
        entity["date"] = dt.current_date_time()
        entity["updated_at"] = dt.current_date_time()

        if parent is not None:
            label = self.__get_name_from_label(parent["label"])
            weight = parent["weight"]
            entity["sector"] = label
            entity["sector_weightage"] = weight

        return entity

    def __parse_webContent(self, webpage, url_temp):
        content = (
            webpage.read()
            .decode()
            .replace("'", "||||")
            .replace("modelDataAvailable(", "[")
            .replace(");", "]")
            .replace("label:", '"label":')
            .replace("label:", '"label":')
            .replace("file:", '"file":')
        )

        with open(url_temp, "w") as file_intermediate:
            # Writing the replaced data in our
            # text file
            json_content = json.dumps(content, ensure_ascii=True, indent=4)
            json_content = json_content.replace('\\"', '"')[1:-1]
            file_intermediate.write(json_content)

        with open(url_temp) as file_intermediate2:
            # Writing the replaced data in our
            # text file
            data = yaml.safe_load(file_intermediate2)

        with open(url_temp, "w") as file_final:
            # Writing the replaced data in our
            # text file
            file_final.write(str(data).replace("'", '"').replace("||||", "'"))

        with open(url_temp) as file_final2:
            # Writing the replaced data in our
            # text file
            return json.load(file_final2)

    def pull_indices_market_cap(self, record: dict):
        temp_folder = FileSystemHelper.create_temp_folder("IndexWeightage")

        if "url" not in record:
            self.tp.log_warning("No url exists for '%s'." % record["name"])
            return None

        # get indices details
        index_url = record["url"]
        index_name = str(record["name"])
        sector_name_file_name = index_name.replace(" ", "_")
        url_temp = f"{temp_folder}/{sector_name_file_name}_temp.json"

        self.tp.log_message(f"Started with {index_name}, {index_url}.", index_name)

        try:
            with urlopen(index_url) as webpage:
                result = self.__parse_webContent(webpage, url_temp)

        except Exception as e:
            message = f"Exception from pull indices {index_url} - `{format(e)}`."
            self.tp.log_error(message=message)
            raise

        return result

    def parse_indices_market_cap(self, index_name: str, record: dict) -> array:
        entities = []

        for ogroup in record["groups"]:

            # remove extra spaces in the dictionaty keys
            record = {k.strip(): v for (k, v) in record.items()}

            if "groups" in ogroup:
                for igroup in ogroup["groups"]:
                    entity = self.__process_record(index_name, igroup, ogroup)
                    if entity is not None:
                        entities.append(entity)
            else:
                entity = self.__process_record(index_name, ogroup, None)
                if entity is not None:
                    entities.append(entity)

        return entities

    def pull_and_parse_market_cap(self):
        urls = Configurations.get_urls_config()

        indices_percentage_urls = urls["indices_percentage"]

        results = []
        for record in indices_percentage_urls:
            weightage_obj = self.pull_indices_market_cap(record)

            if "url" not in record:
                continue

            else:
                results += self.parse_indices_market_cap(
                    record["symbol"], weightage_obj[0]
                )

        return results
