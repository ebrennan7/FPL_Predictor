// pipeline {
//     agent { docker-agent }
//
//     stages {
//         stage('build') {
//
//             steps {
//                 sh '''
//                 docker build -t dream_team_image .
//                 '''
//             }
//         }
//     }
// }


properties([pipelineTriggers([githubPush()])])

pipeline {
    /* specify nodes for executing */
    agent {
        label 'github-ci'
    }

    stages {
        /* checkout repo */
        stage('Checkout SCM') {
            steps {
                checkout([
                 $class: 'GitSCM',
                 branches: [[name: 'master']],
                 userRemoteConfigs: [[
                    url: 'git@github.com:ebrennan7/FPL_Predictor.git',
                    credentialsId: '',
                 ]]
                ])
            }
        }
         stage('Do the deployment') {
            steps {
                echo ">> Run deploy applications "
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