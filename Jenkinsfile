pipeline {
    agent { any { image 'python:3.7.2' } }
    stages {
        stage('build') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
    }
}