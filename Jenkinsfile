pipeline {
    agent{
        label 'Slave'
    }
    
    stages {
        stage ('checkout'){
            steps {
                script{
                    target= input(
                            id: 'userInput', message: 'Enter target IP',
                            parameters: [
                                string(defaultValue: '34.220.17.148',
                                       description: 'ip address',
                                       name: 'IP')])
                    dir('TechToolTest'){
                        deleteDir()
                        checkout([$class: 'GitSCM', branches: [[name: '*/Patch-1']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'b6218c54-9fe9-4052-8da9-58322b94e248', url: 'https://github.com/gadigamburg/TechTooltests.git']]])
                        sh "git fetch --all"
                    }
                }
            }
        }
        stage ('Build Image and Sanity Test'){
            steps {
                script{
                    dir ('development') {
                        sh "ls"
                    myImage = docker.build("gadigamburg/python-app:${nextVersion}", "./app")
                    myImage.withRun('-p 80:80 --name python') {c ->
                      try{
                          sh 'sleep 1'
                          sh 'curl -i -m 1 http://localhost'
                      } catch (err) {
                          currentBuild.result = 'FAILED'
                          
                      }
                    }
                }
                }
            }
        }
        stage ('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', 'docker_hub'){
                        myImage.push()
                }
                }
            }
        }
        stage ('Push to a new branch'){
            steps {
                script {
                    dir ('development'){
                        withCredentials([usernamePassword(credentialsId: 'GadiGit',
                        passwordVariable: 'GIT_PASS', usernameVariable: 'GIT_USER')]) {
                        sh "git branch ${nextVersion}"
                        sh "git checkout ${nextVersion}"
                        sh 'git push https://${GIT_USER}:${GIT_PASS}@github.com/gadigamburg/CI-CD-Project'
                        echo("Push Branch: ${nextVersion} Success")
                    }
                    }
                    
                }
            }
        }
    }
    post {
        success {
             dir('Release') {
                        withCredentials([usernamePassword(credentialsId: 'GadiGit',
                        passwordVariable: 'GIT_PASS', usernameVariable: 'GIT_USER')]) {
                        sh "git checkout Dev"
                        sh "sed -i 's/${CurrentVersion}/${nextVersion}/g' dev.json"
                            sh "cat dev.json"
                        sh "sed -i 's/ipaddr/${target}/g' dev.json"
                            sh "cat dev.json"
                        sh "git add dev.json"
                        sh "git config --global user.email 'gadigamburg@gmail.com'"
                        sh "git config --global user.name 'Gadi'"
                        sh "git commit -m 'CI approved ${nextVersion}'"
                        sh "git push https://${GIT_USER}:${GIT_PASS}@github.com/gadigamburg/Release"
                        sh 'docker image prune -a -f --filter "until=1h"'
        }
        }
        }
        //failure {
            //emailext body: '${BUILD_ID} failed', subject: 'Build Failed', to: 'your email'
        //}
        }
    }
