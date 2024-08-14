# Chat System

A Django-based chat system with user registration, login, and interest functionality.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Nehababar22/Assignments.git
    cd ChatSystem
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment:**

    - **Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply Migrations:**

    ```bash
    Python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a Superuser (for accessing the admin interface):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

## Running Tests

To run tests, use the following command:

```bash
python manage.py test
