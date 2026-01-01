# 🏋️ Personal Workout Tracker

A mobile-friendly web application built with [Streamlit](https://streamlit.io) and Google Sheets to track workouts, monitor progress, and manage training schedules. 

Designed to look and feel like a native app on your phone while keeping your data fully accessible in a spreadsheet.

## ✨ Features

* **📱 Mobile-First Design:** Optimized for phone screens with a clean, focused UI.
* **🔄 Live Sync:** Connects directly to Google Sheets. Updates are instant and permanent.
* **🔒 Admin & Guest Modes:** * **Guest:** Read-only access to view the plan.
    * **Admin:** Password-protected access to log weights, reps, and RPE.
* **📈 Analytics Dashboard:** Visualize strength trends and calculate lifetime volume lifted.
* **⚙️ Plan Generator:** Built-in tool to clone previous weeks and generate CSVs for future workout blocks.
* **ℹ️ Integrated Notes:** Quick access to warm-up routines and exercise cues via the sidebar.

## 🛠️ Prerequisites

1.  **Python 3.8+**
2.  **A Google Account** (for the spreadsheet backend)
3.  **Streamlit Account** (for free hosting)

## 🚀 Installation & Local Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Secrets (Local):**
    Create a file named `.streamlit/secrets.toml` in your project folder and add your credentials:
    ```toml
    # Admin password for "Save" access
    admin_password = "YOUR_SECURE_PASSWORD"

    # Google Sheets Connection
    [connections.gsheets]
    spreadsheet = "YOUR_GOOGLE_SHEET_PUBLIC_URL"
    ```

4.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

## 📊 Google Sheet Setup

The app requires a Google Sheet with specific columns to function correctly. 
1.  Create a new Sheet (or use your existing one).
2.  Ensure it is shared as **"Anyone with the link can Edit"** (or configure Service Account access for higher security).
3.  The sheet **must** contain these columns (case-sensitive):

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Date` | Date | YYYY-MM-DD |
| `Day` | Text | Mon, Tue, etc. |
| `Muscle Group` | Text | e.g., Chest, Back |
| `Exercise` | Text | Exercise Name |
| `Sets` | Number | Target sets |
| `Target Reps` | Text | e.g., "10-12" or "30 sec" |
| `Actual Weight (kg)` | Number | **(Logged by App)** |
| `Actual Reps` | Number | **(Logged by App)** |
| `Difficulty (1-10)` | Number | **(Logged by App)** |
| `Notes` | Text | Optional notes |

## ☁️ Deployment (Streamlit Cloud)

1.  Push your code to **GitHub**.
2.  Go to [share.streamlit.io](https://share.streamlit.io/).
3.  Click **New App** and select your repository.
4.  **IMPORTANT:** Before deploying, click **Advanced Settings** -> **Secrets**.
5.  Paste your secrets into the text area:
    ```toml
    admin_password = "YOUR_CHOSEN_PASSWORD"

    [connections.gsheets]
    spreadsheet = "YOUR_GOOGLE_SHEET_URL"
    ```
6.  Click **Deploy**!

## 📱 How to Install on Phone (PWA Style)

**Android (Chrome):**
1.  Open your app URL in Chrome.
2.  Tap the menu (three dots) -> **Add to Home screen** (or "Install App").
3.  Launch it from your home screen like a native app.

**iOS (Safari):**
1.  Open your app URL in Safari.
2.  Tap the **Share** button -> **Add to Home Screen**.

## 📂 Project Structure

├── app.py # Main application logic ├── requirements.txt # Python dependencies └── README.md # Documentation


## 🛡️ Security Note

This app uses a simple password check for the "Save" button to prevent accidental edits by others. For personal use, this effectively acts as a "Guest Mode" vs "Admin Mode". 

---
*Built using Python and Streamlit.*
