File names that need to be modified (add . for)
.gitlab-ci.yml
.docker
.gitlab

------------------------------------------------------------------------
Minikube step for exposing the flask pod:

Option 1: Service (ClusterIP) - recommended [same cluster only(internal connection]) 
  i. kubectl create -f flask-clusterIP-service.yaml

Option 2: Service (nodePort) - allow external connection
  i. Ingress install
     - minikube addons enable ingress
  ii. kubectl create -f flask-service.yaml
  iii. minikube tunnel
  iv. curl the ip in local device (Since i am using Minikube, external connection is not allowed)
    - minikube service <service-name> —url

------------------------------------------------------------------------
Minikube step for API testing(using other pod with curl image):
  i. kubectl create -f curl-pod.yml
  ii. kubectl logs <curl-pod.name>
      - get the pod name with kubectl get pod <OR> kubectl get pods -l app=curl -o jsonpath='{.items[0].metadata.name}'
  iii. kubectl get logs <pod.name>



