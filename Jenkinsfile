node('JenkinsSlave2'){
	currentBuild.result = "SUCCESS"
	stage('checkout'){
		sh 'echo "checkout"'
	}
	stage('unit test'){
		sh 'echo "unit test"'
	}
	stage('integration test'){
		sh 'python home-assignments/session2/exercise1.py --city dublin --forecast TODAY -c'
	}
	stage('deploy'){
		sh 'echo "deploy"'
	}	
}
