properties([pipelineTriggers([githubPush()])])

pipeline {


    agent {
        label 'master'
    }

    stages {
        stage('Docker Build') {
            steps {
                sh """
                    echo ">> Docker Building ${env.BUILD_NUMBER}"
                    docker build -t image:0.0.${env.BUILD_NUMBER} .
                    docker run -d -p 5000:5000 image:0.0.${env.BUILD_NUMBER}
                """
            }
        }
        stage('SonarQube Scan') {
            steps {

                withSonarQubeEnv('My SonarQube Server', envOnly: true) {
                    // This expands the evironment variables SONAR_CONFIG_NAME, SONAR_HOST_URL, SONAR_AUTH_TOKEN that can be used by any script.
                    println ${env.SONAR_HOST_URL}
                }


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