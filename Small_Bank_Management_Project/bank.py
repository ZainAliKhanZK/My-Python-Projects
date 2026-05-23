import random
import streamlit as st

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered"
)

if "all_accounts" not in st.session_state:
    st.session_state.all_accounts = []

st.title("🏦 Bank Management System")
st.markdown("---")

menu = st.sidebar.radio(
    "📋 Select Operation",
    ["🏠 Home", "🆕 Open Account", "💰 Check Balance", "➕ Deposit", "➖ Withdraw"]
)

if menu == "🏠 Home":
    st.subheader("Welcome to the Bank 👋")
    st.write("Use the **sidebar** to navigate between operations.")

    if st.session_state.all_accounts:
        st.markdown("### 📂 All Registered Accounts")
        st.dataframe(st.session_state.all_accounts, use_container_width=True)
    else:
        st.info("No accounts opened yet. Go to **Open Account** to get started!")

elif menu == "🆕 Open Account":
    st.subheader("🆕 Open a New Account")

    with st.form("open_account_form"):
        account_title   = st.text_input("Full Name")
        f_name          = st.text_input("Father's Name")
        contact_number  = st.number_input("Contact Number", min_value=0, step=1, format="%d")
        cnic            = st.text_input("CNIC (e.g. 12345-1234567-1)")
        initial_deposit = st.number_input("Initial Deposit (Rs.)", min_value=0, step=100)
        submitted       = st.form_submit_button("✅ Open Account")

    if submitted:
        if not account_title or not f_name or not cnic:
            st.error("⚠️ Please fill in all required fields.")
        else:
            account = {}

            account_pin    = random.randint(1000, 9999)
            account_number = random.randint(10000, 99999)

            account["Title"]          = account_title.title()
            account["Father's Name"]  = f_name.title()
            account["Contact Number"] = contact_number
            account["CNIC"]           = cnic
            account["Balance"]        = initial_deposit
            account["Account Number"] = account_number
            account["Pin"]            = account_pin

            st.session_state.all_accounts.append(account)

            st.success(f"🎉 Account opened successfully! Welcome, **{account_title.title()}**!")
            st.info(
                f"📌 **Save these credentials!**\n\n"
                f"- **Account Number:** `{account_number}`\n"
                f"- **PIN:** `{account_pin}`"
            )
            st.markdown("#### 📄 Full Account Details:")
            st.json(account)

elif menu == "💰 Check Balance":
    st.subheader("💰 Check Your Balance")

    with st.form("check_balance_form"):
        account_num = st.number_input("Account Number", min_value=0, step=1, format="%d")
        pin         = st.number_input("PIN",            min_value=0, step=1, format="%d")
        submitted   = st.form_submit_button("🔍 Check Balance")

    if submitted:
        found = False

        for i in st.session_state.all_accounts:
            if account_num == i["Account Number"]:
                found = True
                if pin == i["Pin"]:
                    st.metric(
                        label=f"Balance for {i['Title']}",
                        value=f"Rs. {i['Balance']:,}"
                    )
                else:
                    st.error("❌ Incorrect PIN!")
                break

        if not found:
            st.error("❌ Account Not Found!")

elif menu == "➕ Deposit":
    st.subheader("➕ Deposit Amount")

    with st.form("deposit_form"):
        account_num = st.number_input("Account Number", min_value=0, step=1, format="%d")
        amount      = st.number_input("Deposit Amount (Rs.)", min_value=0, step=100)
        submitted   = st.form_submit_button("💵 Deposit")

    if submitted:
        found = False

        for account in st.session_state.all_accounts:
            if account_num == account["Account Number"]:
                found = True
                if amount > 0:
                    account["Balance"] += amount
                    st.success(
                        f"✅ Amount deposited successfully!\n\n"
                        f"**New Balance:** Rs. {account['Balance']:,}"
                    )
                else:
                    st.error("⚠️ Please enter an amount greater than 0.")
                break

        if not found:
            st.error("❌ Account Not Found!")

elif menu == "➖ Withdraw":
    st.subheader("➖ Withdraw Amount")

    with st.form("withdraw_form"):
        account_num = st.number_input("Account Number", min_value=0, step=1, format="%d")
        pin         = st.number_input("PIN",            min_value=0, step=1, format="%d")
        amount      = st.number_input("Withdraw Amount (Rs.)", min_value=0, step=100)
        submitted   = st.form_submit_button("💸 Withdraw")

    if submitted:
        found = False

        for account in st.session_state.all_accounts:
            if account_num == account["Account Number"]:
                found = True
                if pin == account["Pin"]:
                    if amount > 0:
                        if amount <= account["Balance"]:
                            account["Balance"] -= amount
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

        if not found:
            st.error("❌ Account Not Found!")

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Built By Zain Ali Khan With Streamlit</p>",
    unsafe_allow_html=True
)

