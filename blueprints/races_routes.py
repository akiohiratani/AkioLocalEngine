from flask import Blueprint, jsonify
from services.schedule_client import ScheduleClient
from services.usecase import Usecase
from services.special_client import SpecialClient
from services.race_result_client import RaceResultClient
from services.export_race_data import ExportRaceData
from services.horce_client import HorseClient
from services.race_client import RaceClient
from services.jockey_client import JockeyClient
from services.base.dataset_type import DatasetType

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
        raceClient = RaceClient()
        horseClient = HorseClient()

        # 検証用・テスト用データ作成

        ## 今回出走する、競走馬の取得
        race_id = specialClient.get_race_id(id)
        test_horse_ids = raceClient.get_horse_ids(race_id)
        test_horse = horseClient.get_horses(test_horse_ids)

        ## 出馬表の取得
        candidate_list = raceClient.get_candidate_list(race_id)

        # 学習用データ作成
        ## 過去分のレースid取得
        train_race_ids = specialClient.get_past_race_ids(id)

        ## 過去分のレース結果取得
        train_race_results = RaceResultClient().get_race_results(train_race_ids)

        ## 過去に出走した競走馬リストを取得
        train_horse_ids = Usecase().get_horse_ids(train_race_results)
        train_horses = horseClient.get_horses(train_horse_ids)

        ## csv出力
        exportRaceData = ExportRaceData()
        result = exportRaceData.export_candidate_list(candidate_list, DatasetType.TEST)
        result = exportRaceData.export_horse_history(test_horse, DatasetType.TEST)
        result = exportRaceData.export_past_race_data_to_csv(train_race_results, DatasetType.TRAIN)
        result = exportRaceData.export_horse_history(train_horses, DatasetType.TRAIN)
        exportRaceData.compress_output()
        
        return jsonify({"data": result})
    except Exception as e:
        return jsonify({
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(e)
            }
        }), 500
