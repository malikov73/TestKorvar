## Start postgresql

```console
docker run \
    --name postgres14 \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_USER=user_local \
    -e POSTGRES_DB=korvax_test_db \
    -p 5432:5432 \
    -d postgres:14.2-alpine 
```

## Generate random data for local test

```postgresql
INSERT INTO page_views (site_id, page_id, host_ip, visit_time)
select (100 * random())::int + 1,
       (100 * random())::int + 1,
       CONCAT(
               TRUNC(RANDOM() * 250 + 2), '.',
               TRUNC(RANDOM() * 250 + 2), '.',
               TRUNC(RANDOM() * 250 + 2), '.',
               TRUNC(RANDOM() * 250 + 2)
           )::inet,
       (NOW() + random() * INTERVAL '10 days') - INTERVAL '11 days'
from generate_series(1, 100000)
```

## Tasks

### 1. Write a query to show the total count per site_id and page_id for the last two months.

```postgresql
SELECT page_id, site_id, count(1) as count_view
FROM page_views
WHERE page_id = $page_id
  and site_id = $site_id
  and visit_time > NOW() - INTERVAL '2 months'
GROUP BY page_id, site_id
```

### 2. Create a table (daily_page_visits) for holding daily pre-aggregated data for the page visits count, grouped by site_id, page_id and day

```postgresql
CREATE TABLE daily_page_visits
(
    site_id   int,
    page_id   int,
    visit_day date,
    count     int,
    PRIMARY KEY (site_id, page_id, visit_day)
);
CREATE INDEX daily_page_site_id_idx ON daily_page_visits (site_id);
```

### 3. Create a function for populating the pre-aggregated table every hour (you can use a helper table to holld the last update time);

```postgresql
CREATE TABLE helper_pre_aggregate_table
(
    name        regclass primary key,
    last_update timestamp
);
INSERT INTO helper_pre_aggregate_table
VALUES ('daily_page_visits', now());

CREATE OR REPLACE FUNCTION pre_aggregate_daily_page_visits()
    RETURNS void
    LANGUAGE plpgsql
AS
$function$
DECLARE
    start_time timestamp;
    end_time   timestamp := now() - interval '1 minute';
BEGIN
    SELECT last_update
    INTO start_time
    FROM helper_pre_aggregate_table
    WHERE name = 'daily_page_visits'::regclass;
    UPDATE
        helper_pre_aggregate_table
    SET last_update = end_time
    WHERE name = 'daily_page_visits'::regclass;
    EXECUTE $$
      INSERT INTO daily_page_visits (site_id, visit_day, page_id, "count")
      SELECT site_id, visit_time::date AS visit_day, page_id, count(*) AS "count"
      FROM page_views
      WHERE visit_time >= $1 AND visit_time < $2
      GROUP BY site_id, visit_time::date, page_id
      ON CONFLICT (site_id, visit_day, page_id) DO UPDATE SET
      "count" = daily_page_visits.count + EXCLUDED.count$$
        USING start_time,
            end_time;
END;
$function$;
```

I would set up cron via celery and call the function every hour, alternative to pg_cron, but not sure how good it is.

### 4. Write a query to show the total count per site_id and page_id for the last two months until now, using the the both big and pre-aggregated tables.

```postgresql
SELECT page_id,
       site_id,
       sum(count) AS count
FROM (
         SELECT page_id,
                site_id,
                count(1) AS count
         FROM page_views
         WHERE visit_time > NOW() - INTERVAL '2 months'
           AND visit_time > (
             SELECT last_update
             FROM helper_pre_aggregate_table
             WHERE name = 'daily_page_visits'::regclass)
         GROUP BY page_id,
                  site_id
         UNION
         SELECT page_id,
                site_id,
                sum(count) AS "count"
         FROM daily_page_visits
         WHERE visit_day::TIMESTAMP > NOW() - INTERVAL '2 months'
         GROUP BY page_id,
                  site_id) AS union_daily_page_visits
GROUP BY page_id,
         site_id
```

alternative

```postgresql
SELECT pre_aggregate_daily_page_visits();
SELECT page_id,
       site_id,
       sum(count) AS "count"
FROM daily_page_visits
WHERE visit_day::TIMESTAMP > NOW() - INTERVAL '2 months'
GROUP BY page_id,
         site_id
```