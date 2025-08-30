// 导航栏滚动效果
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// 移动端汉堡菜单
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

 hamburger.addEventListener('click', function() {
    navLinks.classList.toggle('active');
    hamburger.querySelector('i').classList.toggle('fa-bars');
    hamburger.querySelector('i').classList.toggle('fa-times');
});

// 平滑滚动到锚点
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();

        // 关闭移动端菜单（如果打开）
        if (navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            hamburger.querySelector('i').classList.add('fa-bars');
            hamburger.querySelector('i').classList.remove('fa-times');
        }

        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// 性能对比图表
window.addEventListener('load', function() {
    const ctx = document.getElementById('performanceChart').getContext('2d');

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['传输速度', '延迟', '带宽利用率', '安全性', '连接建立时间'],
            datasets: [{
                label: 'SQA协议',
                data: [95, 90, 85, 98, 92],
                backgroundColor: 'rgba(37, 99, 235, 0.7)',
                borderColor: 'rgba(37, 99, 235, 1)',
                borderWidth: 1
            }, {
                label: 'HTTP/2',
                data: [75, 65, 70, 80, 60],
                backgroundColor: 'rgba(100, 116, 139, 0.7)',
                borderColor: 'rgba(100, 116, 139, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: '性能评分 (0-100)'
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'SQA协议与HTTP/2性能对比'
                }
            }
        }
    });
});

// 表单验证
const contactForm = document.querySelector('form');

if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        let isValid = true;

        // 简单验证
        if (name.trim() === '') {
            isValid = false;
            alert('请输入您的姓名');
        } else if (email.trim() === '') {
            isValid = false;
            alert('请输入您的邮箱');
        } else if (!isValidEmail(email)) {
            isValid = false;
            alert('请输入有效的邮箱地址');
        } else if (message.trim() === '') {
            isValid = false;
            alert('请输入您的留言');
        }

        if (isValid) {
            // 这里可以添加表单提交逻辑
            alert('感谢您的留言！我们会尽快回复您。');
            contactForm.reset();
        }
    });
}

// 邮箱验证函数
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// 添加页面加载动画
window.addEventListener('load', function() {
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.style.display = 'none';
    }
});

// 为功能卡片添加动画效果
const featureCards = document.querySelectorAll('.feature-card');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, {
    threshold: 0.1
});

featureCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
});

// 为优势项目添加动画效果
const benefitItems = document.querySelectorAll('.benefit-item');

benefitItems.forEach((item, index) => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(20px)';
    item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    item.style.transitionDelay = `${index * 0.1}s`;
    observer.observe(item);
});

// 技术规格项目动画
const specItems = document.querySelectorAll('.spec-item');

specItems.forEach((item, index) => {
    item.style.opacity = '0';
    item.style.transform = 'translateX(-20px)';
    item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    item.style.transitionDelay = `${index * 0.1}s`;
    observer.observe(item);
});

// 添加数据包动画
function createPacketAnimation() {
    const protocolAnimation = document.querySelector('.protocol-animation');
    if (!protocolAnimation) return;

    // 随机创建额外的数据包
    for (let i = 0; i < 3; i++) {
        const packet = document.createElement('div');
        packet.classList.add('packet');
        packet.style.top = `${Math.random() * 300}px`;
        packet.style.left = `${Math.random() * 100}px`;
        packet.style.backgroundColor = getRandomColor();
        packet.style.animationDelay = `${Math.random() * 3}s`;
        protocolAnimation.appendChild(packet);
    }
}

function getRandomColor() {
    const colors = ['#2563eb', '#f43f5e', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'];
    return colors[Math.floor(Math.random() * colors.length)];
}

// 页面加载完成后创建更多数据包动画
window.addEventListener('load', createPacketAnimation);