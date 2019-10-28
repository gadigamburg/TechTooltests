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
                dir('Release'){
                deleteDir()
                checkout([$class: 'GitSCM', branches: [[name: '*/Dev']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'b6218c54-9fe9-4052-8da9-58322b94e248', url: 'https://github.com/gadigamburg/Release.git']]])
                }
                dir('development'){
                deleteDir()
                checkout([$class: 'GitSCM', branches: [[name: '*/Dev']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'b6218c54-9fe9-4052-8da9-58322b94e248', url: 'https://github.com/gadigamburg/CI-CD-Project.git']]])
                sh "git fetch --all"
                CurrentVersion = sh script: "git branch -r | cut -d'/' -f2 | grep -v -e master -e HEAD -e Dev | sort -r | head -1 ", returnStdout: true
                CurrentVersion = CurrentVersion.trim()
                int a = sh script : "echo $CurrentVersion | cut -c1", returnStdout: true
                int b = sh script : "echo \"$CurrentVersion\" | cut -c3", returnStdout: true
                int c = sh script : "echo \"$CurrentVersion\" | cut -c5", returnStdout: true
                commitIDshort = sh script:"git rev-parse HEAD | cut -c1-10", returnStdout: true
                commitIDshort = commitIDshort.trim()
                nextVersion = "${a}.${b}.${c+1}"
                BuildVersion = "${CurrentVersion}_${commitIDshort}"
                echo("BuildVersion Is: ${BuildVersion}")
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
