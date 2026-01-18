// animation.js - 蓝雀词典搜索结果页面动画效果

// 页面加载动画
function initPageAnimation() {
    // 设置顶部区域的初始动画状态
    const topSection = document.getElementById('topSection');
    if (topSection) {
        topSection.style.opacity = '0';
        topSection.style.transform = 'translateY(20px)';
        topSection.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    }
    
    // 设置释义区域的初始动画状态
    const definitionSection = document.querySelector('.definition-section');
    if (definitionSection) {
        definitionSection.style.opacity = '0';
        definitionSection.style.transform = 'translateY(20px)';
        definitionSection.style.transition = 'opacity 0.8s ease 0.2s, transform 0.8s ease 0.2s';
    }
    
    // 触发页面加载动画
    setTimeout(() => {
        if (topSection) {
            topSection.style.opacity = '1';
            topSection.style.transform = 'translateY(0)';
        }
        
        if (definitionSection) {
            definitionSection.style.opacity = '1';
            definitionSection.style.transform = 'translateY(0)';
        }
    }, 100);
}

// 初始化搜索框动画
function initSearchBoxAnimation() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;
    
    // 搜索框获得焦点时清空placeholder
    searchInput.addEventListener('focus', function() {
        this.setAttribute('data-placeholder', this.getAttribute('placeholder'));
        this.setAttribute('placeholder', '');
    });
    
    // 搜索框失去焦点时恢复placeholder
    searchInput.addEventListener('blur', function() {
        if (this.value === '') {
            this.setAttribute('placeholder', this.getAttribute('data-placeholder') || '输入汉字/单词，回车查询');
        }
    });
}

// 返回顶部按钮动画
function initBackToTopAnimation() {
    const backToTopBtn = document.getElementById('backToTop');
    if (!backToTopBtn) return;
    
    // 监听滚动事件，控制返回顶部按钮的显示/隐藏
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
    
    // 返回顶部功能
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// 搜索结果显示动画
function showResultWithAnimation(element, delay = 0) {
    if (!element) return;
    
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = `opacity 0.6s ease ${delay}s, transform 0.6s ease ${delay}s`;
    
    setTimeout(() => {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 100);
}

// 页面加载时初始化所有动画
document.addEventListener('DOMContentLoaded', function() {
    initPageAnimation();
    initSearchBoxAnimation();
    initBackToTopAnimation();
});
