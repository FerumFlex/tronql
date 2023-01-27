FROM tronprotocol/centos7

ENV TMP_DIR="/tron-build"
ENV JDK_TAR="jdk-8u202-linux-x64.tar.gz"
ENV JDK_DIR="jdk1.8.0_202"
ENV JDK_MD5="0029351f7a946f6c05b582100c7d45b7"
ENV BASE_DIR="/java-tron"


RUN set -o errexit -o nounset \
    && yum -y install git wget \
    && wget -P /usr/local https://github.com/frekele/oracle-java/releases/download/8u202-b08/$JDK_TAR \
    && echo "$JDK_MD5 /usr/local/$JDK_TAR" | md5sum -c \
    && tar -zxf /usr/local/$JDK_TAR -C /usr/local\
    && rm /usr/local/$JDK_TAR \
    && export JAVA_HOME=/usr/local/$JDK_DIR \
    && export CLASSPATH=$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar \
    && export PATH=$PATH:$JAVA_HOME/bin \
    && echo "git clone" \
    && mkdir -p $TMP_DIR \
    && cd $TMP_DIR \
    && git clone https://github.com/tronprotocol/java-tron.git \
    && cd java-tron \
    && git checkout GreatVoyage-v4.7.0.1 \
    && ./gradlew build -x test \
    && cd build/distributions \
    && UNZIP_DISABLE_ZIPBOMB_DETECTION=TRUE unzip -o java-tron-1.0.0.zip \
    && mv java-tron-1.0.0 $BASE_DIR \
    && cd $TMP_DIR && cd .. \
    && rm -rf $TMP_DIR \
    && mkdir -p $TMP_DIR \
    && git clone https://github.com/tronprotocol/event-plugin.git \
    && cd event-plugin \
    && ./gradlew build --warning-mode=all  \
    && mv build/plugins/plugin-kafka-1.0.0.zip $BASE_DIR \
    && cd .. \
    && rm -rf event-plugin \
    && rm -rf $TMP_DIR \
    && rm -rf ~/.gradle \
    && mv $JAVA_HOME/jre /usr/local \
    && rm -rf $JAVA_HOME \
    && yum clean all

RUN wget -P $BASE_DIR/config https://raw.githubusercontent.com/tronprotocol/tron-deployment/master/main_net_config.conf

ENV JAVA_HOME="/usr/local/jre"
ENV PATH=$PATH:$JAVA_HOME/bin

COPY docker-entrypoint.sh $BASE_DIR/bin
COPY logback.xml /java-tron/config/logback.xml

WORKDIR $BASE_DIR

ENTRYPOINT ["./bin/docker-entrypoint.sh"]
