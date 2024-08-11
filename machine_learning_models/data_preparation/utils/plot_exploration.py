import pandas as pd
import matplotlib.pyplot as plt


def plot_exploration(df):
    for column in df.columns:
        # For numeric columns, use a histogram
        if pd.api.types.is_numeric_dtype(df[column]):
            mean = df[column].mean()
            median = df[column].median()
            std = df[column].std()

            plt.figure(figsize=(10, 4))
            plt.hist(df[column], bins=100, alpha=0.5, color="#0088ff")
            plt.axvline(
                mean, color="red", linestyle="solid", linewidth=2, label="Średnia"
            )
            plt.axvline(
                median, color="black", linestyle="dashed", linewidth=2, label="Mediana"
            )
            plt.axvline(
                mean - std,
                color="blue",
                linestyle="dotted",
                linewidth=2,
                label="Średnia - Odch. Std.",
            )
            plt.axvline(
                mean + std,
                color="green",
                linestyle="dotted",
                linewidth=2,
                label="Średnia + Odch. Std.",
            )
            plt.legend()
            plt.ylabel("Ilość punktów w rankingu")
            plt.xlabel("Ilość zawodniczek")
            plt.title(f"Rozkład wartości rankingu Glciko")
            plt.show()
        # For non-numeric columns, use a bar plot of value counts
        else:
            plt.figure(figsize=(10, 4))
            df[column].value_counts().plot(kind="bar")
            plt.title(f"Rozkład wartości dla {column}")
            plt.show()
