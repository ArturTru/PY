pipeline {
    agent none // Global agetn off

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
                '''
            }
        }
    }

    post {
        always {
            // Этот блок выполнится на самом Jenkins (вне контейнера Python), где Java доступна
            node {
                allure includeProperties: false, results: [[path: 'allure-results']]
            }
        }
    }
}
