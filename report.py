from report_reclear_data import ReportReclearData
from warcraft_logs_api import WarcraftLogsAPI


class Report:
    def __init__(self, report_code):
        self.report_code = report_code
        self.character_name_id_map = self._initialize_character_map()
        self.reclear_data = ReportReclearData(self.report_code, self.character_name_id_map)
        self.progression_data = None

    def _initialize_character_map(self):
        player_actor_data = WarcraftLogsAPI.query_player_actor_data(self.report_code)
        actors = player_actor_data["data"]["reportData"]["report"]["masterData"]["actors"]
        return {actor["id"]: actor["name"] for actor in actors}


report = Report(report_code="7PWLT4pzRMma8dnb")
report.reclear_data.query_and_process()


print(report)