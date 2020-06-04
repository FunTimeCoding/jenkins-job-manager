FROM debian
MAINTAINER Alexander Reitzel
ADD script/docker/provision.sh /root/provision.sh
RUN chmod +x /root/provision.sh
RUN /root/provision.sh
ADD . /jenkins-job-manager
ENTRYPOINT ["/jenkins-job-manager/bin/jjm"]
