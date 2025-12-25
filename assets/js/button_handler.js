/**
 * Button Handler - Xử lý logic cho các nút trong giao diện web
 * Tập trung tất cả các sự kiện click của nút
 */

// Mapping các nút với hành động tương ứng
const BUTTON_ACTIONS = {
    // Navigation buttons
    'btn-home': { action: 'navigate', url: '/' },
    'btn-about': { action: 'navigate', url: '/about/' },
    'btn-destinations': { action: 'navigate', url: '/destinations/' },
    'btn-tours': { action: 'navigate', url: '/tours/' },
    'btn-gallery': { action: 'navigate', url: '/gallery/' },
    'btn-blog': { action: 'navigate', url: '/blog/' },
    'btn-contact': { action: 'navigate', url: '/contact/' },
    'btn-faq': { action: 'navigate', url: '/faq/' },
    'btn-terms': { action: 'navigate', url: '/terms/' },
    'btn-privacy': { action: 'navigate', url: '/privacy/' },
    
    // Service buttons
    'btn-booking': { action: 'navigate', url: '/bookings/' },
    'btn-flight': { action: 'navigate', url: '/flight/' },
    'btn-chatbot': { action: 'navigate', url: '/chatbot/' },
    
    // Authentication buttons
    'btn-login': { action: 'navigate', url: '/users/login/' },
    'btn-logout': { action: 'navigate', url: '/users/logout/' },
    'btn-register': { action: 'navigate', url: '/users/register/' },
    
    // Action buttons
    'btn-book-now': { action: 'navigate', url: '/bookings/' },
    'btn-view-details': { action: 'navigate', url: '/tours/' },
    'btn-view-tour': { action: 'navigate', url: '/tours/' },
    'btn-view-all-tours': { action: 'navigate', url: '/tours/' },
    'btn-contact-expert': { action: 'navigate', url: '/contact/' },
    'btn-get-quote': { action: 'navigate', url: '/contact/' },
    'btn-start-exploring': { action: 'navigate', url: '/tours/' },
    'btn-browse-tours': { action: 'navigate', url: '/tours/' },
};

/**
 * Khởi tạo button handlers
 */
function initializeButtonHandlers() {
    // Xử lý tất cả các nút có class 'btn'
    document.querySelectorAll('a[href="#"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Lấy button ID hoặc class
            const buttonId = this.id;
            const buttonClass = Array.from(this.classList).find(cls => cls.startsWith('btn-'));
            const buttonName = buttonId || buttonClass;
            
            if (buttonName) {
                handleButtonClick(buttonName, this);
            }
        });
    });
    
    // Xử lý các nút có data-action attribute
    document.querySelectorAll('[data-action]').forEach(button => {
        button.addEventListener('click', function(e) {
            const action = this.getAttribute('data-action');
            const params = this.getAttribute('data-params');
            
            if (action) {
                handleButtonAction(action, params ? JSON.parse(params) : {});
            }
        });
    });
}

/**
 * Xử lý click button
 */
function handleButtonClick(buttonName, element) {
    const action = BUTTON_ACTIONS[buttonName];
    
    if (action) {
        switch(action.action) {
            case 'navigate':
                window.location.href = action.url;
                break;
            case 'api':
                sendButtonClickToServer(buttonName, element);
                break;
            case 'modal':
                showModal(action.modalId);
                break;
            case 'form':
                submitForm(action.formId);
                break;
            default:
                console.warn(`Unknown action: ${action.action}`);
        }
    } else {
        console.warn(`No action defined for button: ${buttonName}`);
    }
}

/**
 * Xử lý hành động button
 */
function handleButtonAction(action, params = {}) {
    switch(action) {
        case 'book_tour':
            if (params.tour_id) {
                window.location.href = `/bookings/create/tour/${params.tour_id}/`;
            } else {
                window.location.href = '/bookings/';
            }
            break;
        case 'book_flight':
            if (params.flight_id) {
                window.location.href = `/bookings/create/flight/${params.flight_id}/`;
            } else {
                window.location.href = '/flight/';
            }
            break;
        case 'book_hotel':
            if (params.hotel_id) {
                window.location.href = `/bookings/create/hotel/${params.hotel_id}/`;
            } else {
                window.location.href = '/bookings/';
            }
            break;
        case 'contact_expert':
            window.location.href = '/contact/';
            break;
        case 'get_quote':
            window.location.href = '/contact/';
            break;
        default:
            console.warn(`Unknown action: ${action}`);
    }
}

/**
 * Gửi button click tới server
 */
function sendButtonClickToServer(buttonName, element) {
    const data = {
        button_name: buttonName,
        params: {}
    };
    
    // Lấy các tham số từ data attributes
    if (element.dataset) {
        Object.keys(element.dataset).forEach(key => {
            if (key !== 'action') {
                data.params[key] = element.dataset[key];
            }
        });
    }
    
    fetch('/api/button-click/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.redirect_url) {
            window.location.href = data.redirect_url;
        } else {
            console.error('Error:', data.message);
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}

/**
 * Lấy CSRF token từ cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Hiển thị modal
 */
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    }
}

/**
 * Submit form
 */
function submitForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.submit();
    }
}

/**
 * Thêm event listener cho các nút "Book Now"
 */
function initializeBookingButtons() {
    document.querySelectorAll('[data-action="book_tour"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const tourId = this.getAttribute('data-tour-id');
            if (tourId) {
                window.location.href = `/bookings/create/tour/${tourId}/`;
            } else {
                window.location.href = '/bookings/';
            }
        });
    });
    
    document.querySelectorAll('[data-action="book_flight"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const flightId = this.getAttribute('data-flight-id');
            if (flightId) {
                window.location.href = `/bookings/create/flight/${flightId}/`;
            } else {
                window.location.href = '/flight/';
            }
        });
    });
    
    document.querySelectorAll('[data-action="book_hotel"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const hotelId = this.getAttribute('data-hotel-id');
            if (hotelId) {
                window.location.href = `/bookings/create/hotel/${hotelId}/`;
            } else {
                window.location.href = '/bookings/';
            }
        });
    });
}

/**
 * Khởi tạo khi DOM đã sẵn sàng
 */
document.addEventListener('DOMContentLoaded', function() {
    initializeButtonHandlers();
    initializeBookingButtons();
    console.log('Button handlers initialized');
});
