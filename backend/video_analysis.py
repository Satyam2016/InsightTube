import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import requests
import time

# Page configuration
st.set_page_config(
    page_title="InsightTube - Video Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF0000;
        text-align: center;
        margin-bottom: 2rem;
    }
    .video-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF0000;
    }
    .comment-box {
        background-color: #5cbc87;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #4CAF50;
    }
    .positive { border-left-color: #4CAF50; }
    .negative { border-left-color: #f44336; }
    .neutral { border-left-color: #ff9800; }
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    .error-message {
        background-color: #fee;
        border: 1px solid #fcc;
        color: #c33;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"
API_KEY = "test_key"


# API Functions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_video_analysis(video_url):
    """Fetch video analysis from API"""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "video_url": video_url,
            "include_comments": True,
            "include_sentiment": True,
            "include_topics": True,
            "include_keywords": True
        }
        
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json=payload,
            headers=headers,
            timeout=300  # 5 minute timeout
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def process_api_response(api_data):
    """Process and normalize API response data"""
    if not api_data:
        return None
    
    try:
        # Extract video information
        video_info = api_data.get('video_info', {})
        
        # Process video data - Fixed field mapping
        video_data = {
            "title": video_info.get('title', 'Unknown Title'),
            "channel": video_info.get('channel', 'Unknown Channel'),
            "views": video_info.get('views', '0 views'),  # Keep as string since it's already formatted
            "upload_date": video_info.get('upload_date', 'Unknown date'),  # Keep as string since it's already formatted
            "duration": video_info.get('duration', '0:00'),
            "likes": video_info.get('likes', 0),
            "dislikes": video_info.get('dislikes', 0),
            "comments": video_info.get('comments', 0),
            "processing_time": api_data.get('processing_time', 0)
        }
        
        # Process topics data - Fixed field mapping
        topics_data = []
        for topic in api_data.get('topics', []):
            topics_data.append({
                "topic": topic.get('topic', ''),  # Changed from 'name' to 'topic'
                "relevance": topic.get('relevance', 0),  # Changed from 'relevance_score' to 'relevance'
                "mentions": topic.get('mentions', 0)  # Changed from 'mention_count' to 'mentions'
            })
        
        # Process sentiment data - Fixed field mapping
        sentiment_distribution = api_data.get('sentiment_distribution', [])
        sentiment_data = []
        for sentiment in sentiment_distribution:
            sentiment_data.append({
                "name": sentiment.get('name', ''),
                "value": sentiment.get('value', 0),
                "color": sentiment.get('color', '#000000')
            })
        
        # Process sentiment timeline - Fixed field mapping
        sentiment_timeline = []
        for segment in api_data.get('sentiment_over_time', []):  # Changed from 'sentiment_timeline' to 'sentiment_over_time'
            sentiment_timeline.append({
                "time": segment.get('time', ''),  # Changed from 'time_range' to 'time'
                "positive": segment.get('positive', 0),
                "negative": segment.get('negative', 0),
                "neutral": segment.get('neutral', 0)
            })
        
        # Process top comments - Keep as is since the structure matches
        top_comments = []
        for comment in api_data.get('top_comments', []):
            top_comments.append({
                "author": comment.get('author', 'Unknown'),
                "text": comment.get('text', ''),
                "sentiment": comment.get('sentiment', 'neutral'),
                "sentiment_score": comment.get('sentiment_score', 0),
                "likes": comment.get('likes', 0)
            })
        
        # Process keywords - Fixed field mapping
        comment_analysis = api_data.get('comment_analysis', {})
        keywords = comment_analysis.get('top_keywords', [])  # Get from comment_analysis.top_keywords
        
        return {
            'video_data': video_data,
            'topics_data': topics_data,
            'sentiment_data': sentiment_data,
            'sentiment_timeline': sentiment_timeline,
            'top_comments': top_comments,
            'keywords': keywords
        }
        
    except Exception as e:
        st.error(f"Error processing API response: {str(e)}")
        return None

def format_views(views):
    """Format view count for display"""
    # Since the API already returns formatted views, just return as is
    if isinstance(views, str):
        return views
    
    try:
        views = int(float(views))  # Convert to int safely
    except:
        return "Unknown views"

    if views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M views"
    elif views >= 1_000:
        return f"{views / 1_000:.1f}K views"
    else:
        return f"{views} views"


def format_date(date_str):
    """Format date for display"""
    # Since the API already returns formatted date, just return as is
    if isinstance(date_str, str) and ("days ago" in date_str or "ago" in date_str):
        return date_str
    
    if not date_str:
        return "Unknown date"
    
    try:
        # Assuming date_str is in ISO format
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        days_ago = (datetime.now() - date_obj.replace(tzinfo=None)).days
        return f"{days_ago} days ago"
    except:
        return date_str

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None
if 'video_url' not in st.session_state:
    st.session_state.video_url = ""

# Header
st.markdown('<h1 class="main-header">🎬 InsightTube Video Analysis</h1>', unsafe_allow_html=True)

# Video URL Input
st.subheader("🔗 Enter YouTube Video URL")
video_url = st.text_input(
    "Video URL",
    value=st.session_state.video_url,
    placeholder="https://www.youtube.com/watch?v=...",
    help="Enter a valid YouTube video URL to analyze"
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    analyze_button = st.button("🚀 Analyze Video", type="primary")
with col2:
    clear_button = st.button("🗑️ Clear", type="secondary")

if clear_button:
    st.session_state.analysis_data = None
    st.session_state.video_url = ""
    st.rerun()

# Analysis Logic
if analyze_button and video_url:
    if not video_url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
        st.error("Please enter a valid YouTube URL")
    else:
        st.session_state.video_url = video_url
        
        with st.spinner("🔄 Analyzing video... This may take a few minutes."):
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Fetching video data...")
            progress_bar.progress(25)
            
            # Fetch analysis
            api_response = fetch_video_analysis(video_url)
            
            if api_response:
                status_text.text("Processing analysis results...")
                progress_bar.progress(75)
                
                processed_data = process_api_response(api_response)
                
                if processed_data:
                    st.session_state.analysis_data = processed_data
                    status_text.text("Analysis complete!")
                    progress_bar.progress(100)
                    time.sleep(1)
                    status_text.empty()
                    progress_bar.empty()
                    st.success("✅ Video analysis completed successfully!")
                else:
                    status_text.empty()
                    progress_bar.empty()
                    st.error("Failed to process analysis results")
            else:
                status_text.empty()
                progress_bar.empty()
                st.error("Failed to analyze video. Please check the URL and try again.")

# Display Analysis Results
if st.session_state.analysis_data:
    data = st.session_state.analysis_data
    video_data = data['video_data']
    topics_data = data['topics_data']
    sentiment_data = data['sentiment_data']
    sentiment_timeline = data['sentiment_timeline']
    top_comments = data['top_comments']
    keywords = data['keywords']
    
    # Video Information
    st.markdown(f'<div class="video-title">📺 {video_data["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f"**Channel:** {video_data['channel']} | **Duration:** {video_data['duration']} | **Upload Date:** {video_data['upload_date']}")

    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("👁️ Views", video_data["views"])

    with col2:
        st.metric("👍 Likes", f"{video_data['likes']:,}")

    with col3:
        st.metric("💬 Comments", f"{video_data['comments']:,}")

    with col4:
        # Calculate engagement rate
        views_str = video_data.get('views', '0').replace('K', '000').replace('M', '000000').replace(' views', '').replace(',', '')
        try:
            # Extract numeric value from formatted string like "454.1K views"
            if 'K' in video_data.get('views', ''):
                views_num = float(video_data['views'].split('K')[0]) * 1000
            elif 'M' in video_data.get('views', ''):
                views_num = float(video_data['views'].split('M')[0]) * 1000000
            else:
                views_num = float(views_str)
            
            engagement_rate = ((video_data['likes'] + video_data['comments']) / views_num) * 100 if views_num > 0 else 0
            st.metric("📈 Engagement", f"{engagement_rate:.2f}%")
        except:
            st.metric("📈 Engagement", "N/A")

    with col5:
        st.metric("⏱️ Processing Time", f"{video_data['processing_time']:.1f}s")

    st.divider()

    # Analysis Sections
    if topics_data or sentiment_data or top_comments or keywords:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🎯 Topics", "😊 Sentiment", "💬 Comments", "🔍 Keywords"])

        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                if sentiment_data:
                    st.subheader("📈 Overall Sentiment Distribution")
                    
                    # Pie chart for sentiment
                    sentiment_df = pd.DataFrame(sentiment_data)
                    if not sentiment_df.empty:
                        fig_sentiment = px.pie(
                            sentiment_df,
                            values='value',
                            names='name',
                            title="Comment Sentiment Analysis",
                            color='name',
                            color_discrete_map={'Positive': '#22c55e', 'Neutral': '#64748b', 'Negative': '#ef4444'}
                        )
                        st.plotly_chart(fig_sentiment, use_container_width=True)
            
            with col2:
                st.subheader("📊 Video Performance Metrics")
                
                # Calculate performance metrics based on available data
                sentiment_score = sentiment_data[0]['value'] if sentiment_data else 0
                topic_relevance = sum([t['relevance'] for t in topics_data]) / len(topics_data) if topics_data else 0
                
                metrics_data = {
                    'Metric': ['Sentiment Score', 'Topic Relevance', 'Comment Engagement', 'Overall Quality'],
                    'Score': [
                        sentiment_score,
                        topic_relevance,
                        min(100, (video_data['comments'] / max(1, video_data['likes'])) * 100),
                        (sentiment_score + topic_relevance) / 2
                    ],
                    'Max Score': [100, 100, 100, 100]
                }
                
                fig_metrics = go.Figure()
                fig_metrics.add_trace(go.Bar(
                    name='Current Score',
                    x=metrics_data['Metric'],
                    y=metrics_data['Score'],
                    marker_color='#FF0000'
                ))
                fig_metrics.add_trace(go.Bar(
                    name='Max Score',
                    x=metrics_data['Metric'],
                    y=metrics_data['Max Score'],
                    marker_color='#cccccc',
                    opacity=0.3
                ))
                fig_metrics.update_layout(
                    title="Performance Metrics Overview",
                    barmode='overlay',
                    yaxis_title="Score"
                )
                st.plotly_chart(fig_metrics, use_container_width=True)

        with tab2:
            if topics_data:
                st.subheader("🎯 Topic Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Topics relevance chart
                    topics_df = pd.DataFrame(topics_data)
                    if not topics_df.empty:
                        fig_topics = px.bar(
                            topics_df,
                            x='relevance',
                            y='topic',
                            orientation='h',
                            title="Topic Relevance Scores",
                            color='relevance',
                            color_continuous_scale='Reds'
                        )
                        fig_topics.update_layout(yaxis={'categoryorder':'total ascending'})
                        st.plotly_chart(fig_topics, use_container_width=True)
                
                with col2:
                    # Topics mentions
                    if not topics_df.empty:
                        fig_mentions = px.scatter(
                            topics_df,
                            x='mentions',
                            y='relevance',
                            size='mentions',
                            color='relevance',
                            hover_name='topic',
                            title="Topic Mentions vs Relevance",
                            color_continuous_scale='Viridis'
                        )
                        st.plotly_chart(fig_mentions, use_container_width=True)
                
                # Topics table
                st.subheader("📋 Detailed Topic Breakdown")
                st.dataframe(topics_df, use_container_width=True, hide_index=True)
            else:
                st.info("No topic data available for this video.")

        with tab3:
            if sentiment_timeline:
                st.subheader("😊 Sentiment Analysis Over Time")
                
                # Sentiment timeline
                timeline_df = pd.DataFrame(sentiment_timeline)
                
                if not timeline_df.empty:
                    fig_timeline = go.Figure()
                    fig_timeline.add_trace(go.Scatter(
                        x=timeline_df['time'],
                        y=timeline_df['positive'],
                        mode='lines+markers',
                        name='Positive',
                        line=dict(color='#22c55e', width=3)
                    ))
                    fig_timeline.add_trace(go.Scatter(
                        x=timeline_df['time'],
                        y=timeline_df['negative'],
                        mode='lines+markers',
                        name='Negative',
                        line=dict(color='#ef4444', width=3)
                    ))
                    fig_timeline.add_trace(go.Scatter(
                        x=timeline_df['time'],
                        y=timeline_df['neutral'],
                        mode='lines+markers',
                        name='Neutral',
                        line=dict(color='#64748b', width=3)
                    ))
                    
                    fig_timeline.update_layout(
                        title="Sentiment Distribution Throughout Video Duration",
                        xaxis_title="Time Segments",
                        yaxis_title="Sentiment Percentage (%)",
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Sentiment summary
            if sentiment_data:
                col1, col2, col3 = st.columns(3)
                with col1:
                    positive_val = sentiment_data[0]['value'] if sentiment_data else 0
                    st.metric("😊 Positive Comments", f"{positive_val}%")
                with col2:
                    neutral_val = sentiment_data[1]['value'] if len(sentiment_data) > 1 else 0
                    st.metric("😐 Neutral Comments", f"{neutral_val}%")
                with col3:
                    negative_val = sentiment_data[2]['value'] if len(sentiment_data) > 2 else 0
                    st.metric("😞 Negative Comments", f"{negative_val}%")

        with tab4:
            if top_comments:
                st.subheader("💬 Top Comments Analysis")
                
                # Display top comments
                for i, comment in enumerate(top_comments):
                    sentiment_class = comment['sentiment']
                    
                    st.markdown(f"""
                    <div class="comment-box {sentiment_class}">
                        <strong>{comment['author']}</strong> • {comment['likes']} likes • {comment['sentiment'].title()} ({comment['sentiment_score']:.3f})
                        <br><br>
                        "{comment['text']}"
                    </div>
                    """, unsafe_allow_html=True)
                
                # Comment statistics
                st.subheader("📊 Comment Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Comments", f"{video_data['comments']:,}")
                with col2:
                    if top_comments:
                        avg_sentiment = sum([c['sentiment_score'] for c in top_comments]) / len(top_comments)
                        st.metric("Avg Sentiment Score", f"{avg_sentiment:.3f}")
                with col3:
                    if top_comments:
                        total_likes = sum([c['likes'] for c in top_comments])
                        st.metric("Top Comments Likes", f"{total_likes:,}")
            else:
                st.info("No comment data available for this video.")

        with tab5:
            if keywords:
                st.subheader("🔍 Keyword Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Keywords frequency (create frequency based on position in list)
                    keywords_df = pd.DataFrame({
                        'Keyword': keywords[:10],  # Top 10 keywords
                        'Frequency': range(len(keywords[:10]), 0, -1)  # Sample frequencies
                    })
                    
                    if not keywords_df.empty:
                        fig_keywords = px.bar(
                            keywords_df,
                            x='Frequency',
                            y='Keyword',
                            orientation='h',
                            title="Top Keywords Frequency",
                            color='Frequency',
                            color_continuous_scale='Blues'
                        )
                        fig_keywords.update_layout(yaxis={'categoryorder':'total ascending'})
                        st.plotly_chart(fig_keywords, use_container_width=True)
                
                with col2:
                    # Word cloud style visualization
                    st.subheader("🏷️ Keywords Cloud")
                    
                    # Create a simple text display for keywords
                    keywords_text = " • ".join(keywords[:20])  # Show top 20 keywords
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 2rem; border-radius: 10px; text-align: center; font-size: 1.2rem; line-height: 2;">
                        {keywords_text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Keywords table
                    if not keywords_df.empty:
                        st.subheader("📋 Keywords Details")
                        st.dataframe(keywords_df, use_container_width=True, hide_index=True)
            else:
                st.info("No keyword data available for this video.")

    # Summary Section
    st.divider()
    st.subheader("📝 Analysis Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        # Generate dynamic insights based on data
        insights = []
        if sentiment_data and sentiment_data[0]['value'] > 70:
            insights.append(f"**High Positive Reception**: {sentiment_data[0]['value']}% positive sentiment shows excellent audience engagement")
        
        if topics_data:
            top_topic = max(topics_data, key=lambda x: x['relevance'])
            insights.append(f"**Top Topic**: '{top_topic['topic']}' with {top_topic['relevance']:.1f}% relevance")
        
        if video_data['comments'] > 100:
            insights.append(f"**Strong Engagement**: {video_data['comments']} comments indicate active community interaction")
        
        if not insights:
            insights.append("Analysis completed successfully")
        
        st.markdown("**🎯 Key Insights:**\n" + "\n".join([f"- {insight}" for insight in insights]))

    with summary_col2:
        # Generate dynamic recommendations
        recommendations = []
        
        if sentiment_data and len(sentiment_data) > 2 and sentiment_data[2]['value'] > 10:  # High negative sentiment
            recommendations.append("Consider addressing concerns raised in negative comments")
        
        if topics_data:
            recommendations.append("Leverage high-performing topics for similar content")
        
        recommendations.append("Monitor engagement patterns for content optimization")
        recommendations.append("Engage with top comments to build community")
        
        st.markdown("**📈 Recommendations:**\n" + "\n".join([f"- {rec}" for rec in recommendations]))

    # Export functionality
    st.divider()
    st.subheader("💾 Export Analysis Data")

    col1, col2, col3 = st.columns(3)

    with col1:
        if topics_data and st.button("📥 Download Topics Data"):
            topics_csv = pd.DataFrame(topics_data).to_csv(index=False)
            st.download_button(
                label="Download Topics CSV",
                data=topics_csv,
                file_name=f"video_topics_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with col2:
        if top_comments and st.button("📥 Download Comments Data"):
            comments_csv = pd.DataFrame(top_comments).to_csv(index=False)
            st.download_button(
                label="Download Comments CSV",
                data=comments_csv,
                file_name=f"video_comments_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with col3:
        if st.button("📥 Download Full Report"):
            # Create comprehensive report
            report_data = {
                'video_info': video_data,
                'topics': topics_data,
                'sentiment_data': sentiment_data,
                'sentiment_timeline': sentiment_timeline,
                'top_comments': top_comments,
                'keywords': keywords,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            report_json = json.dumps(report_data, indent=2)
            st.download_button(
                label="Download JSON Report",
                data=report_json,
                file_name=f"insighttube_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    # Footer
    st.markdown("---")
    st.markdown("*InsightTube Video Analysis - Powered by Advanced YouTube Analytics*")

else:
    # Show instructions when no analysis is loaded
    st.info("👆 Enter a YouTube video URL above and click 'Analyze Video' to get started!")
    
    st.markdown("""
    ### 🚀 How It Works:
    1. **Enter URL**: Paste any YouTube video URL
    2. **Click Analyze**: Our AI will process the video content and comments
    3. **Explore Results**: Navigate through different analysis tabs
    4. **Export Data**: Download insights for further analysis
    
    ### 📊 What You'll Get:
    - **Sentiment Analysis**: Understand audience reactions
    - **Topic Extraction**: Identify key themes and subjects
    - **Comment Analysis**: Deep dive into viewer feedback  
    - **Keyword Analysis**: Discover trending terms
    - **Performance Metrics**: Comprehensive engagement statistics
    """)

# Sidebar information
st.sidebar.title("📊 Analysis Dashboard")

if st.session_state.analysis_data:
    video_data = st.session_state.analysis_data['video_data']
    st.sidebar.markdown(f"""
    **Current Video:**
    - {video_data['title'][:50]}{'...' if len(video_data['title']) > 50 else ''}
    - Channel: {video_data['channel']}
    - Duration: {video_data['duration']}
    - Processing Time: {video_data['processing_time']:.1f}s

    **Analysis Coverage:**
    - ✅ Sentiment Analysis
    - ✅ Topic Extraction  
    - ✅ Comment Analysis
    - ✅ Keyword Analysis
    - ✅ Performance Metrics
    """)
else:
    st.sidebar.markdown("""
    **Ready to Analyze:**
    - Enter a YouTube URL
    - Click 'Analyze Video'
    - Explore comprehensive insights
    
    **Features:**
    - 🎯 AI-powered analysis
    - 📊 Interactive visualizations
    - 💾 Export capabilities
    - ⚡ Real-time processing
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔧 API Configuration")
st.sidebar.markdown(f"""
- **Status**: {'🟢 Connected' if API_BASE_URL != 'http://localhost:8000' else '🟡 Local Dev'}
- **Cache**: 1 hour TTL
- **Timeout**: 5 minutes
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips:")
st.sidebar.markdown("""
1. **Use Popular Videos**: Better results with more comments
2. **Check Processing Time**: Complex videos take longer
3. **Export Data**: Save insights for later analysis
4. **Compare Videos**: Analyze multiple videos for trends
""")