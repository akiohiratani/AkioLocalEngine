from flask import Blueprint, jsonify, request
from services.schedule_client import ScheduleClient
from services.usecase import Usecase
from services.special_client import SpecialClient
from services.race_result_client import RaceResultClient
from services.export_race_data import ExportRaceData
from services.horce_client import HorseClient
from services.race_client import RaceClient
from services.jockey_client import JockeyClient
from services.base.dataset_type import DatasetType
import time

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
    
@races_bp.route('/data', methods=['POST'])
def output_topic_race():
    ## http://127.0.0.1:5000/api/races/data
    try:
        data = request.get_json()  # JSONデータを取得
        id = data.get('id')      # 'id'キーの値（配列）を取り出す
        years = data.get('years')      # 'years'キーの値（配列）を取り出す

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
        train_race_ids = specialClient.get_past_race_ids(id, years)

        ## 過去分のレース結果取得
        train_race_results = RaceResultClient().get_race_results(train_race_ids)

        ## 過去に出走した競走馬リストを取得
        train_horse_ids = Usecase().get_horse_ids(train_race_results)
        train_horses = horseClient.get_horses(train_horse_ids)

        ## csv出力
        exportRaceData = ExportRaceData()
        exportRaceData.export_candidate_list(candidate_list, DatasetType.TEST)
        exportRaceData.export_horse_history(test_horse, DatasetType.TEST)
        exportRaceData.export_past_race_data_to_csv(train_race_results, DatasetType.TRAIN)
        exportRaceData.export_horse_history(train_horses, DatasetType.TRAIN)
        exportRaceData.compress_output()
        result = exportRaceData.get_output_path()
        return jsonify({"data": result + ".zip"})
    except Exception as e:
        return jsonify({
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(e)
            }
        }), 500
    
@races_bp.route('/calculation', methods=['POST'])
def get_processing_time():
    data = request.get_json()  # JSONデータを取得
    id = data.get('id')      # 'id'キーの値（配列）を取り出す
    executions = data.get('executions')      # 'years'キーの値（配列）を取り出す
    start = time.perf_counter()
    specialClient = SpecialClient()
    raceClient = RaceClient()
    horseClient = HorseClient()

    # 検証用・テスト用データ作成

    ## 今回出走する、競走馬の取得
    race_id = specialClient.get_race_id(id)
    test_horse_ids = raceClient.get_horse_ids(race_id)
    horseClient.get_horses(test_horse_ids)

    ## 出馬表の取得
    raceClient.get_candidate_list(race_id)

    # 学習用データ作成
    ## 過去分のレースid取得
    train_race_ids = specialClient.get_past_race_ids(id, 1)

    ## 過去分のレース結果取得
    train_race_results = RaceResultClient().get_race_results(train_race_ids)

    ## 過去に出走した競走馬リストを取得
    train_horse_ids = Usecase().get_horse_ids(train_race_results)
    horseClient.get_horses(train_horse_ids)

    end = time.perf_counter()

    first_time = end - start

    estimated_time = first_time + (executions - 1) * 21.79

    return jsonify({"data": estimated_time})