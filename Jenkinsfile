node {

    stage('Checkout SCM') {

        checkout scm

    }
    stage('Build Image') {

        /* Let's make sure we have the repository cloned to our workspace */
        withEnv(['REG_URL=registry.allbright.local:5000']) {
            sh 'docker build -t ${REG_URL}/${JOB_NAME}:${BUILD_NUMBER} .'

        }
    }

    stage('Push Image into Registry') {

        withEnv(['REG_URL=registry.allbright.local:5000']) {

            sh 'docker login -u admin -p allbright ${REG_URL}'
            sh 'docker push ${REG_URL}/${JOB_NAME}:${BUILD_NUMBER}'

            }
        }
    stage('Promotion Confirmation') {

        withEnv(['REG_URL=registry.allbright.local:5000']) {
        timeout(time: 1, unit: 'HOURS'){
        input 'Proceed to deploy to Kubernetes Cluster ?'
        sh 'docker rmi ${REG_URL}/${JOB_NAME}:${BUILD_NUMBER}'
             }
        }
    }


    stage('Update Pod in K8s Cluster') {

        /* Let's make sure we have the repository cloned to our workspace */
        withEnv(['REG_URL=registry.allbright.local:5000']) {
        sh 'kubectl set image deployment/k8s-ui k8s-ui=${REG_URL}/${JOB_NAME}:${BUILD_NUMBER}'
        sh 'kubectl rollout status deployment/k8s-ui'
        }
        /* sh 'kubectl expose deployment k8s-ui --port=8008 --target-port=80' */

    }

}









