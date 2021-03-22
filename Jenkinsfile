// 젠킨스 파이프라인 플러그인을 호출하기 위한 블록
pipeline {
	// 파이프라인을 실행하고 싶은 위치 정의
	agent none
	// gitlab의 소스를 jenkins 디렉토리로 내려받을 시
	// skipDefaultCheckout(true)일 경우 내려받는 프로세스 skip
	// skipDefaultCheckout(false)일 경우 gitlab 소스 체크
	options { skipDefaultCheckout(true) }
	// stage의 모음
	stages {
		// 실제 작업이 수행되는 블록
		// 해당 stage 명으로 jenkins 화면에 표시된다
        stage('Docker build') {
            agent any
            steps {
                // front-end 및 back-end dockerfile 실행을 통해 image 생성
                // -t : 이미지 이름과 tag 설정, 만약 이미지 이름만 설정하면 latest로 설정됨
                sh 'docker build -t SmaitFront:latest /var/jenkins_home/workspace/smait/frontend'
                sh 'docker build -t SmaitBack:latest /var/jenkins_home/workspace/smait/backend'
            }
        }
        stage('Docker run') {
            agent any
            steps {
				// 현재 동작중인 컨테이너 중 SmaitFront의 이름을 가진 컨테이너를 stop
				sh 'docker ps -f name=SmaitFront -q \
					| xargs --no-run-if-empty docker container stop'
				// 현재 동작중인 컨테이너 중 SmaitBack의 이름을 가진 컨테이너를 stop
				sh 'docker ps -f name=SmaitBack -q \
					| xargs --no-run-if-empty docker container stop'
				// SmaitFront의 이름을 가진 컨테이너를 삭제
				sh 'docker container ls -a -f name=SmaitFront -q \
					| xargs -r docker container rm'
				// SmaitBack의 이름을 가진 컨테이너를 삭제
				sh 'docker container ls -a -f name=SmaitBack -q \
					| xargs -r docker container rm'
				// docker image build 시 기존에 존재하던 이미지는
				// dangling 상태가 되기 때문에 이미지를 일괄 삭제
				sh 'docker images -f dangling=true && \
					docker rmi $(docker images -f "dangling=true" -q)'
				// docker container 실행
				// 하나의 docker network에 연결하여 통신이 가능하도록 설정
				sh 'docker run -d --name SmaitFront \
					-p 80:80 \
					-p 443:443 \
					-v /home/ubuntu/keys:/var/jenkins_home/workspace/smait/sslkey/ \
					--network smait \
					SmaitFront:latest'
				sh 'docker run -d --name SmaitBack \
					--network smait \
					SmaitBack:latest'
			}
		}
	}
}