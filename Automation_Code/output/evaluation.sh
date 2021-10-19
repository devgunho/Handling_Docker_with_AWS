#!/bin/bash
function timestamp {
    TEXT="Date:"
    DATE=`date +%Y-%m-%d`
    TIME=`date +%H:%M:%S`
    ZONE=`date +"%Z %z"`
    echo $TEXT $DATE $TIME $ZONE
}

sudo docker start worker-container
sudo docker exec worker-container /bin/sh -c "rm -rf /input"
sudo docker exec worker-container /bin/sh -c "rm -rf /output"
sudo docker cp /transmission/. worker-container:/input
echo $timestamp
sudo docker exec worker-container /bin/sh -c "/run.sh"
echo $timestamp
sudo mkdir -p /output
sudo docker cp worker-container:/output/. /output/