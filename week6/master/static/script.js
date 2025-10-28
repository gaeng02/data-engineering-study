// 블로그 마스터 서버 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 좋아요 버튼 이벤트 리스너
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const postId = this.dataset.postId;
            const likeCountElement = this.querySelector('.like-count');
            const originalText = this.innerHTML;
            
            // 로딩 상태 표시
            this.innerHTML = '⏳';
            this.disabled = true;
            
            // 좋아요 요청
            fetch(`/like/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                // 성공 시 좋아요 수 업데이트
                if (likeCountElement) {
                    likeCountElement.textContent = data.likes_count;
                }
                
                // 애니메이션 효과
                this.classList.add('liked');
                setTimeout(() => {
                    this.classList.remove('liked');
                }, 1000);
                
                // 성공 메시지 표시
                showNotification('좋아요가 추가되었습니다!', 'success');
            })
            .catch(error => {
                console.error('좋아요 오류:', error);
                showNotification('좋아요 처리 중 오류가 발생했습니다.', 'error');
            })
            .finally(() => {
                // 버튼 상태 복원
                this.innerHTML = originalText;
                this.disabled = false;
            });
        });
    });
    
    // 댓글 버튼 이벤트 리스너
    document.querySelectorAll('.comment-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const postId = this.dataset.postId;
            const originalText = this.innerHTML;
            
            // 로딩 상태 표시
            this.innerHTML = '⏳';
            this.disabled = true;
            
            // 댓글 시도 요청
            fetch(`/comment/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                // 성공 메시지 표시
                showNotification('댓글 시도가 기록되었습니다! (실제로는 저장되지 않음)', 'info');
            })
            .catch(error => {
                console.error('댓글 오류:', error);
                showNotification('댓글 처리 중 오류가 발생했습니다.', 'error');
            })
            .finally(() => {
                // 버튼 상태 복원
                this.innerHTML = originalText;
                this.disabled = false;
            });
        });
    });
    
    // 포스트 카드 클릭 이벤트 (홈 페이지에서만)
    document.querySelectorAll('.post-card').forEach(card => {
        card.addEventListener('click', function(e) {
            // 버튼 클릭이 아닌 경우에만 페이지 이동
            if (!e.target.closest('button') && !e.target.closest('a')) {
                const postId = this.dataset.postId;
                window.location.href = `/post/${postId}`;
            }
        });
    });
    
    // 페이지 로드 시 페이드인 애니메이션
    document.querySelectorAll('.card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease-in-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// 알림 표시 함수
function showNotification(message, type = 'info') {
    // 기존 알림 제거
    const existingAlert = document.querySelector('.alert-notification');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // 새 알림 생성
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} alert-dismissible fade show alert-notification`;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 3초 후 자동 제거
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 3000);
}

// 사용자 확인 함수 (개발자용)
function checkUsers() {
    fetch('/users')
        .then(response => response.json())
        .then(users => {
            console.log('현재 사용자:', users);
            showNotification(`총 ${users.length}명의 사용자가 등록되어 있습니다.`, 'info');
        })
        .catch(error => {
            console.error('사용자 조회 오류:', error);
            showNotification('사용자 조회 중 오류가 발생했습니다.', 'error');
        });
}

// 로그 확인 함수 (개발자용)
function checkLogs() {
    fetch('/logs')
        .then(response => response.json())
        .then(logs => {
            console.log('현재 로그:', logs);
            showNotification(`총 ${logs.length}개의 로그가 기록되었습니다.`, 'info');
        })
        .catch(error => {
            console.error('로그 조회 오류:', error);
            showNotification('로그 조회 중 오류가 발생했습니다.', 'error');
        });
}

// 키보드 단축키
document.addEventListener('keydown', function(e) {
    // Ctrl + L: 로그 확인
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        checkLogs();
    }
    
    // Ctrl + H: 홈으로 이동
    if (e.ctrlKey && e.key === 'h') {
        e.preventDefault();
        window.location.href = '/';
    }
});

// 페이지 가시성 변경 시 로그 기록 (선택사항)
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        console.log('페이지가 숨겨졌습니다');
    } else {
        console.log('페이지가 다시 보입니다');
    }
});

// 에러 처리
window.addEventListener('error', function(e) {
    console.error('JavaScript 오류:', e.error);
    showNotification('페이지에서 오류가 발생했습니다.', 'error');
});

// 네트워크 오류 처리
window.addEventListener('unhandledrejection', function(e) {
    console.error('Promise 오류:', e.reason);
    showNotification('네트워크 오류가 발생했습니다.', 'error');
});
