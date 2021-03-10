pipeline {
    agent agent {
        docker {
          label 'docker'
          image 'node:7-alpine'
        }
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