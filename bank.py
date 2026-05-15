import random          # For generating random account numbers and PINs
import streamlit as st  # Streamlit library for building the web UI

# ─────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# Must be the FIRST Streamlit command in the script.
# Sets the browser tab title, icon, and sidebar default state.
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────
# SESSION STATE — Persistent storage across button clicks
# Streamlit re-runs the entire script on every interaction.
# st.session_state keeps data alive between those re-runs.
# We store the list of all accounts here so it isn't reset.
# ─────────────────────────────────────────────────────────────
if "all_accounts" not in st.session_state:
    st.session_state.all_accounts = []   # Start with an empty list of accounts


# ─────────────────────────────────────────────────────────────
# APP TITLE & DESCRIPTION
# st.title()    → big heading
# st.markdown() → supports HTML/Markdown for styling
# ─────────────────────────────────────────────────────────────
st.title("🏦 Bank Management System")
st.markdown("---")   # Horizontal divider line


# ─────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# st.sidebar lets us put a menu on the left panel.
# st.sidebar.radio() shows radio buttons to pick a section.
# ─────────────────────────────────────────────────────────────
menu = st.sidebar.radio(
    "📋 Select Operation",
    ["🏠 Home", "🆕 Open Account", "💰 Check Balance", "➕ Deposit", "➖ Withdraw"]
)


# ══════════════════════════════════════════════════════════════
# SECTION 1 — HOME
# Shows a welcome message and all existing accounts in a table.
# ══════════════════════════════════════════════════════════════
if menu == "🏠 Home":
    st.subheader("Welcome to the Bank")
    st.write("Use the **sidebar** to navigate between operations.")

    # Only show accounts table if at least one account exists
    if st.session_state.all_accounts:
        st.markdown("### 📂 All Registered Accounts")
        # st.dataframe() renders a list of dicts as a nice table
        st.dataframe(st.session_state.all_accounts, use_container_width=True)
    else:
        # st.info() shows a blue informational message box
        st.info("No accounts opened yet. Go to **Open Account** to get started!")


# ══════════════════════════════════════════════════════════════
# SECTION 2 — OPEN ACCOUNT
# Replaces all input() calls with Streamlit form widgets.
# A st.form groups inputs so the page only re-runs on Submit.
# ══════════════════════════════════════════════════════════════
elif menu == "🆕 Open Account":
    st.subheader("🆕 Open a New Account")

    # st.form() groups all widgets; nothing is submitted until
    # the form's submit button is clicked — prevents partial runs.
    with st.form("open_account_form"):

        # st.text_input() → single-line text box (replaces input())
        account_title = st.text_input("Full Name")
        f_name        = st.text_input("Father's Name")

        # st.number_input() → numeric input (replaces int(input()))
        # min_value prevents negative numbers; step=1 means integers only
        contact_number = st.number_input("Contact Number", min_value=0, step=1, format="%d")
        cnic           = st.text_input("CNIC (e.g. 12345-1234567-1)")
        initial_deposit = st.number_input("Initial Deposit (Rs.)", min_value=0, step=100)

        # st.form_submit_button() → the Submit button for this form
        submitted = st.form_submit_button("✅ Open Account")

    # This block runs ONLY after the user clicks "Open Account"
    if submitted:

        # Basic validation — make sure required fields are filled
        if not account_title or not f_name or not cnic:
            # st.error() shows a red error message box
            st.error("⚠️ Please fill in all required fields.")
        else:
            # ── YOUR ORIGINAL LOGIC (unchanged) ──────────────────
            account = {}

            # random.randint() generates a random integer in [a, b]
            account_pin    = random.randint(1000, 9999)
            account_number = random.randint(10000, 99999)

            account["Title"]          = account_title.title()
            account["Father's Name"]  = f_name.title()
            account["Contact Number"] = contact_number
            account["CNIC"]           = cnic
            account["Balance"]        = initial_deposit
            account["Account Number"] = account_number
            account["Pin"]            = account_pin

            # Append to session state list (persists across reruns)
            st.session_state.all_accounts.append(account)
            # ─────────────────────────────────────────────────────

            # st.success() shows a green success message box
            st.success(f"🎉 Account opened successfully! Welcome, **{account_title.title()}**!")

            # st.info() to show account credentials clearly
            st.info(
                f"📌 **Save these credentials!**\n\n"
                f"- **Account Number:** `{account_number}`\n"
                f"- **PIN:** `{account_pin}`"
            )

            # st.json() renders a dict as formatted, collapsible JSON
            st.markdown("#### 📄 Full Account Details:")
            st.json(account)


# ══════════════════════════════════════════════════════════════
# SECTION 3 — CHECK BALANCE
# Asks for account number + PIN, then shows balance.
# ══════════════════════════════════════════════════════════════
elif menu == "💰 Check Balance":
    st.subheader("💰 Check Your Balance")

    with st.form("check_balance_form"):
        account_num = st.number_input("Account Number", min_value=0, step=1, format="%d")
        pin         = st.number_input("PIN",            min_value=0, step=1, format="%d")
        submitted   = st.form_submit_button("🔍 Check Balance")

    if submitted:
        found = False   # Flag to track if account was found

        # ── YOUR ORIGINAL LOGIC (unchanged) ──────────────────────
        for i in st.session_state.all_accounts:
            if account_num == i["Account Number"]:
                found = True
                if pin == i["Pin"]:
                    # st.metric() shows a highlighted KPI card
                    st.metric(
                        label=f"Balance for {i['Title']}",
                        value=f"Rs. {i['Balance']:,}"
                    )
                else:
                    st.error("❌ Incorrect PIN!")
                break
        # ─────────────────────────────────────────────────────────

        if not found:
            st.error("❌ Account Not Found!")


# ══════════════════════════════════════════════════════════════
# SECTION 4 — DEPOSIT
# Adds money to an account (no PIN needed, matches your original)
# ══════════════════════════════════════════════════════════════
elif menu == "➕ Deposit":
    st.subheader("➕ Deposit Amount")

    with st.form("deposit_form"):
        account_num = st.number_input("Account Number", min_value=0, step=1, format="%d")
        amount      = st.number_input("Deposit Amount (Rs.)", min_value=0, step=100)
        submitted   = st.form_submit_button("💵 Deposit")

    if submitted:
        found = False   # Flag to track if account was found

        # ── YOUR ORIGINAL LOGIC (unchanged) ──────────────────────
        for account in st.session_state.all_accounts:
            if account_num == account["Account Number"]:
                found = True
                if amount > 0:
                    account["Balance"] += amount   # Update balance in session state
                    st.success(
                        f"✅ Amount deposited successfully!\n\n"
                        f"**New Balance:** Rs. {account['Balance']:,}"
                    )
                else:
                    st.error("⚠️ Please enter an amount greater than 0.")
                break
        # ─────────────────────────────────────────────────────────

        if not found:
            st.error("❌ Account Not Found!")


# ══════════════════════════════════════════════════════════════
# SECTION 5 — WITHDRAW
# Deducts money after verifying account number + PIN + balance.
# ══════════════════════════════════════════════════════════════
elif menu == "➖ Withdraw":
    st.subheader("➖ Withdraw Amount")

    with st.form("withdraw_form"):
        account_num = st.number_input("Account Number", min_value=0, step=1, format="%d")
        pin         = st.number_input("PIN",            min_value=0, step=1, format="%d")
        amount      = st.number_input("Withdraw Amount (Rs.)", min_value=0, step=100)
        submitted   = st.form_submit_button("💸 Withdraw")

    if submitted:
        found = False   # Flag to track if account was found

        # ── YOUR ORIGINAL LOGIC (unchanged) ──────────────────────
        for account in st.session_state.all_accounts:
            if account_num == account["Account Number"]:
                found = True
                if pin == account["Pin"]:
                    if amount > 0:
                        if amount <= account["Balance"]:
                            account["Balance"] -= amount   # Deduct from balance
                            st.success(
                                f"✅ Withdrawal successful!\n\n"
                                f"**Withdrawn:** Rs. {amount:,}\n\n"
                                f"**New Balance:** Rs. {account['Balance']:,}"
                            )
                        else:
                            st.error("❌ Insufficient Balance!")
                    else:
                        st.error("⚠️ Please enter a valid amount greater than 0.")
                else:
                    st.error("❌ Incorrect PIN!")
                break
        # ─────────────────────────────────────────────────────────

        if not found:
            st.error("❌ Account Not Found!")


# ─────────────────────────────────────────────────────────────
# FOOTER
# st.markdown() with unsafe_allow_html=True lets us use HTML tags.
# ─────────────────────────────────────────────────────────────
st.markdown("---")