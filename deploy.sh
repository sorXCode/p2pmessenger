cd k8s
yamls=`{ls -p | grep -v / | tr '\n' ','}`;
yamls="${yamls:0:-1}";
kubectl apply -f $yamls