import json

from warcraft_logs_api import WarcraftLogsAPI


class GameSpellUtility:
    spell_id_map = None

    @staticmethod
    def _load_spell_id_map():
        if GameSpellUtility.spell_id_map is None:
            try:
                with open('./resource/data/spell_id_cache.json', 'r') as file:
                    GameSpellUtility.spell_id_map = json.load(file)
            except FileNotFoundError:
                GameSpellUtility.spell_id_map = {}

    @staticmethod
    def _save_spell_id_map():
        with open('./resources/data/spell_id_cache.json', 'w') as file:
            json.dump(GameSpellUtility.spell_id_map, file, indent=4)

    @staticmethod
    def get_spell_name_from_id(spell_id):
        # if spell found in map, return it
        GameSpellUtility._load_spell_id_map()
        if spell_id in GameSpellUtility.spell_id_map:
            return GameSpellUtility.spell_id_map[spell_id]

        # otherwise, query the data from the API and save it to the cache
        try:
            api_response = WarcraftLogsAPI.query_spell_information(spell_id)
            spell_name = api_response['data']['gameData']['ability']['name']
            GameSpellUtility.spell_id_map[spell_id] = spell_name
            GameSpellUtility._save_spell_id_map()
        except Exception as e:
            raise Exception("Error querying spell information: " + str(e))

        return spell_name
