properties([pipelineTriggers([githubPush()])])

pipeline {


    agent {
        label 'docker'
    }


    stages {
         stage('Docker Build') {
            steps {
            sh """
                echo ">> Docker Building ${env.BUILD_NUMBER}"
                docker build -t image:0.0.${env.BUILD_NUMBER} .
                docker run -d -p 5000:5000 image:0.0.${env.BUILD_NUMBER}
                docker logs
            """
            }
        }
    }

    /* Cleanup workspace */
    post {
       always {
           deleteDir()
       }
   }
}