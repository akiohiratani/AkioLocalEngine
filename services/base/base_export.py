import os
import zipfile
import shutil
import pandas as pd
import numpy as np
import datetime
from pathlib import Path
from dataclasses import asdict
from typing import List

class ExportBase:
    def __init__(self):
        # フォルダ名の時刻を確定
        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_name = date_str + "_HorseInfomainon"
        # ダウウンロード先のパス確定
        user_folder = os.path.expanduser("~")
        download_folder = os.path.join(user_folder, "Downloads")
        self.output_path = os.path.join(download_folder, folder_name)
        out_dir = Path(self.output_path)
        out_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = out_dir
        
    def compress_output(self):
        zip_path = self.output_dir.parent / f'{self.output_dir.name}.zip'
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.output_dir.glob('*'):
                if file_path.is_file():
                    zipf.write(file_path, arcname=file_path.name)

        # 圧縮が終わったら元フォルダを削除
        shutil.rmtree(self.output_dir)
    def get_output_path(self):
        return self.output_path