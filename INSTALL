To run this script every hour in the said machine use the following script and hook it up to the crontab 

1/ Create a new virtual env using 

``` 
  mkvirtualenv s3lncoll
```
2/ Get inside the virtual Env
```
  workon s3lncoll
```

3/ Install s3lncoll from pypy

```
  pip install s3lncoll
```

4/ Now deactivate the env
```
  deactivate 
```

5/ Now open crontab using

```
  crontab -e

  # inside crontab
  15 * * * * /home/kafka/s3lncoll_runner.sh
```

6/ The contents of s3lncoll_runner.sh is as given below

```

#!/bin/bash

export AWS_ACCESS_KEY_ID=<<MAGIC>>
export AWS_SECRET_ACCESS_KEY=<<MAGIC>>
YEAR=$(date +%Y -d "1 hour ago")
MONTH=$(date +%m -d "1 hour ago")
DAY=$(date +%d -d "1 hour ago")
HOUR=$(date +%H -d "1 hour ago")
MINUTE=$(date +%M)
# echo ${YEAR}${MONTH}${DAY}_${HOUR}${MINUTE}

# /home/kafka/Envs/s3lncoll/bin/s3lncoll s3://my_home/topics/topic-ua-king-patch/year=${YEAR}/month=${MONTH}/day=${DAY}/hour=${HOUR}/ s3://datavisor-prod/data/king/rawdata/$YEAR$MONTH$DAY/rawlog.${YEAR}${MONTH}${DAY}_${HOUR}${MINUTE}00.${YEAR}${MONTH}${DAY}_${HOUR}${MINUTE}00.RULE_ENGINE_{}.gz -z -b 209715200 2>&1 | tee /home/kafka/kafka-logs/s3runner_${YEAR}${MONTH}${DAY}_${HOUR}${MINUTE}.log

/home/kafka/Envs/s3lncoll/bin/s3lncoll s3://my_home/topics/topic-ua-king-patch/year=${YEAR}/month=${MONTH}/day=${DAY}/hour=${HOUR}/ s3://datavisor-prod-king/rawdata/$YEAR$MONTH$DAY/rawlog.${YEAR}${MONTH}${DAY}_${HOUR}${MINUTE}00.${YEAR}${MONTH}${DAY}_${HOUR}${MINUTE}00.RULE_ENGINE_{}.gz -z -b 209715200 2>&1 | tee /home/kafka/kafka-logs/s3runner_${YEAR}${MONTH}${DAY}_${HOUR}${MINUTE}.log

# export AWS_ACCESS_KEY_ID=; export AWS_SECRET_ACCESS_KEY=; YEAR=$(date +%Y -d "1 hour ago"); MONTH=$(date +%m -d "1 hour ago"); DAY=$(date +%d -d "1 hour ago"); HOUR=$(date +%H -d "1 hour ago"); MINUTE=$(date +%M); /home/kafka/Envs/s3lncoll/bin/s3lncoll s3://my_home/topics/topic-ua-king/year=${YEAR}/month=${MONTH}/day=${DAY}/hour=${HOUR}/ s3://my_home/prod/data/king/rawdata/$YEAR$MONTH$DAY/rawlog.${YEAR}${MONTH}${DAY}_${HOUR}${MINUTE}00.${YEAR}${MONTH}${DAY}_${HOUR}${MINUTE}00.RULE_ENGINE_{}.gz -z -b 209715200

```
