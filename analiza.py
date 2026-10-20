import pandas as pd

# Load the dataset
df = pd.read_csv("data.csv")

# Clean column names (replace dots for SQL/database compatibility)
df = df.rename(columns = {"Reached.on.Time_Y.N": "Reached_on_Time_Y_N"})

def sla_status(value):
    if value == 1:
        return "Reached on Time"
    else:
        return "Delayed"

df["SLA_Status"] = df["Reached_on_Time_Y_N"].apply(sla_status)

# Summary 
summary = df.groupby("Warehouse_block").agg(
    Total_Shipments=("ID", "count"),
    Avg_Cost=("Cost_of_the_Product", "mean"),
    Delayed_Shipments=("Reached_on_Time_Y_N", lambda x: (x == 0).sum()) # Counts the number of delayed shipments (where value == 0)
).reset_index()

# Calculate delay rate (%) per warehouse
summary["Delay_Rate_%"] = (summary["Delayed_Shipments"] / summary["Total_Shipments"]) * 100

print(summary.round(2))

# Export clean datasets to multi-tab Excel report
with pd.ExcelWriter("Logistics Report.xlsx") as writer:
    summary.round(2).to_excel(writer, sheet_name="Warehouses_Summary", index=False)
    df.to_excel(writer, sheet_name="Full_Data", index=False)

print("Logistics Report.xlsx has been created successfully.")