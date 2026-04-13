import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:root64@localhost:5432/chaitra_db"
)

df = pd.read_sql("SELECT * FROM walmart_sales", engine)

# Sales distribution
title = "Distribution of Weekly Sales"
plt.figure()
sns.histplot(df["weekly_sales"], bins=50)
plt.title(title)

filename = title.lower().replace(" ", "_")
plt.savefig(f"../data/Outputs/visualize_basic/{filename}.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()


# Holiday vs Non-Holiday
title = "Holiday vs Non-Holiday Sales"
plt.figure()
sns.boxplot(x="isholiday", y="weekly_sales", data=df)
plt.title(title)

filename = title.lower().replace(" ", "_").replace("-", "")
plt.savefig(f"../data/Outputs/visualize_basic/{filename}.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()



