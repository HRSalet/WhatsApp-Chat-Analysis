import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analysis")
st.header("Chat Analysis Shows Here")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis",user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics of Chats")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

    # Most busy users
    if selected_user == 'Overall':
        st.title("Most Busy Users")
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index,x.values,color="red")
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # Most common words
    most_common_df = helper.most_common_words(selected_user, df)
    st.dataframe(most_common_df)

    fig, ax = plt.subplots()
    ax.bar(most_common_df[0],most_common_df[1],color="orange")
    plt.xticks(rotation=90)
    st.title("Most Common Words")
    st.pyplot(fig)
    
    # Emoji analysis
    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Emoji Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(x=emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        st.pyplot(fig)

    # Monthly timeline
    st.title("Monthly Time Analysis")
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Daily timeline
    st.title("Daily Time Analysis")
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color="green")
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Activity map
    st.title("Activity Map")
    col1,col2 = st.columns(2)

    with col1:
        st.header("Most Busy Days")
        busy_day = helper.week_activity_map(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(x=busy_day.index, height=busy_day.values, color="purple")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header("Most Busy Months")
        busy_month = helper.month_activity_map(selected_user, df)

        fig, ax = plt.subplots()
        ax.bar(x=busy_month.index, height=busy_month.values, color="magenta")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    # Online activity heatmap
    st.title("Online Activity Heatmap")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)