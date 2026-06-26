# 🏦 Bank Management System

A simple, interactive Bank Management System built with **Streamlit**, allowing users to open accounts, check balances, deposit, and withdraw funds through a clean web interface.

## 🎯 Objective

To build a functional, menu-driven banking application that simulates core banking operations — account creation, balance inquiry, deposits, and withdrawals — using Streamlit's session state to manage account data in real time.

## ✨ Features

- **🆕 Open Account** – Create a new account with personal details (name, father's name, contact number, CNIC) and an initial deposit. Auto-generates a unique **Account Number** and **PIN**.
- **💰 Check Balance** – Securely view account balance after verifying Account Number and PIN.
- **➕ Deposit** – Add funds to an existing account.
- **➖ Withdraw** – Withdraw funds after PIN verification, with built-in checks for insufficient balance.
- **🏠 Home Dashboard** – View all registered accounts in a table at a glance.
- **🔒 Input Validation** – Handles missing fields, incorrect PINs, invalid amounts, and non-existent accounts gracefully with clear error messages.

## 🛠️ How It Works

- Account data is stored in `st.session_state`, so it persists across interactions within a session (resets when the app restarts).
- Each new account is assigned a randomly generated **4-digit PIN** and **5-digit Account Number** for identification and security.
- All operations (balance check, deposit, withdrawal) validate the account number — and PIN, where applicable — before processing the request.

## 🧠 Skills Demonstrated

- Building multi-page-style apps using Streamlit's sidebar navigation
- Managing state across user interactions with `st.session_state`
- Form handling and input validation
- Conditional logic for transaction processing
- Basic security simulation (PIN-based authentication)

## 📦 Tech Stack

| Tool / Library | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web app framework and UI components |

## 🚀 Getting Started

### Prerequisites

```bash
pip install streamlit
```

### Running the App

1. Clone the repository:
```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
```
2. Run the app:
```bash
   streamlit run bank_management.py
```
3. The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

├── bank_management.py   # Main Streamlit application

├── README.md             # Project documentation

└── requirements.txt       # Python dependencies

## 📌 Notes

- Account data is **not persisted to a database or file** — it exists only in memory for the current session and will be lost on app restart. This project is intended as a demonstration of Streamlit's UI and state management capabilities, not a production banking system.
- CNIC and contact number fields do not currently enforce format validation; these could be enhanced with regex-based checks.
