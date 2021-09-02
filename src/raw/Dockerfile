
FROM osgeo/gdal

RUN apt update && \
    apt-get install -y jq libxml2-utils

ADD functions.sh /functions.sh

ADD rcm-raw /usr/bin/rcm-raw
  
RUN chmod +x /usr/bin/rcm-raw