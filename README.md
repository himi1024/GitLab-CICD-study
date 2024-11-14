File names that need to be modified (add . for)
.gitlab-ci.yml
.docker
.gitlab

------------------------------------------------------------------------
Minikube step for exposing the flask pod:

Option 1: Service (ClusterIP) - recommended [same cluster only(internal connection]) 

Option 2: Service (nodePort) - allow external connection

------------------------------------------------------------------------
Minikube step for API testing(using other pod with curl image):



