from typing import List
import datetime

def create_performance_message(new_performance:List[map]) -> str:
    '''
        成績が更新された時刻と内容を合わせてメッセージを作成する

        Args:
            new_performance (List[map]): 更新された成績
        
        Returns:
            str:  成績が更新された時刻と内容を合わせたメッセージ

    '''
    get_time = str(datetime.datetime.now())
    get_time = get_time[:str(datetime.datetime.now()).find(".")]
    get_time = get_time.replace(" ","  ")
    message = "----------自動更新----------\n"
    message += "取得時間：" + get_time + "\n"
    message += "以下の教科の成績が更新されました\n"

    for performance in new_performance:
        message += "\n" + performance[0]
    
    return message