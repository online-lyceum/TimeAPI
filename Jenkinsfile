#!groovy

pipeline {
    agent any
    stages {
        stage("Build image") {
            steps {
                sh 'docker build -t time_api:${JOB_NAME} .'
            }
        }
        stage("Run images") {
            steps {
                sh 'docker-compose up -d'
                sh 'sleep 5'
                sh 'bash -c docker-compose exec -d ${JOB_NAME,,}_time_api init_models'
            }
        }
    }
}
