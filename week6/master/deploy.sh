#!/bin/bash
echo "🚀 Blog Master Server 배포를 시작합니다..."

echo "📦 시스템 업데이트 중..."
sudo yum update -y

# 2. Python 및 pip 설치
echo "🐍 Python 환경 설정 중..."
sudo yum install python3 python3-pip -y
pip3 install --upgrade pip
pip3 install virtualenv

# 3. 가상환경 생성 및 활성화
echo "🔧 가상환경 설정 중..."
python3 -m venv venv
source venv/bin/activate

# 4. 의존성 설치
echo "📚 의존성 설치 중..."
pip install -r requirements.txt

# 5. 데이터베이스 초기화
echo "🗄️ 데이터베이스 초기화 중..."
python3 -c "from database import create_tables; create_tables()"

# 6. systemd 서비스 설정
echo "⚙️ systemd 서비스 설정 중..."
sudo cp blog-master.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable blog-master

# 7. 서비스 시작
echo "▶️ 서비스 시작 중..."
sudo systemctl start blog-master
sudo systemctl status blog-master

echo "✅ 배포가 완료되었습니다!"
echo "🌐 서버 접속: http://43.200.129.41:8000"
echo "📊 로그 확인: http://43.200.129.41:8000/logs?caller_name=학생이름"
echo "👥 사용자 확인: http://43.200.129.41:8000/users?caller_name=학생이름"
