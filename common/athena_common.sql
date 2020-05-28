
-- adding non-hive-style partitions
ALTER TABLE manual_mod ADD PARTITION (partition_0 = 'layer', partition_1 = '11') location 's3://path/layer/11';





-- JSON nested fields
create external table dummy(
  a string,
  b struct <
    b1: string,
    b2: string
  >
  )
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://path/';

select b.b1 from dummy;