Travel_tourism/
│
├── .vscode/                      # VSCode settings
│   └── settings.json
│
├── admin_panel/                  #  Admin Dashboard Module
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   ├── views.py
│   ├── services.py              # Statistics, reports
│   ├── forms.py                 # Admin forms
│   ├── static/
│   │   └── admin_panel/
│   │       ├── css/
│   │       │   └── dashboard.css
│   │       └── js/
│   │           ├── dashboard.js
│   │           └── charts.js
│   └── templates/
│       └── admin_panel/
│           ├── base_admin.html       # Admin base layout
│           ├── dashboard.html        # Dashboard overview
│           ├── users_manage.html     # Quản lý users
│           ├── tours_manage.html     # Quản lý tours
│           ├── hotels_manage.html    # Quản lý hotels
│           ├── flights_manage.html   # Quản lý flights
│           ├── bookings_manage.html  # Quản lý bookings
│           ├── chatlog_view.html     # Xem chat logs
│           └── statistics.html       # Báo cáo thống kê
│
├── bookings/                     #  Booking Module
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                # Booking model
│   ├── forms.py                 # Booking forms
│   ├── views.py                 # Booking views
│   ├── urls.py
│   ├── services.py              # BookingService
│   ├── signals.py               # Booking notifications
│   ├── admin.py
│   ├── tests.py
│   ├── static/
│   │   └── bookings/
│   │       ├── css/
│   │       │   └── booking.css
│   │       └── js/
│   │           └── booking.js
│   └── templates/
│       └── bookings/
│           ├── create.html           # Tạo booking
│           ├── list.html             # Danh sách bookings của user
│           ├── detail.html           # Chi tiết booking
│           └── confirm.html          # Xác nhận booking
│
├── chatbot/                      #  Chatbot Module
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                # ChatLog model
│   ├── views.py                 # Chat API
│   ├── urls.py
│   ├── chatbot_service.py       # NLP logic
│   ├── train.py                 # Train chatbot model
│   ├── admin.py
│   ├── tests.py
│   ├── data/
│   │   ├── intents.json         # Training data
│   │   └── model/               # Trained model files
│   ├── static/
│   │   └── chatbot/
│   │       ├── css/
│   │       │   └── chatbot.css
│   │       └── js/
│   │           └── chatbot.js   # Chat widget
│   └── templates/
│       └── chatbot/
│           ├── widget.html           # Chat widget (embed vào pages)
│           └── logs.html             # Admin xem logs
│
├── core/                         #  Core Module (Common pages)
│   ├── __init__.py
│   ├── apps.py
│   ├── views.py                 # Homepage, About, Contact
│   ├── urls.py
│   ├── middleware.py            # Custom middleware
│   ├── utils.py                 # Helper functions
│   ├── exceptions.py            # Custom exceptions
│   ├── validators.py            # Custom validators
│   ├── static/
│   │   └── core/
│   │       ├── css/
│   │       │   └── core.css
│   │       └── js/
│   │           └── core.js
│   └── templates/
│       └── core/
│           ├── home.html             # Homepage
│           ├── about.html            # Giới thiệu
│           ├── contact.html          # Liên hệ
│           └── search_results.html   # Kết quả tìm kiếm
│
├── data/                         #  Seed Data
│   ├── users.json
│   ├── tours.json
│   ├── hotels.json
│   ├── flights.json
│   └── bookings.json
│
├── docs/                         #  Documentation
│   ├── api.md
│   ├── database_schema.md
│   ├── deployment.md
│   └── user_guide.md
│
├── flight/                       #  Flight Module
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                # Flight model
│   ├── forms.py                 # Search, filter forms
│   ├── views.py
│   ├── urls.py
│   ├── services.py              # FlightService
│   ├── admin.py
│   ├── tests.py
│   ├── static/
│   │   └── flight/
│   │       ├── css/
│   │       │   └── flight.css
│   │       └── js/
│   │           └── flight.js
│   └── templates/
│       └── flight/
│           ├── list.html             # Danh sách chuyến bay
│           ├── detail.html           # Chi tiết chuyến bay
│           └── search.html           # Tìm kiếm chuyến bay
│
├── hotels/                       #  Hotels Module
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                # Hotel model
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py              # HotelService
│   ├── admin.py
│   ├── tests.py
│   ├── static/
│   │   └── hotels/
│   │       ├── css/
│   │       │   └── hotel.css
│   │       └── js/
│   │           └── hotel.js
│   └── templates/
│       └── hotels/
│           ├── list.html             # Danh sách khách sạn
│           ├── detail.html           # Chi tiết khách sạn
│           └── search.html           # Tìm kiếm khách sạn
│
├── scripts/                      #  Utility Scripts
│   ├── seed_data.py             # Seed database
│   ├── backup_db.sh             # Backup database
│   ├── deploy.sh                # Deployment script
│   └── test_frontend.sh         # Test frontend
│
├── static/                       #  Global Static Files
│   ├── css/
│   │   ├── base.css             # Base styles
│   │   ├── navbar.css           # Navigation styles
│   │   ├── footer.css           # Footer styles
│   │   ├── forms.css            # Form styles
│   │   └── responsive.css       # Responsive styles
│   ├── js/
│   │   ├── main.js              # Main JavaScript
│   │   ├── utils.js             # Utility functions
│   │   ├── ajax.js              # AJAX helpers
│   │   └── validation.js        # Form validation
│   ├── images/
│   │   ├── logo.png             # Logo
│   │   ├── banner.jpg           # Hero banner
│   │   ├── favicon.ico          # Favicon
│   │   └── placeholder.jpg      # Placeholder image
│   └── vendor/                  # Third-party libraries
│       ├── bootstrap/           # (CDN khuyến nghị)
│       ├── jquery/              # (CDN khuyến nghị)
│       └── fontawesome/         # (CDN khuyến nghị)
│
├── templates/                    #  Global Templates
│   ├── base.html                # Base template (extends all)
│   ├── components/
│   │   ├── navbar.html          # Navigation bar
│   │   ├── footer.html          # Footer
│   │   ├── messages.html        # Flash messages
│   │   ├── pagination.html      # Pagination component
│   │   └── breadcrumb.html      # Breadcrumb navigation
│   └── errors/
│       ├── 400.html             # Bad request
│       ├── 403.html             # Forbidden
│       ├── 404.html             # Not found
│       └── 500.html             # Server error
│
├── tours/                        #  Tours Module
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                # Tour model
│   ├── forms.py                 # Search, filter forms
│   ├── views.py
│   ├── urls.py
│   ├── services.py              # TourService
│   ├── admin.py
│   ├── tests.py
│   ├── static/
│   │   └── tours/
│   │       ├── css/
│   │       │   └── tour.css
│   │       └── js/
│   │           └── tour.js
│   └── templates/
│       └── tours/
│           ├── list.html             # Danh sách tours
│           ├── detail.html           # Chi tiết tour
│           ├── search.html           # Tìm kiếm tour
│           └── categories.html       # Tour theo danh mục
│
├── travel_tourism/               #  Main Project Folder
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL config
│   ├── wsgi.py                  # WSGI config
│   └── asgi.py                  # ASGI config
│
├── users/                        #  Users Module  (ĐÃ HOÀN THÀNH)
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                #  User model
│   ├── forms.py                 #  Auth forms
│   ├── views.py                 #  Auth views
│   ├── urls.py                  #  Auth URLs
│   ├── services.py              #  UserService
│   ├── signals.py               # Signals
│   ├── middleware.py            #  Auth middleware
│   ├── decorators.py            #  Decorators
│   ├── context_processors.py   #  Context processors
│   ├── admin.py                 # Admin config
│   ├── tests.py                 #  Tests
│   ├── management/
│   │   └── commands/
│   │       └── create_admin.py  #  CLI command
│   ├── static/
│   │   └── users/
│   │       ├── css/
│   │       │   └── auth.css     #  CẦN TẠO
│   │       └── js/
│   │           └── auth.js      #  CẦN TẠO
│   └── templates/
│       └── users/
│           ├── login.html            #  CẦN TẠO
│           ├── register.html         #  CẦN TẠO
│           ├── forget_password.html  #  CẦN TẠO
│           └── reset_password.html   #  CẦN TẠO
│
├── .env                          # Environment variables
├── .env.example                  # Env example
├── .gitignore                    # Git ignore
├── docker-compose.yml            # Docker compose
├── Dockerfile                    # Docker file
├── manage.py                     # Django management
├── README.md                     # Project readme
├── requirements.txt              # Python dependencies
└── dir                           # Directory listing