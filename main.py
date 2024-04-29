import math
import pandas as pd
import sys

try:
    logs = pd.read_csv("logs.csv", thousands=",")
    players = pd.read_csv("players.csv", thousands=",")
    
    # エントリーしたplayerのみとする
    filtered_logs = logs[logs["player_id"].isin(players["player_id"])]
    
    # player_idごとにMaxスコアのみにする
    max_logs = filtered_logs.groupby("player_id", as_index=False).agg({"score":"max"})
    
    # スコアが同じ場合、player_idで降順にするため、先にソート
    sorted_logs_temp = max_logs.sort_values("player_id", ignore_index=True)
    sorted_logs = sorted_logs_temp.sort_values("score", ascending=False, ignore_index=True)
    
    # スコア起点でRankを付与
    sorted_logs["rank"] = sorted_logs.rank(numeric_only=True, ascending=False, method='min')
    
    # ハンドルネームを突合する
    sorted_logs_merged = pd.merge(sorted_logs, players, on="player_id", how="left")
    
    # 10行目以降は順位が同じ場合のみ出力
    for index, row in sorted_logs_merged.iterrows():
        if index <= 9:
            elements = [str(math.floor(row["rank"])), str(row["player_id"]), str(row["handle_name"]), str(row["score"])]
            print(','.join(elements))
            pre_rank = row["rank"]
        else:
            if row["rank"] == pre_rank:
                elements = [str(row["rank"]), str(row["player_id"]), str(row["handle_name"]), str(row["score"])]
                print(','.join(elements))
            else:
                break
except Exception as e:
    sys.exit()
