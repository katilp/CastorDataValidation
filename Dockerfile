# Container image that runs your code
FROM gitlab-registry.cern.ch/clange/cmssw-docker/cmssw_4_2_8_lowpupatch1:latest

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Change the permission of the entrypoint script. It can also be done on command line, but doing it here removes the need of local download.
USER root
RUN chmod +x /entrypoint.sh
USER cmsusr

# Executes `entrypoint.sh` when the Docker container starts up 
ENTRYPOINT ["/entrypoint.sh"]
