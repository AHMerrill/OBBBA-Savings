import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

st.title("Growth of Freedom Savings Account Over Time")

# Sidebar sliders
birth_year = st.sidebar.number_input("Birth Year", min_value=2000, max_value=2100, value=2025, step=1)
contribution = st.sidebar.slider("Annual Contribution ($)", 0, 5000, 5000, step=100)
interest_rate = st.sidebar.slider("Interest Rate (%)", 0.0, 15.0, 8.0, step=0.1)
stop_contrib_age = st.sidebar.slider("Stop Contributing Age", 0, 17, 17, step=1)

# Timeline of years
end_age = 65
years = np.arange(birth_year, birth_year + end_age + 1)
ages = np.arange(0, len(years))

# Initialize balance array
balance = np.zeros_like(years, dtype=float)

# Loop through each year
for i, (year, age) in enumerate(zip(years, ages)):
    if i == 0:
        # Year 0: government grant + possible parental contribution
        balance[i] = 1000
        if age <= stop_contrib_age:
            balance[i] += contribution
    else:
        # Grow previous balance
        balance[i] = balance[i - 1] * (1 + (interest_rate / 100))
        
        # Add contribution only if still contributing
        if age <= stop_contrib_age:
            balance[i] += contribution

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(years, balance, color='blue', linewidth=2)
ax.axvline(birth_year, color='green', linestyle='--', label=f"Start Saving (Year {birth_year})")
ax.axvline(birth_year + stop_contrib_age + 1, color='red', linestyle='--', label=f"Stop Contrib Age: {stop_contrib_age} (Year {birth_year + stop_contrib_age})")

# Formatter for Y axis
def millions(x, pos):
    if abs(x) >= 1_000_000:
        return f'${x*1e-6:.1f}M'
    else:
        return f'${x:,.0f}'

ax.yaxis.set_major_formatter(mtick.FuncFormatter(millions))
ax.set_xlabel("Calendar Year")
ax.set_ylabel("Account Balance")
ax.set_title("Growth of Freedom Savings Account Over Time (before withdrawal tax)")
ax.legend()
ax.grid(True)

# Show plot in Streamlit
st.pyplot(fig)

# Show balances at key years
st.subheader("Balances at Key Years")

for target_age in [18, 30, 60]:
    target_year = birth_year + target_age
    if target_year <= years[-1]:
        bal = balance[target_age]
        st.write(f"Balance in year {target_year} (age {target_age}): {millions(bal, None)}")
