import streamlit as st
import pandas as pd
import plotly.express as px
import ast  # To parse strings representing lists

def main():
    # Page Configuration
    st.set_page_config(page_title="Nike Shoes Sales Dashboard", page_icon=":athletic_shoe:", layout="wide")

    # Load Data
    df = pd.read_csv("nike_shoes_sales_cleaned.csv")

    # Clean Column Names
    df.columns = df.columns.str.strip()

    # Sidebar Layout
    with st.sidebar:
        st.image("nike logo.jpg", width=780)
        st.header("Filter Options")

        # Sale Price Slider
        min_price, max_price = df['sale_price'].min(), df['sale_price'].max()
        selected_price_range = st.slider(
            "Select Sale Price Range (₹)",
            min_value=int(min_price),
            max_value=int(max_price),
            value=(int(min_price), int(max_price))
        )

        # Rating Multiselect with "Select All"
        unique_ratings = sorted(df['rating'].unique())
        select_all_ratings = st.checkbox("Select All Ratings", value=True)
        if select_all_ratings:
            selected_ratings = unique_ratings
        else:
            selected_ratings = st.multiselect(
                "Select Ratings",
                options=unique_ratings,
                default=unique_ratings
            )

        # Discount Slider with "Select All"
        min_discount, max_discount = df['discount'].min(), df['discount'].max()
        select_all_discounts = st.checkbox("Select All Discounts", value=True)
        if select_all_discounts:
            selected_discount_range = (int(min_discount), int(max_discount))
        else:
            selected_discount_range = st.slider(
                "Select Discount Range (%)",
                min_value=int(min_discount),
                max_value=int(max_discount),
                value=(int(min_discount), int(max_discount))
            )

    # Filter Data
    filtered_df = df[
        (df['sale_price'] >= selected_price_range[0]) &
        (df['sale_price'] <= selected_price_range[1]) &
        (df['discount'] >= selected_discount_range[0]) &
        (df['discount'] <= selected_discount_range[1]) &
        (df['rating'].isin(selected_ratings))
    ]

    # Main Dashboard Layout
    st.title(":athletic_shoe: NIKE SHOES SALES DASHBOARD")
    st.subheader("Explore Nike shoes Pricing, Reviews, Ratings, and Discounts using this **interactive dashboard**.")

    # Key Metrics
    st.markdown("---")
    st.subheader("📊 Sales Overview")
    col1, col2, col3 = st.columns(3)
    average_sale_price = filtered_df['sale_price'].mean() if not filtered_df.empty else 0
    average_discount = filtered_df['discount'].mean() if not filtered_df.empty else 0
    total_reviews = filtered_df['reviews'].sum() if not filtered_df.empty else 0
    col1.metric("Avg Sale Price (₹)", f"₹{average_sale_price:.2f}")
    col2.metric("Avg Discount (%)", f"{average_discount:.2f}%")
    col3.metric("Total Reviews", f"{total_reviews:,}")
    
        # Visualization Section 4: Top Products with Images (Side-by-Side Layout)
    st.markdown("---")
    st.subheader("🖼️ Top 5 Products by Reviews with Images")
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        top_products = filtered_df.sort_values(by="reviews", ascending=False).head(5)
        columns = st.columns(5)  # Create 5 columns for side-by-side display

        for idx, (col, row) in enumerate(zip(columns, top_products.iterrows())):
            _, row_data = row

            # Parse the image URLs if stored as a stringified list
            try:
                image_list = ast.literal_eval(row_data['images'])
                image_url = image_list[0] if isinstance(image_list, list) and len(image_list) > 0 else None
            except (ValueError, SyntaxError):
                image_url = None

            # Display product image and details
            with col:
                if image_url:
                    col.image(image_url, caption=f"{row_data['product_name']}\n{row_data['reviews']} Reviews", width=150)
                else:
                    col.warning(f"No image available for {row_data['product_name']}")
        # Visualization Section 1: Distribution and Insights
    st.markdown("---")
    st.subheader("📈 Distribution and Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💵 Sale Price Distribution")
        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
        else:
            fig_price_dist = px.histogram(
                filtered_df,
                x="sale_price",
                nbins=20,
                title="Price Distribution",
                color_discrete_sequence=px.colors.qualitative.Set1
            )
            fig_price_dist.update_layout(xaxis_title="Price (₹)", yaxis_title="Count")
            st.plotly_chart(fig_price_dist)

    with col2:
        st.subheader("📝 Reviews Distribution")
        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
        else:
            fig_reviews_dist = px.histogram(
                filtered_df,
                x="reviews",
                nbins=20,
                title="Reviews Distribution",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_reviews_dist.update_layout(xaxis_title="Reviews", yaxis_title="Count")
            st.plotly_chart(fig_reviews_dist)

    # Visualization Section 2: Relationships Between Metrics
    st.markdown("---")
    st.subheader("📉 Relationships Between Metrics")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📉 Discount vs Sale Price")
        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
        else:
            fig_discount_price = px.scatter(
                filtered_df,
                x="discount",
                y="sale_price",
                size="reviews",
                color="rating",
                title="Discount vs Sale Price",
                color_continuous_scale=px.colors.sequential.Viridis
            )
            st.plotly_chart(fig_discount_price)

    with col2:
        st.subheader("💬 Reviews vs Sale Price")
        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
        else:
            fig_reviews_price = px.scatter(
                filtered_df,
                x="sale_price",
                y="reviews",
                size="reviews",
                color="rating",
                title="Reviews vs Sale Price",
                color_continuous_scale=px.colors.sequential.Plasma
            )
            st.plotly_chart(fig_reviews_price)

    # Visualization Section 3: Advanced Insights
    st.markdown("---")
    st.subheader("💡 Advanced Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Sale Price Box Plot")
        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
        else:
            fig_box = px.box(
                filtered_df,
                y="sale_price",
                title="Sale Price Spread",
                color_discrete_sequence=px.colors.sequential.Purp
            )
            fig_box.update_layout(yaxis_title="Price (₹)")
            st.plotly_chart(fig_box)

    with col2:
        st.subheader("🔥 Correlation Heatmap")
        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
        else:
            corr = filtered_df[['sale_price', 'discount', 'rating', 'reviews']].corr()
            fig_heatmap = px.imshow(
                corr,
                text_auto=True,
                title="Correlation Heatmap",
                color_continuous_scale=px.colors.sequential.Reds
            )
            st.plotly_chart(fig_heatmap)



    # Footer
    st.markdown("---")
    st.markdown(
        """
        This dashboard provides an interactive and detailed analysis of Nike shoe sales data.
        - **Built with**: Python, Streamlit, and Plotly.
        - **Deployed on**: Streamlit Cloud.
        

        [Visit GitHub Repository](https://github.com/<your-username>/nike-shoes-sales) for the codebase.
        """
    )

if __name__ == "__main__":
    main()
