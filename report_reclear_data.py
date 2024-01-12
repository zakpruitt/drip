from dtos.performance_type import PerformanceType
from dtos.player_fight_parse_performance import PlayerFightParsePerformance
from game_spell_utility import GameSpellUtility
from warcraft_logs_api import WarcraftLogsAPI


class ReportReclearData:
    def __init__(self, report_code, character_name_id_map):
        self.report_code = report_code
        self.character_name_id_map = character_name_id_map
        self.kill_ids = self._initialize_kill_ids()
        self.dps_data = {}
        self.hps_data = {}
        self.bossdps_data = {}
        self.defensive_data = {}

    def _initialize_kill_ids(self):
        kill_id_response = WarcraftLogsAPI.query_kill_ids(self.report_code)
        fights = kill_id_response["data"]["reportData"]["report"]["fights"]
        return [fight["id"] for fight in fights]

    def _process_parse_data(self, response_parse_data, performance_type):
        # get data attribute dynamically
        data_attribute = getattr(self, f"{performance_type.value}_data")

        for fight in response_parse_data['data']['reportData']['report']['rankings']['data']:
            # initialize each encounter in the dictionary
            encounter_name = fight['encounter']['name']
            if encounter_name not in data_attribute:
                data_attribute[encounter_name] = []

            # parse individual performance and append to dictionary's list value
            for role in fight['roles'].values():
                for character in role['characters']:
                    player = PlayerFightParsePerformance(
                        name=character['name'],
                        player_class=character['class'],
                        player_spec=character['spec'],
                        rank_percent=character['rankPercent'],
                        amount=character['amount'],
                        performance_type=performance_type
                    )
                    data_attribute[encounter_name].append(player)

    def _process_defensive_data(self, response_defensive_data):
        for event in response_defensive_data["data"]["reportData"]["report"]["events"]["data"]:
            character_name = self.character_name_id_map[event["sourceID"]]
            spell_name = GameSpellUtility.get_spell_name_from_id(event["abilityGameID"])

            # initialize nested dictionary for character_name if it doesn't exist for the encounter
            if character_name not in self.defensive_data:
                self.defensive_data[character_name] = {}

            # Count the ability casts
            if spell_name not in self.defensive_data[character_name]:
                self.defensive_data[character_name][spell_name] = 0
            self.defensive_data[character_name][spell_name] += 1

    def query_and_process(self):
        reclear_parse_data = WarcraftLogsAPI.query_mythic_reclear_parse_stats(self.report_code)
        defensive_data = WarcraftLogsAPI.query_defensive_casts(self.report_code, self.kill_ids)
        for performance_type in PerformanceType:
            self._process_parse_data(reclear_parse_data[performance_type.value], performance_type)
        self._process_defensive_data(defensive_data)
