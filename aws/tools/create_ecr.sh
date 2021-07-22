#!/bin/bash

set -x

aws ecr create-repository \
    --repository-name dev-nikkei-notify \
    --image-scanning-configuration scanOnPush=true \
    --region ap-northeast-1
