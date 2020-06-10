# Container image that runs your code
FROM cmsopendata/cmssw_4_2_8:latest

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Executes `entrypoint.sh` when the Docker container starts up 
ENTRYPOINT ["/entrypoint.sh"]
