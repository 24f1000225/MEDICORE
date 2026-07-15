hospital-management-system/
│
├── backend/
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          
│   │   ├── doctor.py
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   ├── treatment.py
│   │   └── department.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py         
│   │   ├── admin.py         
│   │   ├── doctor.py        
│   │   ├── patient.py      
│   │   └── appointment.py  
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── reminders.py     
│   │   ├── reports.py       
│   │   └── export_csv.py    
│   │
│   ├── utils/
│   │   ├── auth.py          
│   │   ├── cache.py         
│   │   └── mail.py          
│   │
|   ├── config.py
│   ├── database.py          
│   └── celery_worker.py    
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── AdminDashboard.vue
│   │   │   ├── DoctorDashboard.vue
│   │   │   ├── PatientDashboard.vue
│   │   │   ├── DoctorAvailability.vue
│   │   │   └── PatientHistory.vue
│   │   │
│   │   ├── services/
│   │   │   └── api.js        
│   │   │
│   │   ├── router/
│   │   │   └── index.js      
│   │   │
│   │   └── main.js
│   │
│   └── index.html            
│
├── redis/
│   └── redis.conf
│
├── main.py
├── requirements.txt
└── README.md


