from flask import Blueprint, jsonify
from services.schedule_client import ScheduleClient
from services.usecase import Usecase
from services.special_client import SpecialClient
from services.race_result_client import RaceResultClient
from services.export_race_data import ExportRaceData
from services.horce_client import HorseClient
from services.jockey_client import JockeyClient

races_bp = Blueprint('races', __name__, url_prefix='/api/races')

@races_bp.route('/g_race', methods=['GET'])
def get_topic_race():
    ## http://127.0.0.1:5000/api/races/g_race
    try:
        days = Usecase().get_holidays()
        race_list = ScheduleClient().search_g_race_list(days)
        return jsonify({
            "data": [r.to_dict() for r in race_list],
            "meta": {"total": len(race_list)}
        }), 200
    except Exception as e:
        return jsonify({
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(e)
            }
        }), 500
    
@races_bp.route('/data', methods=['GET'])
def output_topic_race():
    ## http://127.0.0.1:5000/api/races/data
    try:
        id = "0052"
        specialClient = SpecialClient()

        race_id = specialClient.get_race_id(id)
        ## 10年分のレースid取得
        past_race_ids = specialClient.get_past_race_ids(id)

        ## 10年分のレース結果取得
        race_results = RaceResultClient().get_race_results(past_race_ids)

        ## 出走した競走馬リストを取得
        horse_ids = Usecase().get_horse_ids(race_results)
        horses = HorseClient().get_horses(horse_ids)

        ## 出走した騎手リストを取得
        joceky_ids = Usecase().get_joceky_ids(race_results)
        jos = JockeyClient().get_jockeys(joceky_ids)

        ## csv出力
        exportRaceData = ExportRaceData()
        result = exportRaceData.export_past_race_data_to_csv(race_results)
        result = exportRaceData.export_horse_history(horses)

        return jsonify({"data": result})
    except Exception as e:
        return jsonify({
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(e)
            }
        }), 500
