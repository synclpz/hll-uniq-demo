# hll-uniq-demo

## Scenario

Load gen (`producer.py`) sends events like:

```json
{
    "timestamp": <utc seconds>,
    "cookie": <random string>
}
```
to Kafka topic `requests`, which is read by CH engine, then aggregated through Materialized View `requests_uniq_daily_view` to AggregatingMergeTree table, which stores HyperLogLog states for each day.

Grafana dashboard allows querying aggregation table. One can create any graphs using `uniqCobmined64Merge(uniq)` on aggregated table due to commutative property of HLL state.

Each day (one HLL state) costs ~100KB storage.

## Requirements

* Python 3
* pipenv
* docker
* docker-compose

## Run

From project directory run:

```
./start.sh
```
After loading data navigate to http://localhost:3000 and check dashboard "Uniq", it should be able to show last 30 days of data ~10k uniq events per day.

```
./stop.sh
```
All containers stop, you need to purge venv manually.

