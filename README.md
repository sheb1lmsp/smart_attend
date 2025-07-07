# Smart Attend: Automated Attendance Management System

## Overview
Smart Attend is an AI-driven attendance management system designed to streamline and automate attendance tracking in educational institutions. Utilizing facial recognition technology, it replaces time-consuming and error-prone traditional methods with a scalable, user-friendly solution. The system achieves approximately 95% accuracy in face detection and recognition, offering role-based access for Admins, Teachers, and Students, and integrates Twilio API for automated parental notifications.

## Features
- **Facial Recognition-Based Attendance**: Marks attendance by uploading a single photo.
- **Role-Based Dashboards**: Tailored interfaces for Admin, Teacher, and Student roles.
- **Real-Time Tracking**: Monitors attendance in real time with detailed records.
- **Parental Notifications**: Sends automated updates to parents via Twilio API.
- **Class-Specific Model Training**: Ensures high accuracy for specific class groups.

## System Architecture
- **Client-Side**: HTML, CSS (Bootstrap), JavaScript
- **Server-Side**: Python Django
- **Database**: SQLite (scalable to PostgreSQL)
- **Machine Learning**: PyTorch (MTCNN for face detection, InceptionResNetV1 for recognition)
- **External API**: Twilio for SMS notifications

## Technology Stack
| Component            | Technology                     |
|---------------------|--------------------------------|
| Frontend            | HTML, CSS (Bootstrap), JavaScript |
| Backend             | Python Django                 |
| Database            | SQLite (scalable to PostgreSQL) |
| Machine Learning    | PyTorch (MTCNN, InceptionResNetV1) |
| Notification System | Twilio API                    |

## Implementation Process
1. **Setup**: Admin creates users and assigns roles (Admin, Teacher, Student).
2. **Training**: Teachers upload 50 photos per student to train the facial recognition model.
3. **Attendance Marking**: A single photo upload automatically marks attendance.
4. **Viewing Records**: Role-specific dashboards display attendance data.

## Applications & Impact
- Automates attendance tracking in educational institutions.
- Ensures accurate, compliant record-keeping.
- Enhances parental involvement through automated notifications.
- Reduces administrative workload.
- Scalable for large institutions with multiple classes.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/smart-attend.git
   cd smart-attend
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Environment**:
   - Configure Django settings in `settings.py`.
   - Set up Twilio API credentials (Account SID, Auth Token, and phone number).
   - Initialize SQLite database or configure PostgreSQL.
4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start the Server**:
   ```bash
   python manage.py runserver
   ```
6. **Train the Model**:
   - Upload student photos via the Teacher dashboard.
   - Run the training script: `python train_model.py`.

## Usage
- **Admin**: Log in to create users, assign roles, and manage the system.
- **Teacher**: Upload photos for model training and mark attendance.
- **Student**: View personal attendance records.
- **Parental Notifications**: Automatically sent via Twilio when attendance is marked.

## Future Enhancements
- Develop a mobile app for on-the-go access.
- Integrate with CCTV or Raspberry Pi for real-time monitoring.
- Improve accuracy using ArcFace algorithm.
- Add cloud support for multi-college deployments.
- Incorporate biometric alternatives (e.g., fingerprint, iris scanning).

## Conclusion
Smart Attend revolutionizes attendance management with high accuracy, reduced errors, and improved efficiency. It ensures secure, scalable, and user-friendly operations, laying the foundation for smarter educational systems. Future improvements will focus on real-time processing and broader adaptability.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
