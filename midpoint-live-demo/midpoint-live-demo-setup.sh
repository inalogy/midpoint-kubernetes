#!/bin/bash
set -x

NAMESPACE=mp-demo
DOMAIN=example.com
SMTP_NAME=fake-smtp
OVERLAY=overlays/nginx
TUNNEL=false

ROOT_DIR=$PWD

while getopts n:o:c:a:i:h:t flag
do
    case "${flag}" in
        n) NAMESPACE=${OPTARG};;
        o) OVERLAY=${OPTARG};;
        c) CERTADDRESS=${OPTARG};;
        a) DOMAIN=${OPTARG};;
        i) INGRESSCLASS=${OPTARG};;
        t) TUNNEL=${OPTARG};;
        h | *)
          echo "script usage:"
          echo "$0 [-s value] [-n value]"
          echo "-n 	 custom namespace in which demo would be deployed. Default namespace is mp-demo"
          echo "-o 	 overlay to use, [azure, nginx] in the form of  overlays/nginx"
          echo "-c 	 custom yaml certificate for ingresses. Default certificate is packed with demo. PLEASE USE THE SAME NAME FOR THE FILE AND THE KUBERNETES OBJECT"
          echo "-a 	 custom domain for ingresses. Default domain is example.com. Please be aware that default certificate does work only with default host"
          echo "-i    custom ingressClass name. Default is default on your machine (one with annotation ingressclass.kubernetes.io/is-default-class: true). Make sure that you do have ONE default ingressClass or use this option to set a custom one."
          echo "-t    do you want to start minikube tunnel?"
          ;; 
    esac
done

sed -i .bak "s/ingress_host: .*/ingress_host: $DOMAIN/g" base/kustomize-env-config/options-map.yaml

if [ -z $INGRESSCLASS ]
then
   INGRESSCLASS=$(kubectl get ingressClass -o=jsonpath='{.items[?(@.metadata.annotations.ingressclass\.kubernetes\.io/is-default-class=="true")].metadata.name}')
fi

sed -i .bak "s/ingress_class_name: .*/ingress_class_name: $INGRESSCLASS/g" base/kustomize-env-config/options-map.yaml

if [ $CERTADDRESS ]
then
   kubectl apply -f $CERTADDRESS -n $NAMESPACE 2> /dev/null || true
   CERT=$(basename $CERTADDRESS)
else
   mkdir base/kustomize-env-config/certificate/ 2> /dev/null || true
   cd base/kustomize-env-config/certificate/

   kubectl delete secret -n $NAMESPACE cert-mp-demo || true
   rm -rf tls.crt tls.key

   openssl req -new -sha256 -newkey rsa:2048 -keyout tls.key -nodes -subj "/CN=test CA" -out tls.csr
   openssl x509 -req -signkey tls.key -in tls.csr -out tls.crt -days 3650 -sha256 -extfile  <(cat <<EOF
basicConstraints = CA:FALSE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = digitalSignature, nonRepudiation, keyEncipherment
subjectAltName = DNS:*.$DOMAIN
extendedKeyUsage = serverAuth
EOF
)
   kubectl create secret tls -n $NAMESPACE cert-mp-demo --cert=tls.crt --key=tls.key  # 2> /dev/null || true
   CERT="cert-mp-demo"
fi

cd $ROOT_DIR
sed -i .bak "s/ingress_cert: .*/ingress_cert: $CERT/g" base/kustomize-env-config/options-map.yaml

kubectl create namespace $NAMESPACE 2> /dev/null || true
kubectl apply -k $OVERLAY -n $NAMESPACE

if $TUNNEL; then
  echo "Starting minikube tunnel!"
  sudo minikube tunnel
fi
