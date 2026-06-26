pipeline {
    agent none // global agetn 

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
            // allure switch 
            node('') {
                allure includeProperties: false, results: [[path: 'allure-results']]
            }
        }
    }
}
