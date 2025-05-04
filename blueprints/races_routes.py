from flask import Blueprint, jsonify
from services.schedule_client import ScheduleClient
from services.get_holidays_usecase import GetHolidaysUsecase
from services.special_client import SpecialClient
from services.race_result_client import RaceResultClient

races_bp = Blueprint('races', __name__, url_prefix='/api/races')

@races_bp.route('/g_race', methods=['GET'])
def get_topic_race():
    ## http://127.0.0.1:5000/api/races/g_race
    try:
        days = GetHolidaysUsecase().execute()
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
        race_result = RaceResultClient().get_race_results(past_race_ids)
       
        return jsonify({"data": "Success"})
    except Exception as e:
        return jsonify({
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(e)
            }
        }), 500
