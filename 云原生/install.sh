#!/bin/bash

# 获取版本号用的URL
DOCKER_VERSION_URL='https://download.docker.com/linux/static/stable/x86_64/'
KUBERNETES_VERSION_URL='https://dl.k8s.io/release/stable.txt'

# 检查是否已经有现成压缩包
# docker压缩包
DOCKER_ARCHIVE='docker*gz'
# k8s压缩包
K8S_ARCHIVE='kubernetes*gz'
K8S_BIN_LIST='kube-apiserver|kube-controller-manager|kubectl|kubelet|kube-proxy|kube-scheduler'


