#!/bin/bash
fileid="1tyjEaNwLGYNu93BR7p43soBvLXR_kZQW"
filename="sentiment_model.tgz"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}