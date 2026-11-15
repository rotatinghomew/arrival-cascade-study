from datetime import datetime


def parse_time(value):
    return datetime.fromisoformat(value)


def operate(path, payload, release):
    if path != '/v1/window-check':
        raise LookupError('时窗接口不存在')
    start,end = parse_time(payload['start']),parse_time(payload['end'])
    if end <= start:
        raise ValueError('时窗为空')
    seconds = sum(max(0,(min(end,parse_time(row['end']))-max(start,parse_time(row['start']))).total_seconds()) for row in release['tables']['exposure'] if row['site']==payload['site'] and row['observed'])
    events = [row for row in release['tables']['events'] if row['site']==payload['site'] and parse_time(row['start'])<end and parse_time(row['end'])>start]
    return {'observed_seconds':seconds,'events':events}
