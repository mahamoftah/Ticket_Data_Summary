import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

class EDA:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._prepare_data()

    def _prepare_data(self):
        """Ensure date columns are in datetime format."""
        self.df['ACCEPTANCE_TIME'] = pd.to_datetime(self.df['ACCEPTANCE_TIME'], errors='coerce')
        self.df['COMPLETION_TIME'] = pd.to_datetime(self.df['COMPLETION_TIME'], errors='coerce')
        self.df['Resolution_Time_Hours'] = (self.df['COMPLETION_TIME'] - self.df['ACCEPTANCE_TIME']).dt.total_seconds() / 3600


    def plot_service_category_distribution(self):
        """Plot number of tickets per service category."""
        category_counts = self.df['SERVICE_CATEGORY'].value_counts()

        fig, ax = plt.subplots(figsize=(10, 4))
        category_counts.plot(kind='barh', ax=ax)
        ax.set_title('Tickets by Service Category')
        ax.set_xlabel('Number of Tickets')
        ax.set_ylabel('Service Category')
        st.pyplot(fig)

    def plot_product_distribution(self):
        """Plot number of tickets per product."""
        if 'PRODUCT' in self.df.columns:
            product_counts = self.df['PRODUCT'].value_counts()

            fig, ax = plt.subplots(figsize=(10, 4))
            product_counts.plot(kind='barh', ax=ax)
            ax.set_title('Tickets by Product')
            ax.set_xlabel('Number of Tickets')
            ax.set_ylabel('Product')
            st.pyplot(fig)

    def plot_top_issue_causes(self, top_n=5):
        """Plot the top N most common issue causes."""
        top_causes = self.df[self.df['ORDER_DESCRIPTION_3_MAXIMUM'].str.lower() != 'stable']['CAUSE'].value_counts().head()

        fig, ax = plt.subplots(figsize=(10, 4))
        top_causes.plot(kind='barh', color='orange', ax=ax)
        ax.set_title(f'Top {top_n} Common Issue Causes')
        ax.set_xlabel('Number of Tickets')
        ax.set_ylabel('Cause')
        st.pyplot(fig)

    def show_average_resolution_time(self):
        """Show average resolution time in hours."""
        average_resolution = self.df['Resolution_Time_Hours'].mean()
        st.metric(label="Average Resolution Time (hours)", value=f"{average_resolution:.2f}")
        return average_resolution