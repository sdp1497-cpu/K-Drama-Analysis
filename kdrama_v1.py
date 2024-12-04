import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

file_path = "top100_kdrama_aug_2023.csv"  
kdata = pd.read_csv(file_path)
most_frequent_network = kdata['Network'].mode()[0]
kdata['Network'].fillna(most_frequent_network, inplace=True)

# Title of the App
st.title(":heart: The Rise and Evolution of K-Dramas in 2023 :heart:")

# **Story and Visualizations**

st.markdown("""
Korean dramas (K-dramas) have transitioned from being regional entertainment staples to global cultural touchstones. With compelling narratives, stellar acting, and production quality, they have gained massive followings across continents. This analysis uncovers key trends driving this success, delves into the factors influencing audience preferences, and highlights their diverse storytelling techniques.
""")

# **Visualization 1: Number of K-Dramas by Year**
st.subheader("Chapter 1: The Surge in K-Drama Production")
st.markdown("In recent years, the K-drama industry has entered what can be considered its golden era. The sheer volume of productions has skyrocketed, with over 50% of top-rated dramas released after 2017.Global streaming platforms like Netflix and the pandemic-driven shift to at-home entertainment have fueled a boom in K-drama production, making them more accessible than ever..")
year_counts = kdata['Year of release'].value_counts().sort_index().reset_index()
year_counts.columns = ['Year of Release', 'Number of Dramas']
fig = px.bar(
    year_counts,
    x='Year of Release',
    y='Number of Dramas',
    title='Number of K-Dramas by Year',
    text='Number of Dramas',
    color='Number of Dramas',
    color_continuous_scale=px.colors.sequential.Blues  # Use a valid color scale
)
fig.update_layout(
    title_font_size=18,
    xaxis_title='Year of Release',
    yaxis_title='Number of Dramas',
    font=dict(size=14),
    template='plotly_white'
)
fig.update_traces(
    texttemplate='%{text}',
    textposition='outside',
    marker=dict(line=dict(color='white', width=1))
)
st.plotly_chart(fig)

# **Visualization 2: Episode Count vs. Rating**
st.subheader("Chapter 2: The Magic of Short and Sweet")
st.markdown("While some viewers appreciate long story arcs, shorter K-dramas dominate ratings. Concise storytelling paired with emotional depth creates a winning formula..")
fig = px.scatter(
    kdata,
    x='Number of Episode',
    y='Rating',
    title='Episode Count vs. Rating',
    labels={'Number of Episode': 'Number of Episodes', 'Rating': 'Rating'},
    color='Rating',  # Color points by rating for a gradient effect
    color_continuous_scale=px.colors.sequential.Turbo,
    hover_data=['Name', 'Genre', 'Year of release']  # Add hover details
)

fig.update_layout(
    title_font_size=18,
    xaxis_title='Number of Episodes',
    yaxis_title='Rating',
    font=dict(size=14),
    template='plotly_white'
)

st.plotly_chart(fig)
st.markdown("""
Dramas with fewer than 16 episodes often outperform longer series in ratings, underscoring the audience's preference for tightly woven plots.
""")

# **Visualization 3: Genre Distribution**
st.subheader("Chapter 3: A Genre for Every Mood ")
st.markdown("From romance to thrillers, K-dramas offer something for everyone. While traditional romance and life dramas remain staples, action and medical genres are seeing steady growth.")
genres = kdata['Genre'].str.split(',').explode().str.strip().value_counts().head(10)
genres = kdata['Genre'].str.split(',').explode().str.strip()
top_genres = genres.value_counts().head(10).reset_index()
top_genres.columns = ['Genre', 'Count']  # Rename columns for clarity
fig_genres = px.bar(
    top_genres,
    x='Genre',
    y='Count',
    title='Top 10 Most Common Genres in K-Dramas',
    labels={'Genre': 'Genre', 'Count': 'Number of Dramas'},
    text='Count',  
    color='Count',  
    color_continuous_scale=px.colors.sequential.PuRd  # Choose a vibrant color scale
)
fig_genres.update_layout(
    title_font_size=18,
    xaxis_title='Genre',
    yaxis_title='Number of Dramas',
    font=dict(size=14),
    template='plotly_white',
    xaxis=dict(tickangle=45), 
)
fig_genres.update_traces(
    texttemplate='%{text}',
    textposition='outside',
    marker=dict(line=dict(color='white', width=1)) 
)
st.plotly_chart(fig_genres)
st.markdown("Genres like action and thriller—often featuring intricate plots and edge-of-the-seat moments—are gaining traction among younger viewers, breaking the stereotype of K-dramas as purely romance-centric.")

# **Visualization 4: Top Networks by Dramas**
st.subheader("Chapter 4: Platforms That Define K-Dramas")
st.markdown("The Titans of Distribution Netflix, tvN, and JTBC have emerged as powerhouses, delivering the highest-rated dramas. Their global distribution networks and investment in high-quality content make them industry leaders.")
network_counts = kdata['Network'].str.split(',').explode().str.strip().value_counts().head(10)
network_counts = kdata['Network'].str.split(',', expand=True).stack().str.strip().value_counts()
top_networks = network_counts[:10].reset_index()
top_networks.columns = ['Network', 'Count']  # Rename columns for clarity
fig = px.bar(
    top_networks,
    x='Network',
    y='Count',
    title='Top Networks by Number of High-Ranking Dramas',
    labels={'Network': 'Network', 'Count': 'Number of Dramas'},
    text='Count',  # Add data labels to the bars
    color='Count',  # Color bars based on the count
    color_continuous_scale=px.colors.sequential.Peach  # Use a clean, vibrant color scale
)
fig.update_layout(
    title_font_size=18,
    xaxis_title='Network',
    yaxis_title='Number of Dramas',
    font=dict(size=14),
    template='plotly_white',
    xaxis=dict(tickangle=45),  # Rotate x-axis labels for readability
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for a cleaner look
)
fig.update_traces(
    texttemplate='%{text}',
    textposition='outside',
    marker=dict(line=dict(color='white', width=1))  # Add borders for bars
)
st.plotly_chart(fig) 
st.markdown("Netflix's global accessibility and tvN's rich storytelling have made them go-to platforms for premium K-dramas, with consistent critical and audience acclaim.")


# **Visualization 5: The Rhythm of K-Drama Releases**
st.subheader("Chapter 5: The Rhythm of K-Drama Releases")
st.markdown("K-Dramas are not just about captivating stories; their scheduling plays a pivotal role in engaging viewers. By analyzing the days on which dramas are aired, we uncover patterns that reflect audience preferences and broadcasting strategies.")
days_aired = kdata['Aired On'].str.split(',').explode().str.strip().value_counts().reset_index()
days_aired.columns = ['Day', 'Count']

# Create the Plotly pie chart
fig_days = px.pie(
    days_aired,
    names='Day',
    values='Count',
    title='Proportion of Dramas Aired on Different Days',
    labels={'Day': 'Day of the Week'},
    color='Day',  # Assign colors by day
    color_discrete_sequence=px.colors.qualitative.T10
      # Use a pastel color scheme
)

# Customize layout for aesthetics
fig_days.update_traces(
    textinfo='percent+label',  # Show both percentages and labels
    pull=[0.1 if i == days_aired['Count'].idxmax() else 0 for i in range(len(days_aired))],  # Highlight the largest slice
    marker=dict(line=dict(color='white', width=1))  # Add borders for better distinction
)

fig_days.update_layout(
    title_font_size=18,
    font=dict(size=14),
    template='plotly_white'
)

st.plotly_chart(fig_days) 
st.markdown("Certain days, like Friday and Saturday, dominate the schedule for K-Drama releases.Friday & Saturday are prime days for airing new episodes, as they coincide with the start of the weekend, when viewers are more likely to have leisure time to relax and binge-watch. While weekdays are less dominant, they cater to a dedicated audience that prefers a consistent schedule to unwind after work or school. The chart highlights these patterns, with Friday often taking the lead, emphasizing its role as the gateway to the weekend binge. The rhythm of K-Drama airing days mirrors the careful planning behind their success. From weekday consistency to weekend excitement, the schedule ensures that dramas capture and hold viewer attention, contributing significantly to their popularity and cultural impact.")


# **Visualization 6: Proportion of Dramas Aired on Different Days**
st.subheader("Chapter 6: Thematic Boldness")
st.markdown("K-dramas are no longer confined to lighthearted or family-friendly themes. Recent years have seen a surge in mature, gritty narratives targeting a more diverse demographic.")
content_trends = kdata.groupby(['Year of release', 'Content Rating']).size().reset_index(name='Count')
fig_content = px.area(
    content_trends,
    x='Year of release',
    y='Count',
    color='Content Rating',
    title='Content Rating Trends Over the Years',
    labels={'Year of release': 'Year of Release', 'Count': 'Number of Dramas', 'Content Rating': 'Content Rating'},
    color_discrete_sequence=px.colors.sequential.Purp  # Use a gradient color palette
)

fig_content.update_layout(
    title_font_size=18,
    xaxis_title='Year of Release',
    yaxis_title='Number of Dramas',
    font=dict(size=14),
    template='plotly_white',
    legend_title_text='Content Rating',
    legend=dict(
        title_font_size=14,
        font_size=12,
        x=1.05,
        y=1.0
    )
)
fig_content.update_traces(
    mode='lines+markers',
    marker=dict(size=5, line=dict(width=1, color='DarkSlateGrey'))
)
st.plotly_chart(fig_content) 
st.markdown("18+ Restricted content has gained prominence, showcasing bold storytelling that resonates with modern audiences craving realism and complexity.")

# **Visualization 7: Proportion of Dramas Aired on Different Days**
st.subheader("Chapter 7: The Essence of Themes")
st.markdown("K-Dramas are renowned not only for their gripping storylines but also for the unique themes and motifs that resonate with viewers. These recurring themes, captured in tags, reveal what audiences connect with most deeply. By analyzing the most common tags, we gain insight into the core elements that define popular K-Dramas.")
tags = kdata['Tags'].str.split(',').explode().str.strip()
top_tags = tags.value_counts().head(10).reset_index()
top_tags.columns = ['Tag', 'Count']
fig_tags_hbar = px.bar(
    top_tags,
    x='Count',
    y='Tag',
    title='Top 10 Most Common Tags in K-Dramas',
    orientation='h',
    text='Count',
    color='Count',
    color_continuous_scale='Burg'
)

fig_tags_hbar.update_layout(xaxis_title='Number of Dramas', yaxis_title='Tag')
st.plotly_chart(fig_tags_hbar)
st.markdown("The analysis reveals recurring themes such as Family, Friendship, Romance, and Secrets, which are central to the storytelling fabric of K-Dramas. For instance, Family and Friendship themes highlight the importance of relationships and bonds, a hallmark of emotional Korean storytelling. Romance continues to dominate as a universal favorite, while Secrets and Betrayal reflect the love for suspense and drama among audiences. These common tags not only shape narratives but also connect deeply with viewers on emotional and psychological levels.")


# **Top 10 Dramas Highlight Table**
st.subheader("Chapter 8: The Hall of Fame")
st.markdown("What makes a K-drama unforgettable? A mix of high ratings, groundbreaking narratives, and exceptional casts. Highlighting the top-rated dramas provides a glimpse into what works.")
# Prepare data for the table
top_dramas = kdata[['Name', 'Rating', 'Genre', 'Year of release', 'Network']].sort_values(by='Rating', ascending=False).head(10)

# Create a table using Plotly
fig_table = go.Figure(data=[
    go.Table(
        header=dict(
            values=["<b>Drama Name</b>", "<b>Rating</b>", "<b>Genre</b>", "<b>Year of Release</b>", "<b>Network</b>"],
            fill_color='yellowgreen',
            align='left',
            font=dict(color='black', size=12),
            height=30
        ),
        cells=dict(
            values=[top_dramas[col] for col in top_dramas.columns],
            fill_color='lightyellow',
            align='left',
            font=dict(color='black', size=11),
            height=25
        )
    )
])

# Update layout for aesthetics
fig_table.update_layout(
    title="Top 10 K-Dramas by Rating",
    title_font_size=18,
    title_x=0.5,
    template='plotly_white',
    margin=dict(l=10, r=20, t=40, b=20)  # Adjust margins
)


st.plotly_chart(fig_table)
st.markdown("Dramas like Move to Heaven and Hospital Playlist stand out for their deep emotional resonance and relatability, earning them spots in the hall of fame.")
st.markdown("Epilogue: K-Dramas and the Future As K-dramas continue to evolve, they are redefining storytelling in the global entertainment industry. The data highlights the industry's adaptability, offering timeless romance, nail-biting thrillers, and socially relevant themes. With the world as their stage, K-dramas are here to stay.")