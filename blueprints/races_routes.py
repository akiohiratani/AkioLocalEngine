from flask import Blueprint, jsonify, request
from services.schedule_client import ScheduleClient
from services.usecase import Usecase
from services.special_client import SpecialClient
from services.race_result_client import RaceResultClient
from services.export_race_data import ExportRaceData
from services.horce_client import HorseClient
from services.race_client import RaceClient
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
        name = data.get('name')      # 'years'キーの値（配列）を取り出す

        specialClient = SpecialClient()
        raceClient = RaceClient()

        ## 今回出走する、競走馬の取得
        race_id = specialClient.get_race_id(id)

        ## 出走馬情報を取得
        candidate_list = raceClient.get_candidate_list(race_id)

        ## 出走馬のID取得
        candidate_horse_ids = [candidate.horse_id for candidate in candidate_list]
        candidate_horses = HorseClient().get_horses(candidate_horse_ids)

        # 学習用データ作成
        ## 過去分のレースid取得
        train_race_ids = specialClient.get_past_race_ids(id, years)

        ## 過去分のレース結果取得
        train_race_results = RaceResultClient().get_race_results(train_race_ids)

        train_race_results.extend(candidate_list)

        ## csv出力
        exportRaceData = ExportRaceData()
        exportRaceData.export_past_race_data_to_csv(f'{name}_{years}年分の分析データ', train_race_results)
        exportRaceData.export_horse_history(f'{name}_出走する馬の戦歴データ', candidate_horses)
        result = exportRaceData.get_output_path()
        return jsonify({"data": result})
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

    ## 今回出走する、競走馬の取得
    race_id = specialClient.get_race_id(id)

    ## 出走馬情報を取得
    candidate_list = raceClient.get_candidate_list(race_id)

    ## 出走馬のID取得
    candidate_horse_ids = [candidate.horse_id for candidate in candidate_list]
    HorseClient().get_horses(candidate_horse_ids)

    # 学習用データ作成
    ## 過去分のレースid取得
    train_race_ids = specialClient.get_past_race_ids(id, 1)

    ## 過去分のレース結果取得
    train_race_results = RaceResultClient().get_race_results(train_race_ids)

    train_race_results.extend(candidate_list)

    end = time.perf_counter()

    first_time = end - start
    # print("---初期開始時間---")
    # print(first_time)
    # print("-----------------")

    estimated_time = (0.5636*executions*executions) + (1.379*executions) + first_time

    return jsonify({"data": estimated_time})