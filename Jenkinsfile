pipeline {
    agent none

    stages {
        stage('Install & Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh '''
                    pip install -e .
                    playwright install-deps chromium
                    playwright install chromium
                    pytest tests/ -v --alluredir=allure-results
                    chmod -R 777 allure-results   # <-- добавляем эту строку
                '''
            }
        }
    }

    post {
        always {
            node('') {
                allure includeProperties: false, results: [[path: 'allure-results']]
            }
        }
    }
}