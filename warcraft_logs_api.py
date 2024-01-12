import requests
import os

from dotenv import load_dotenv

load_dotenv()


class WarcraftLogsAPI:
    AUTH_URL = os.environ.get("WARCRAFTLOGS_AUTH_URL")
    GRAPHQL_URL = os.environ.get("WARCRAFTLOGS_GRAPHQL_URL")
    CLIENT_ID = os.environ.get("WARCRAFTLOGS_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("WARCRAFTLOGS_CLIENT_SECRET")
    ACCESS_TOKEN = None

    @staticmethod
    def _get_access_token():
        payload = {
            "grant_type": "client_credentials",
            "client_id": WarcraftLogsAPI.CLIENT_ID,
            "client_secret": WarcraftLogsAPI.CLIENT_SECRET
        }
        response = requests.post(WarcraftLogsAPI.AUTH_URL, data=payload)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception("Failed to obtain access token")

    @staticmethod
    def _load_query(file_name, **kwargs):
        with open(f"./resources/queries/{file_name}", 'r') as file:
            return file.read().format(**kwargs)

    @staticmethod
    def query(graphql_query):
        if WarcraftLogsAPI.ACCESS_TOKEN is None:
            WarcraftLogsAPI.ACCESS_TOKEN = WarcraftLogsAPI._get_access_token()

        headers = {
            "Authorization": f"Bearer {WarcraftLogsAPI.ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.post(WarcraftLogsAPI.GRAPHQL_URL, json={"query": graphql_query}, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Query failed")

    @staticmethod
    def query_spell_information(spell_id):
        query = WarcraftLogsAPI._load_query("spell_information_query.txt",
                                            spell_id=spell_id)
        return WarcraftLogsAPI.query(query)

    @staticmethod
    def query_player_actor_data(report_code):
        query = WarcraftLogsAPI._load_query("player_actor_data.txt",
                                            report_code=report_code)
        return WarcraftLogsAPI.query(query)

    @staticmethod
    def query_kill_ids(report_code):
        query = WarcraftLogsAPI._load_query("kill_fight_ids_query.txt",
                                            report_code=report_code)
        return WarcraftLogsAPI.query(query)

    @staticmethod
    def query_mythic_reclear_parse_stats(report_code):
        responses = {}
        for player_metric in ['dps', 'hps', 'bossdps']:
            query = WarcraftLogsAPI._load_query("reclear_stats_query.txt",
                                                report_code=report_code,
                                                difficulty="5",
                                                player_metric=player_metric)
            response = WarcraftLogsAPI.query(query)
            responses[player_metric] = response
        return responses

    @staticmethod
    def query_defensive_casts(report_code, fight_ids):
        fight_ids_str = ", ".join(map(str, fight_ids))
        query = WarcraftLogsAPI._load_query("defensive_cast_count_query.txt",
                                            report_code=report_code,
                                            fight_ids=fight_ids_str)
        return WarcraftLogsAPI.query(query)
