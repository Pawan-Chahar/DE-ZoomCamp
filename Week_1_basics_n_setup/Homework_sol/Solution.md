#Prepare Data for Homework Sol.

Ingest data to PostgresSQL

 URL="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet"

  docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
      --user=root \
      --password=root \
      --host=pg_container \
      --port=5432 \
      --db=ny_taxi \
      --table_name=green_taxi_trip_data_2019_10 \
      --url=${URL}



















Question 1. Understanding docker first run
Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.

What's the version of pip in the image?

24.3.1
24.2.1
23.3.1
23.2.1


Answer 1. A

run Docker container
docker run -it --entrypoint bash python:3.12.8

Inside Container Check pip --veriosn
24.3.1


Answer 2. C

for Postgres :
Hostname : postgres 
Port : 5432


green_tripdata_2019-10.csv.gz

taxi_zone_lookup.csv

Answer 3:Trip Segmentation Count

104,838; 199,013; 109,645; 27,688; 35,202

SELECT * FROM public.green_tripdata
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


104,838; 199,013; 109,645; 27,688; 35,202


Answer 4: Longest trip for each day



Answer 5 : Three biggest pickup zones

SELECT count(*) FROM public.green_tripdata
where filename = 'green_tripdata_2019-10.csv'
LIMIT 100

-- Question 3. Trip Segmentation Count
--476386

SELECT * FROM public.green_tripdata
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


--   Question 5. Three biggest pickup zones

East Harlem North, East Harlem South, Morningside Heights


















Answer 6 : Largest tip

East Harlem South

#Terraform:

terraform init ,  terraform apply -auto-approve , terraform destroy




