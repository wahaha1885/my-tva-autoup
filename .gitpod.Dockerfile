FROM gitpod/workspace-full:latest

# 安装必要的依赖项
RUN sudo apt-get update && sudo apt-get install -y \
    python3-pip \
    zlib1g-dev \
    libffi-dev \
    gcc \
    build-essential \
    cython \
    libssl-dev \
    pkg-config \
    autoconf \
    automake \
    bison \
    flex \
    gettext \
    libtool \
    m4 \
    make \
    openjdk-8-jdk \
    unzip \
    wget

# 安装Android SDK和NDK
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-6609375_latest.zip -O /tmp/tools.zip && \
    unzip /tmp/tools.zip -d $ANDROID_HOME/cmdline-tools && \
    rm /tmp/tools.zip

ENV PATH $ANDROID_HOME/cmdline-tools/tools/bin:$PATH
RUN yes | sdkmanager --licenses
RUN sdkmanager "platform-tools" "platforms;android-29" "build-tools;29.0.3" "ndk;21.3.6528147"

# 安装Buildozer和依赖项
RUN pip3 install --upgrade pip
RUN pip3 install buildozer
RUN pip3 install cython==0.29.19

# 设置环境变量
ENV ANDROIDSDK /home/gitpod/android-sdk-linux
ENV ANDROIDNDK /home/gitpod/android-sdk-linux/ndk/21.3.6528147
ENV ANDROIDAPI 29
ENV ANDROIDMINAPI 21
