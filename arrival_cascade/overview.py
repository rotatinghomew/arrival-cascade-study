from datetime import datetime


def parse_time(value):
    return datetime.fromisoformat(value)


def summarize(release):
    tables = release["tables"]
    cutoff = release["cutoff"]
    by_site = {}
    for row in tables['arrivals']:
        by_site[row['site']] = by_site.get(row['site'], 0) + 1
    exposure = sum((parse_time(row['end'])-parse_time(row['start'])).total_seconds()/3600 for row in tables['exposure'] if row['observed'])
    return {'arrivals': len(tables['arrivals']), 'by_site': by_site, 'observed_site_hours': exposure, 'known_events': len(tables['events'])}
