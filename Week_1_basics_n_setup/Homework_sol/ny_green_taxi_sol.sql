
-- Question 3. Trip Segmentation Count
--476386

SELECT Count(*) FROM public.green_tripdata
where filename = 'green_tripdata_2019-10.csv'
and trip_distance <= 1     -- 104838



SELECT Count(*) FROM public.green_tripdata
where filename = 'green_tripdata_2019-10.csv'
and (trip_distance >1 and trip_distance <= 3);



SELECT Count(*) FROM public.green_tripdata
where filename = 'green_tripdata_2019-10.csv'
and (trip_distance >3 and trip_distance <= 7);


SELECT Count(*) FROM public.green_tripdata
where filename = 'green_tripdata_2019-10.csv'
and (trip_distance >7 and trip_distance <= 10);

SELECT Count(*) FROM public.green_tripdata
where filename = 'green_tripdata_2019-10.csv'
and (trip_distance > 10) ;



-- Question 4. Longest trip for each day

With single_trip_longest as
(
SELECT Date(lpep_pickup_datetime) as date, max(trip_distance) as max_trip_distance  FROM public.green_tripdata
where filename = 'green_tripdata_2019-10.csv'
group by date(lpep_pickup_datetime)

)
select date from single_trip_longest 
order by max_trip_distance desc
limit 1

OutPuts:

"2019-10-31"

--   Question 5. Three biggest pickup zones




with green_tripdata_2019_10 as 
(
SELECT  *
FROM public.green_tripdata as tr
where filename = 'green_tripdata_2019-10.csv' and Date(lpep_pickup_datetime) = '2019-10-18'
)
, top_pickup_location as
(
SELECT
    lpep_pickup_datetime,
    lpep_dropoff_datetime,
    total_amount,
	sum(total_amount)  over(partition by CONCAT(zpu.Borough, ' | ', zpu.Zone) ) as total_zone_amount ,
	zpu.Zone as puzone ,
    CONCAT(zpu.Borough, ' | ', zpu.Zone) AS "pickup_loc",
    CONCAT(zdo.Borough, ' | ', zdo.Zone) AS "dropoff_loc"
FROM 
    green_tripdata_2019_10 t
JOIN 

    public.taxi_zone_lookup zpu 
	ON t.pulocationid::numeric = zpu.locationid
JOIN
    public.taxi_zone_lookup zdo 
	ON t.dolocationid::numeric = zdo.locationid
	)
Select puzone , total_zone_amount
from top_pickup_location
where total_zone_amount > 13000
Group by puzone , total_zone_amount
order by total_zone_amount desc

OutPuts:

"East Harlem North"	18686.679999999727
"East Harlem South"	16797.259999999762
"Morningside Heights"	13029.789999999935

-- select * from public.taxi_zone_lookup;

-- select * from public.dim_zones;

-- select * from public.taxi_zone_lookup ;


-- Question 6. Largest tip





with green_tripdata_2019_10 as 
(
SELECT  *
FROM public.green_tripdata as tr
where filename = 'green_tripdata_2019-10.csv' --and Date(lpep_pickup_datetime) = '2019-10-18'
)
, max_tip_drop_location as
(
SELECT
    lpep_pickup_datetime,
    lpep_dropoff_datetime,
    tip_amount,
	max(tip_amount)  over(partition by  zpu.Zone , zdo.Zone ) as max_tip_amount ,
	zpu.Zone as pickup_zone,
	zdo.Zone as drop_zone ,
    CONCAT(zpu.Borough, ' | ', zpu.Zone) AS "pickup_loc",
    CONCAT(zdo.Borough, ' | ', zdo.Zone) AS "dropoff_loc"
FROM 
    green_tripdata_2019_10 t
JOIN 

    public.taxi_zone_lookup zpu 
	ON t.pulocationid::numeric = zpu.locationid
JOIN
    public.taxi_zone_lookup zdo 
	ON t.dolocationid::numeric = zdo.locationid
	
	)
	,max_tip_drop_zone as
	(
	select max_tip_amount ,pickup_zone ,drop_zone 
	from max_tip_drop_location
	where pickup_zone = 'East Harlem North'
	Group by max_tip_amount ,pickup_zone ,drop_zone
	order by max_tip_amount desc
)
select drop_zone  from max_tip_drop_zone 
where max_tip_amount= (select max(max_tip_amount) from max_tip_drop_zone) ;


OutPuts:


"JFK Airport"