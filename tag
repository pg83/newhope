#!/bin/sh

docker tag $1 antonsamokhvalov/newhope:$2
docker tag antonsamokhvalov/newhope:$2 antonsamokhvalov/newhope:latest

docker push antonsamokhvalov/newhope:$2
docker push antonsamokhvalov/newhope:latest
