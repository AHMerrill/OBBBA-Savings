import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

st.title("Growth of Savings Account Over Time")

# Sidebar sliders
start_age = st.sidebar.slider("Start Saving Age", 0, 17, 0, step=1)
contribution = st.sidebar.slider("Annual Contribution ($)", 0, 5000, 5000, step=100)
interest_rate = st.sidebar.slider("Interest Rate (%)", 0.0, 15.0, 8.0, step=0.1)
stop_contrib_age = st.sidebar.slider("Stop Contributing Age", 0, 17, 17, step=1)

# Run calculations
initial_gov_contribution = 1000
end_age = 65
years = np.arange(0, end_age + 1)
balance = np.zeros_like(years, dtype=float)

for i, age in enumerate(years):
    if i == 0:
        balance[i] = initial_gov_contribution
    else:
        balance[i] = balance[i - 1] * (1 + (interest_rate / 100))
        if start_age <= age <= stop_contrib_age:
            balance[i] += contribution

# Create plot
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(years, balance, color='blue', linewidth=2)
ax.axvline(start_age, color='green', linestyle='--', label=f"Start Saving Age: {start_age}")
ax.axvline(stop_contrib_age, color='red', linestyle='--', label=f"Stop Contrib Age: {stop_contrib_age}")

def millions(x, pos):
    if abs(x) >= 1_000_000:
        return f'${x*1e-6:.1f}M'
    else:
        return f'${x:,.0f}'

ax.yaxis.set_major_formatter(mtick.FuncFormatter(millions))
ax.set_xlabel("Age")
ax.set_ylabel("Account Balance")
ax.set_title("Growth of Savings Account Over Time (before withdrawal tax)")
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)

# Show balances at specific ages
st.subheader("Balances at Key Ages")

for target_age in [18, 30, 60]:
    if target_age <= end_age:
        bal = balance[target_age]
        st.write(f"Balance at age {target_age}: {millions(bal, None)}")
