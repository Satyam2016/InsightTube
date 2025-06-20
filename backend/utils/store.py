# utils/store.py

video_analysis_log = []

def store_result(result: dict):
    video_analysis_log.append(result)

def get_all_results():
    return video_analysis_log
