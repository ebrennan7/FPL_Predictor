pipeline {
    agent { docker-agent }

    stages {
        stage('build') {

            steps {
                sh '''
                docker build -t dream_team_image .
                '''
            }
        }
    }
}