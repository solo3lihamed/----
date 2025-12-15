// وظائف JavaScript مخصصة لموقع عَبَق

// Lazy loading للصور
document.addEventListener('DOMContentLoaded', function() {
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }
});

// Smooth scroll للروابط الداخلية
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Show/hide scroll to top button
let scrollToTopBtn = document.createElement('button');
scrollToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
scrollToTopBtn.className = 'fixed bottom-8 right-8 bg-purple-600 text-white p-4 rounded-full shadow-lg hover:bg-purple-700 transition-all duration-300 z-50 hidden';
scrollToTopBtn.id = 'scrollToTop';
document.body.appendChild(scrollToTopBtn);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollToTopBtn.classList.remove('hidden');
    } else {
        scrollToTopBtn.classList.add('hidden');
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Toast notifications
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500';
    toast.className = `fixed top-24 right-8 ${bgColor} text-white px-6 py-4 rounded-lg shadow-lg z-50 animate-slide-in`;
    toast.innerHTML = `
        <div class="flex items-center gap-3">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} text-2xl"></i>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('border-red-500');
            isValid = false;
        } else {
            input.classList.remove('border-red-500');
        }
    });
    
    return isValid;
}

// Add to cart animation
function addToCartAnimation(button) {
    const cart = document.querySelector('.fa-shopping-cart');
    if (!cart) return;
    
    const buttonRect = button.getBoundingClientRect();
    const cartRect = cart.getBoundingClientRect();
    
    const clone = button.cloneNode(true);
    clone.style.position = 'fixed';
    clone.style.left = buttonRect.left + 'px';
    clone.style.top = buttonRect.top + 'px';
    clone.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
    clone.style.zIndex = '9999';
    document.body.appendChild(clone);
    
    setTimeout(() => {
        clone.style.left = cartRect.left + 'px';
        clone.style.top = cartRect.top + 'px';
        clone.style.transform = 'scale(0)';
        clone.style.opacity = '0';
    }, 10);
    
    setTimeout(() => {
        clone.remove();
        cart.classList.add('scale-125');
        setTimeout(() => cart.classList.remove('scale-125'), 300);
    }, 800);
}

// Handle add to cart buttons
document.addEventListener('submit', function(e) {
    if (e.target.matches('form[action*="cart/add"]')) {
        const button = e.target.querySelector('button[type="submit"]');
        if (button) {
            addToCartAnimation(button);
        }
    }
});

// Image zoom on hover
document.querySelectorAll('.zoom-on-hover').forEach(img => {
    img.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
    });
    img.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});

// Auto-update cart quantities
let quantityTimeout;
document.querySelectorAll('input[type="number"][name="quantity"]').forEach(input => {
    input.addEventListener('change', function() {
        clearTimeout(quantityTimeout);
        quantityTimeout = setTimeout(() => {
            this.closest('form').submit();
        }, 500);
    });
});

// Copy tracking code to clipboard
function copyTrackingCode(code) {
    navigator.clipboard.writeText(code).then(() => {
        showToast('تم نسخ رمز التتبع', 'success');
    }).catch(() => {
        showToast('فشل نسخ رمز التتبع', 'error');
    });
}

// Add copy button to tracking codes
document.querySelectorAll('.tracking-code').forEach(element => {
    const code = element.textContent.trim();
    const copyBtn = document.createElement('button');
    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
    copyBtn.className = 'ml-2 text-purple-600 hover:text-purple-800';
    copyBtn.onclick = () => copyTrackingCode(code);
    element.appendChild(copyBtn);
});

// Initialize tooltips
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute bg-gray-800 text-white px-3 py-2 rounded text-sm z-50';
            tooltip.textContent = this.dataset.tooltip;
            tooltip.style.top = (this.offsetTop - 40) + 'px';
            tooltip.style.left = this.offsetLeft + 'px';
            this.appendChild(tooltip);
        });
        element.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.absolute.bg-gray-800');
            if (tooltip) tooltip.remove();
        });
    });
}

// Initialize on page load
window.addEventListener('load', () => {
    initTooltips();
    
    // Add fade-in class to elements
    document.querySelectorAll('.fade-in-on-load').forEach(element => {
        element.classList.add('fade-in');
    });
});

// Handle network errors
window.addEventListener('offline', () => {
    showToast('لا يوجد اتصال بالإنترنت', 'error');
});

window.addEventListener('online', () => {
    showToast('تم استعادة الاتصال بالإنترنت', 'success');
});

console.log('🌸 مرحباً بك في موقع عَبَق للعطور الفاخرة!');

