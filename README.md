# GitLab-CICD-study

# .gitlab-ci.yml
stages:   
#  - sast       # List of stages for jobs, and their order of execution
#  - build
  - test
#  - deploy
#  - verify
#  - custom-dast
  
.semgrep-sast:
  stage: sast
  variables:
    SAST_ANALYZER_IMAGE_TAG: "3.7"
    SAST_IMAGE_SUFFIX: '-fips'

.build_image:
  image: docker:20.10.20
  stage: build
  services:
    - docker:20.10.20-dind
  variables:
    DOCKER_HOST: tcp://docker:2375/
  script:
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER $CI_REGISTRY --password-stdin
    - docker build -t $CI_REGISTRY_IMAGE .
    - docker push $CI_REGISTRY_IMAGE

.ontainer_scanning:
  variables:
    CS_IMAGE: registry.gitlab.hk/himi/cicd:latest

.deploy:
  image:
    name: bitnami/kubectl:latest
    entrypoint: ['']
  stage: deploy
  script:
    - kubectl config use-context himi/cicd:gitlab-agent
    - kubectl replace -f flask-deployment.yml
    - sleep 10
  variables:
    KUBE_CONTEXT: himi/cicd:gitlab-agent

test_api:
  stage: test
  image:
    name: bitnami/kubectl:latest
    entrypoint: ['']
  script:
    - kubectl config use-context himi/cicd:gitlab-agent
    - POD_NAME=$(kubectl get pods -l app=curl -o jsonpath='{.items[0].metadata.name}' || echo "none")
    - if [ "$POD_NAME" = "none" ]; then
        echo "No pod found with label app=curl.";
        exit 1;
      fi
    - OUTPUT=$(kubectl logs $POD_NAME --tail=4)  # Fetch only the latest log entry
    - echo "Latest Log Entry:"
    - echo "$OUTPUT"  # Output the latest log entry
    - |
      if echo "$OUTPUT" | grep -q '"message": "hello world"'; then
        echo "API test succeeded.";
      else
        echo "API test failed.";
        exit 1;  # Exit with an error code to fail the job
      fi
  
.resource_verify:
  stage: verify
  image:
    name: bitnami/kubectl:latest
    entrypoint: ['']
  script:
  - echo "Checking if all pods are running..."
  - kubectl config use-context himi/cicd:gitlab-agent
  - kubectl rollout status deployment/flask-deployment
  - kubectl get pods -l app=test
  variables:
    KUBE_CONTEXT: himi/cicd:gitlab-agent

.function_verify:
  stage: verify
  needs: [resource_verify]
  image:
    name: bitnami/kubectl:latest
    entrypoint: ['']
  script:
  - kubectl config use-context himi/cicd:gitlab-agent
  - kubectl rollout status deployment/curl-deployment
  variables:
    KUBE_CONTEXT: himi/cicd:gitlab-agent

.dast:
  stage: custom-dast
  image: bitnami/kubectl:latest  # Main image for the job
  services:
    - name: docker:20.10.20  # Additional service image
  #rules:
    #- if: '$CI_PIPELINE_SOURCE == "schedule"'
    #- when: always  # Change for testing
  script:
    - echo "Running DAST..."
    - kubectl config use-context himi/cicd:gitlab-agent
    - bash ./dast-scanning.sh



.include:
  - template: Jobs/SAST.gitlab-ci.yml
  - template: Jobs/Container-Scanning.gitlab-ci.yml
#  - template: Jobs/DAST.gitlab-ci.yml

---
