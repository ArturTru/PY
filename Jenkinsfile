pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Install & Test') {
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
            allure includeProperties: false, results: [[path: 'allure-results']]
        }
    }
}
