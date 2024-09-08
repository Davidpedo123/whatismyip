pipeline {
    agent any
    
    stages {
        stage('Clone repository') {
            steps {
                git 'https://github.com/Davidpedo123/whatismyip'
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    // Construir la imagen Docker
                    sh 'docker-compose build'
                }
            }
        }

        stage('Run Python Script') {
            steps {
                script {
                    // Ejecutar el script Python desde el subdirectorio
                    def result = sh(script: 'python3 back/test.py', returnStdout: true).trim()
                    if (result.contains('VALIDACION EXITOSA: 200')) {
                        echo 'La validación fue exitosa.'
                    } else {
                        error 'La validación falló.'
                    }
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main' // Solo se ejecuta en la rama principal
            }
            steps {
                script {
                    // Desplegar la aplicación si la validación fue exitosa
                    sh 'docker-compose down && docker-compose up -d'
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminado'
        }
        success {
            echo 'Pipeline ejecutado con éxito'
        }
        failure {
            echo 'El pipeline falló'
        }
    }
}
