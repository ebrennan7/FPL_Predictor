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

                def sonarScanner(projectKey) {
                def scannerHome = tool 'sonarqube-scanner'
                withSonarQubeEnv("sonarqube") {
                    if(fileExists("sonar-project.properties")) {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                    else {
                        sh "${scannerHome}/bin/sonar-scanner -     Dsonar.projectKey=80f29535b5100e2cc1f735c835697e9690be32b3 -Dsonar.java.binaries=build/classes -Dsonar.java.libraries=**/*.jar -Dsonar.projectVersion=${env.BUILD_NUMBER}"
                    }
                }
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
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