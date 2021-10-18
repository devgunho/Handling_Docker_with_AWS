sudo docker start worker-container
sudo docker exec worker-container /bin/sh -c "rm -rf /input"
sudo docker exec worker-container /bin/sh -c "rm -rf /output"
sudo docker cp /transmission/. worker-container:/input
sudo docker exec worker-container /bin/sh -c "/run.sh"
sudo docker cp worker-container:/output/. /output/