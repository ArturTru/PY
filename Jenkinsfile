pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    pip install -e .
                    playwright install chromium
                    pytest tests/ -v --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            // Дженкинс заберет результаты и превратит их в красивый граф
            allure includeProperties: false, jdq: '', results: [[path: 'allure-results']]
        }
    }
}

