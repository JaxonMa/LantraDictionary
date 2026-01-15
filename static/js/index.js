// 搜索框交互功能
document.addEventListener('DOMContentLoaded', function() {
    const searchBox = document.querySelector('.search-box');
    const originalPlaceholder = searchBox.getAttribute('placeholder');

    // 监听焦点事件
    searchBox.addEventListener('focus', function() {
        this.style.transform = 'translateY(-2px)';
        // 保存原始placeholder文本并清空
        this.setAttribute('data-placeholder', this.getAttribute('placeholder'));
        this.setAttribute('placeholder', '');
    });

    // 监听失去焦点事件
    searchBox.addEventListener('blur', function() {
        this.style.transform = 'translateY(0)';
        // 恢复placeholder文本
        this.setAttribute('placeholder', originalPlaceholder);
    });

    // 添加页面加载时的动画效果
    setTimeout(() => {
        document.querySelector('.header-container').style.opacity = '1';
        document.querySelector('.header-container').style.transform = 'translateY(0)';
        document.querySelector('.search-container').style.opacity = '1';
        document.querySelector('.search-container').style.transform = 'translateY(0)';
    }, 100);
});

// 初始样式设置（用于动画）
document.querySelector('.header-container').style.opacity = '0';
document.querySelector('.header-container').style.transform = 'translateY(-20px)';
document.querySelector('.header-container').style.transition = 'opacity 0.8s ease, transform 0.8s ease';

document.querySelector('.search-container').style.opacity = '0';
document.querySelector('.search-container').style.transform = 'translateY(20px)';
document.querySelector('.search-container').style.transition = 'opacity 0.8s ease 0.2s, transform 0.8s ease 0.2s';