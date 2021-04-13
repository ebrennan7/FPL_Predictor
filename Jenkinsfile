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

                script {
                    sonarScanner('FPL-Predictor')
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

def sonarScanner(projectKey) {
    def scannerHome = tool 'sonar-scanner-local'
    withSonarQubeEnv("local-sonar") {

        if(fileExists("sonar-project.properties")) {
//             sh "${scannerHome}/bin/sonar-scanner"
                sh """pytest --cov=main_predictor tests/dream_team_tests.py
                      coverage xml
                """
        }
        else {
            sh "${scannerHome}/bin/sonar-scanner -     Dsonar.projectKey=${projectKey} -Dsonar.java.binaries=build/classes -Dsonar.java.libraries=**/*.jar -Dsonar.projectVersion=${BUILD_NUMBER}"
        }
    }
    timeout(time: 10, unit: 'MINUTES') {
        waitForQualityGate abortPipeline: true
    }
}