pipeline {
    agent {
        dockerfile {
            filename 'ci/Dockerfile'
            args '-u root --entrypoint=""'
        }
    }
    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '30', artifactDaysToKeepStr: '14'))
    }
    stages {
        stage('Toolchain') {
            steps {
                sh '''
                    set -eu
                    git config --global --add safe.directory "$WORKSPACE"
                    git clean -fdx -q
                '''
            }
        }
        stage('Compiler') { steps { sh 'grill install wurstscript' } }
        stage('Dependencies') { steps { sh 'grill install' } }
        stage('Tests') { steps { sh 'grill test' } }
    }
    post {
        failure { archiveArtifacts allowEmptyArchive: true, artifacts: '_build/**' }
        cleanup { sh 'chmod -R a+rwX "$WORKSPACE" 2>/dev/null || true' }
    }
}
