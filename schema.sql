DROP TABLE IF EXISTS requests;

CREATE TABLE requests
(
  timestamp UInt64,
  cookie String
) ENGINE  = Kafka()
SETTINGS
    kafka_broker_list = 'kafka:9093',
    kafka_topic_list = 'requests',
    kafka_group_name = 'ch-group',
    kafka_format = 'JSONEachRow';

DROP TABLE IF EXISTS requests_uniq_daily;

CREATE TABLE requests_uniq_daily
(
  date Date,
  uniq AggregateFunction(uniqCombined64, String)
) ENGINE  = AggregatingMergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date);

DROP VIEW IF EXISTS requests_uniq_daily_view;

CREATE MATERIALIZED VIEW requests_uniq_daily_view TO requests_uniq_daily
AS SELECT 
    toDate(timestamp) AS date, 
    uniqCombined64State(cookie) AS uniq
FROM requests
GROUP BY date
