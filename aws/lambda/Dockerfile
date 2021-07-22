# docker build -t dev-nikkei-notify .

ARG FUNCTION_DIR="/app"
FROM python:3.8-alpine3.13

ENV PYTHONIOENCODING utf-8

RUN apk add --update \
  curl \
  chromium \
  chromium-chromedriver \
# Install aws-lambda-cpp build dependencies
  build-base \
  libtool \
  autoconf \
  automake \
  libexecinfo-dev \
  make \
  cmake \
  libcurl \
  wget \
  bash \
  which \
  groff \
  udev

ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}
COPY app/* ${FUNCTION_DIR}

RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

COPY requirements.txt .
RUN pip install -r requirements.txt

ARG FUNCTION_DIR
WORKDIR ${FUNCTION_DIR}

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["headless_lambda.lambda_handler"]
