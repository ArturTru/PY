pipeline {
    agent any // Запускаем пайплайн на самом Дженкинсе, без докер-агента

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test') {
            steps {
                // Дженкинс сам соберет образ и запустит тесты через обычные shell-команды
                sh '''
                    docker build -t playwright-tests .
                    docker run --rm -v ${WORKSPACE}/allure-results:/app/allure-results playwright-tests
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
