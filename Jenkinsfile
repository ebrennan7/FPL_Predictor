pipeline {
    agent {
        label 'docker'
    }

    stages {
        stage('build') {
            agent {
                docker {
                    label 'docker'
                    image 'node:7-alpine'
                }
            }
            steps {
                sh '''
                docker build -t dream_team_image .
                '''
            }
        }
    }
}