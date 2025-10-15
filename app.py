import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import json
import os
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

# Global theming for charts (light theme)
# Palette from info/style-guide.md
PALETTE = {
    "sunshine": "#eec362",
    "eggwhite": "#f5edd2",
    "brick": "#b85829",
    "olive": "#83a066",
    "deep_brown": "#2b1414",
    "light_blue": "#2c6398",
}

COLOR_SEQUENCE = [
    PALETTE["light_blue"],
    PALETTE["brick"],
    PALETTE["olive"],
    PALETTE["sunshine"],
    PALETTE["deep_brown"],
]

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = COLOR_SEQUENCE

# Page configuration
st.set_page_config(
    page_title="AISSA Track Record",
    page_icon="images/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external CSS
with open("styles.css", "r") as f:
    css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

def create_image_placeholder(description, side="below", image_url=None):
    """Display actual images with descriptions"""
    if image_url and os.path.exists(image_url):
        if side == "below":
            st.image(image_url, caption=description, width='content')
        else:
            # For side images, use fixed square dimensions
            st.image(image_url, caption=description, width=200)
    else:
        # Fallback to placeholder if image doesn't exist
        if side == "below":
            return st.markdown(f"""
            <div class="image-placeholder">
                📸 Image Placeholder: {description}
            </div>
            """, unsafe_allow_html=True)
        else:
            return st.markdown(f"""
            <div class="image-placeholder" style="width: 200px; height: 200px; display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                📸 Image Placeholder:<br>{description}
            </div>
            """, unsafe_allow_html=True)

def create_side_by_side_layout(text_content, image_description, image_url=None):
    """Create a side-by-side layout with text taking 2/3 and image taking 1/3 of the space"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(text_content, unsafe_allow_html=True)
    
    with col2:
        if image_url and os.path.exists(image_url):
            st.image(image_url, caption=image_description, use_column_width=True)
        else:
            st.markdown(f"""
            <div class="image-placeholder-square">
                📸 Image Placeholder:<br>{image_description}
            </div>
            """, unsafe_allow_html=True)

def create_demographics_chart():
    """Create demographics pie chart for 2024 AISF course"""
    # Demographics data from PDF (approximate)
    exp_data = pd.DataFrame({
        'Experience': ['Undergraduate', 'Masters', 'PhD', 'Mid-Career', 'Experienced', 'Early Career'],
        'Percentage': [10, 10, 5, 35, 25, 15]
    })
    
    fig = px.pie(
        exp_data,
        values='Percentage',
        names='Experience',
        title='AISF Course Participant Demographics (2024)',
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        font=dict(size=12),
        showlegend=True,
        height=400
    )
    
    return fig

def create_participant_growth_chart():
    """Create participant growth bar chart across years"""
    years = ['2023', '2024', '2025']
    participants = [85, 98, 120]  # Approximate numbers based on data
    
    fig = go.Figure(data=[
        go.Bar(
            x=years,
            y=participants,
            marker_color=[PALETTE["light_blue"], PALETTE["brick"], PALETTE["olive"]],
            text=participants,
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Participant Growth Across Years',
        xaxis_title='Year',
        yaxis_title='Total Participants',
        height=400,
        font=dict(size=12),
        template='plotly_white'
    )
    
    return fig

def create_course_completion_chart():
    """Create course completion comparison chart"""
    tracks = ['Technical Track', 'Governance Track']
    completed = [20, 54]  # From 2024 data
    total = [39, 92]  # From 2024 data
    
    fig = go.Figure(data=[
        go.Bar(name='Completed', x=tracks, y=completed, marker_color=PALETTE["olive"]),
        go.Bar(name='Total Participants', x=tracks, y=total, marker_color=PALETTE["light_blue"])
    ])
    
    fig.update_layout(
        title='AISF Course Completion by Track (2024)',
        xaxis_title='Track',
        yaxis_title='Number of Participants',
        barmode='group',
        height=400,
        font=dict(size=12),
        template='plotly_white'
    )
    
    return fig

def generate_pdf_report():
    """Generate a PDF report of the track record"""
    # This would use reportlab or weasyprint to generate PDF
    # For now, return a placeholder
    return "PDF generation functionality would be implemented here using reportlab or weasyprint"

def create_share_link():
    """Create a shareable link for the current view"""
    # This would generate a shareable URL
    return "https://aisafetysa.com/track-record"

def add_search_functionality():
    """Add search functionality to filter content"""
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    search_term = st.text_input("🔍 Search for keywords (e.g., 'research', 'courses', 'events'):", 
                               placeholder="Type to filter content...")
    st.markdown('</div>', unsafe_allow_html=True)
    return search_term

def add_export_buttons():
    """Add export and share buttons"""
    st.markdown('<div class="export-buttons">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download PDF Report", key="download_pdf"):
            st.success("PDF download would be implemented here")
    
    with col2:
        if st.button("🔗 Share Link", key="share_link"):
            share_url = create_share_link()
            st.success(f"Share this link: {share_url}")
    
    with col3:
        if st.button("📊 Export Data", key="export_data"):
            st.success("Data export would be implemented here")
    
    st.markdown('</div>', unsafe_allow_html=True)

def load_year_data(year):
    """Load data for a specific year from JSON file"""
    try:
        with open(f"data/{year}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Data file for year {year} not found")
        return None
    except json.JSONDecodeError:
        st.error(f"Error parsing JSON data for year {year}")
        return None

def calculate_metrics():
    """Calculate metrics programmatically from the JSON data - dynamically loops through all years"""
    
    # Initialize totals
    total_courses = 0
    total_participants = 0
    total_research_papers = 0
    total_workshops_events = 0
    total_university_groups = 0
    total_individual_impacts = 0
    
    # Get all available years dynamically
    years = ["2023", "2024", "2025"]
    
    for year in years:
        data = load_year_data(year)
        if not data:
            continue
            
        # Count courses
        courses = data.get("courses", [])
        total_courses += len(courses)
        
        # Count university groups
        university_groups = data.get("university_groups", [])
        total_university_groups += len(university_groups)
        
        # Count research papers
        research_items = data.get("research", [])
        total_research_papers += len(research_items)
        
        # Count individual impacts
        individual_impacts = data.get("individual_impacts", [])
        total_individual_impacts += len(individual_impacts)
        
        # Count participants from courses
        for course in courses:
            # Count participants from course completion data
            if "completion" in course:
                completion = course["completion"]
                if "total_completed" in completion:
                    total_participants += completion["total_completed"]
                elif "technical_completed" in completion and "governance_completed" in completion:
                    total_participants += completion["technical_completed"] + completion["governance_completed"]
            
            # Count participants from course metrics
            if "metrics" in course and "completed" in course["metrics"]:
                total_participants += course["metrics"]["completed"]
        
        # Count participants from events
        events = data.get("events", {})
        
        # Count workshops and events
        if "workshops" in events:
            total_workshops_events += len(events["workshops"])
        
        if "talks" in events:
            total_workshops_events += len(events["talks"])
        
        if "notable_meetups" in events:
            total_workshops_events += len(events["notable_meetups"])
        
        # For 2023, count all events as workshops/tutorials
        if year == "2023":
            all_events = data.get("events", [])
            total_workshops_events += len(all_events)
        
        # Count participants from specific events
        if year == "2024":
            # Retreat participants
            if "retreat" in events:
                retreat = events["retreat"]
                if "participants" in retreat and "24" in str(retreat["participants"]):
                    total_participants += 24
        
        # Count participants from 2023 events (extract from participant strings)
        if year == "2023":
            all_events = data.get("events", [])
            for event in all_events:
                if "participants" in event:
                    participants_str = event["participants"]
                    # Extract numbers from strings like "~30", "~15", "~40"
                    import re
                    numbers = re.findall(r'~?(\d+)', participants_str)
                    if numbers:
                        total_participants += int(numbers[0])
    
    return {
        "total_courses": total_courses,
        "total_participants": total_participants,
        "total_research_papers": total_research_papers,
        "total_workshops_events": total_workshops_events,
        "total_university_groups": total_university_groups,
        "total_individual_impacts": total_individual_impacts
    }

def display_2025_content(section="overview"):
    st.markdown('<div class="year-header">2025</div>', unsafe_allow_html=True)
    
    if section == "overview":
        # Show all sections for overview
        display_2025_courses()
        display_2025_university_groups()
        display_2025_events()
        display_2025_individual_impacts()
        display_2025_research()
    elif section == "courses":
        display_2025_courses()
    elif section == "university":
        display_2025_university_groups()
    elif section == "events":
        display_2025_events()
    elif section == "impacts":
        display_2025_individual_impacts()
    elif section == "research":
        display_2025_research()

def display_2025_courses():
    # Courses Section
    st.markdown('<div class="section-header">📚 Courses</div>', unsafe_allow_html=True)
    
    data = load_year_data("2025")
    if not data:
        return
    
    courses = data.get("courses", [])
    
    for course in courses:
        st.markdown(f'<div class="subsection-header">{course["title"]}</div>', unsafe_allow_html=True)
        
        if "details" in course:
            st.markdown(course["details"])
        
        # Display metrics if available
        if "metrics" in course:
            metrics = course["metrics"]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">Participants</div>
                    <div class="metric-value">{metrics.get('accepted', 'N/A')}</div>
                    <div class="metric-description">Accepted</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">Completed</div>
                    <div class="metric-value">{metrics.get('completed', 'N/A')}</div>
                    <div class="metric-description">{metrics.get('completion_rate', 'N/A')} completion rate</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">Rating</div>
                    <div class="metric-value">{metrics.get('rating', 'N/A')}/10</div>
                    <div class="metric-description">Overall average</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Display statistics if available
        if "statistics" in course:
            stats = course["statistics"]
            st.markdown(f"""
            **Key Statistics:**
            - {course["metrics"]["dropout_rate"]} dropout rate (expected for professional courses)
            - {stats.get("professional_participation", "")}
            - Highest rated: {stats.get("highest_rated", "")}
            - Lowest rated: {stats.get("lowest_rated", "")}
            """)
        
        # Display African context topics if available
        if "african_context_topics" in course:
            topics_list = "\n".join([f"- {topic}" for topic in course["african_context_topics"]])
            st.markdown(f"""**Participants mentioned interest in African context topics:**

{topics_list}""")
        
        # Display image with side-by-side layout
        text_content = "### Course Details"
        if "impact" in course:
            text_content += f"\n\n**Impact:** {course['impact']}"
        
        create_side_by_side_layout(
            text_content, 
            course.get("image_description", ""), 
            course.get("image_url")
        )

def display_2025_university_groups():
    # University Groups Section
    st.markdown('<div class="section-header">🏫 University Groups</div>', unsafe_allow_html=True)
    
    data = load_year_data("2025")
    if not data:
        return
    
    university_groups = data.get("university_groups", [])
    
    for group in university_groups:
        st.markdown(f'<div class="subsection-header">{group["name"]}</div>', unsafe_allow_html=True)
        
        # Display organizers if available
        if "organizers" in group:
            organizers_list = "\n".join([f"- {org}" for org in group["organizers"]])
            st.markdown(f"""**Community Organizers:**

{organizers_list}""")
        
        # Display image with side-by-side layout
        text_content = "### Group Information"
        if "first_meetup" in group:
            meetup = group["first_meetup"]
            rating_text = f", rated {meetup['rating']}" if "rating" in meetup else ""
            text_content += f"\n\n**First Meetup:** {meetup['attendees']} attendees{rating_text}"
        
        create_side_by_side_layout(
            text_content, 
            group.get("image_description", ""), 
            group.get("image_url")
        )

def display_2025_events():
    # Events Section
    st.markdown('<div class="section-header">🎯 Events</div>', unsafe_allow_html=True)
    
    data = load_year_data("2025")
    if not data:
        return
    
    events = data.get("events", {})
    
    # Display talks
    if "talks" in events:
        st.markdown('<div class="subsection-header">Talks</div>', unsafe_allow_html=True)
        for talk in events["talks"]:
            st.markdown(f"**{talk['title']}**")
            st.markdown(f"Hosted {talk['speaker']} - {talk['attendees']}")
            create_image_placeholder(talk.get("image_description", ""), "below", talk.get("image_url"))
    
    # Display notable meetups
    if "notable_meetups" in events:
        st.markdown('<div class="subsection-header">Notable Meetups</div>', unsafe_allow_html=True)
        for meetup in events["notable_meetups"]:
            st.markdown(f"**{meetup['title']}**")
            st.markdown(f"{meetup['description']} - {meetup['attendees']}")
            create_image_placeholder(meetup.get("image_description", ""), "below", meetup.get("image_url"))

def display_2025_individual_impacts():
    # Highlighted Individual Impacts
    st.markdown('<div class="section-header">🌟 Highlighted Individual Impacts</div>', unsafe_allow_html=True)
    
    data = load_year_data("2025")
    if not data:
        return
    
    impacts = data.get("individual_impacts", [])
    
    for impact in impacts:
        with st.expander(f"👤 {impact['name']} - {impact['role']}"):
            for achievement in impact['achievements']:
                st.markdown(f"• {achievement}")
            create_image_placeholder(impact.get("image_description", f"Photo of {impact['name']}"), "below", impact.get("image_url"))

def display_2025_research():
    # Research Section
    st.markdown('<div class="section-header">🔬 Research</div>', unsafe_allow_html=True)
    
    data = load_year_data("2025")
    if not data:
        return
    
    research_items = data.get("research", [])
    
    for item in research_items:
        st.markdown(f'<div class="subsection-header">{item["title"]}</div>', unsafe_allow_html=True)
        
        # Display paper information if available
        if "paper_title" in item:
            st.markdown(f"**Paper:** \"{item['paper_title']}\"")
        
        if "authors" in item:
            st.markdown(f"**Authors:** {item['authors']}")
        
        if "venue" in item:
            st.markdown(f"**Venue:** {item['venue']}")
        
        if "status" in item:
            st.markdown(f"**Status:** {item['status']}")
        
        if "url" in item:
            st.markdown(f"**URL:** {item['url']}")
        
        # Display bounties if available
        if "bounties" in item:
            for bounty in item["bounties"]:
                st.markdown(f"• **{bounty}**")
        
        # Display grant information if available
        if "grant_amount" in item:
            st.markdown(f"**Grant:** {item['grant_amount']} awarded in {item.get('awarded', '')}")
        
        if "project" in item:
            st.markdown(f"**Project:** \"{item['project']}\"")
        
        if "team" in item:
            st.markdown(f"**Team:** {item['team']}")
        
        if "partnership" in item:
            st.markdown(f"**Partnership:** {item['partnership']}")

def display_2024_content(section="overview"):
    st.markdown('<div class="year-header">2024</div>', unsafe_allow_html=True)
    
    if section == "overview":
        # Show all sections for overview
        display_2024_coworking()
        display_2024_website()
        display_2024_newsletter()
        display_2024_courses()
        display_2024_events()
    elif section == "coworking":
        display_2024_coworking()
    elif section == "website":
        display_2024_website()
    elif section == "newsletter":
        display_2024_newsletter()
    elif section == "courses":
        display_2024_courses()
    elif section == "events":
        display_2024_events()

def display_2024_coworking():
    # Co-working Space
    st.markdown('<div class="section-header">🏢 Co-working Space</div>', unsafe_allow_html=True)
    
    data = load_year_data("2024")
    if not data:
        return
    
    coworking = data.get("coworking_space", {})
    
    st.markdown(f"""
    Established co-working space at {coworking.get('location', 'Innovation City')} in {coworking.get('established', 'October 2024')}
    - Capacity: {coworking.get('capacity', 'Up to 6 community members')}
    - {coworking.get('regular_bookings', 'Regular Wednesday afternoon bookings (fully booked before reading groups)')}
    - {coworking.get('access', 'Access to media channels for public communication')}
    - {coworking.get('event_spaces', 'Large event spaces for talks, workshops, and reading groups')}
    """)
    create_image_placeholder(coworking.get("image_description", "Innovation City co-working space"), "below", coworking.get("image_url"))

def display_2024_website():
    # Website
    st.markdown('<div class="section-header">🌐 Website</div>', unsafe_allow_html=True)
    
    data = load_year_data("2024")
    if not data:
        return
    
    website = data.get("website", {})
    
    st.markdown(website.get("description", "Built website to house newsletter and enable greater outreach and credibility"))
    st.markdown(f"**Website:** [{website.get('url', 'www.aisafetyct.com')}](http://{website.get('url', 'www.aisafetyct.com')})")
    create_image_placeholder(website.get("image_description", "AISSA website homepage"), "below", website.get("image_url"))

def display_2024_newsletter():
    # Newsletter
    st.markdown('<div class="section-header">📰 Newsletter</div>', unsafe_allow_html=True)
    
    data = load_year_data("2024")
    if not data:
        return
    
    newsletter = data.get("newsletter", {})
    
    st.markdown(f"""
    - Published {newsletter.get('articles_published', 3)} articles at {newsletter.get('timing', 'end of 2024')}
    - Mailing list: {newsletter.get('mailing_list_size', '~60 people')}
    - {newsletter.get('platform', 'Moved to Substack for better metrics and feedback tracking')}
    """)
    create_image_placeholder(newsletter.get("image_description", "Newsletter articles"), "below", newsletter.get("image_url"))

def display_2024_courses():
    # Courses
    st.markdown('<div class="section-header">📚 Courses</div>', unsafe_allow_html=True)
    
    data = load_year_data("2024")
    if not data:
        return
    
    courses = data.get("courses", [])
    
    for course in courses:
        st.markdown(f'<div class="subsection-header">{course["title"]}</div>', unsafe_allow_html=True)
        
        # Display course details
        if "duration" in course:
            st.markdown(f"**Duration:** {course['duration']}")
        
        if "tracks" in course:
            tracks_text = " and ".join(course["tracks"])
            st.markdown(f"**Tracks:** {tracks_text} (based on {course.get('based_on', 'BlueDot AISF Course')})")
        
        # Display applications info
        if "applications" in course:
            apps = course["applications"]
            st.markdown(f"**Applications:** {apps['total']} applicants, {apps['accepted']} accepted")
        
        # Display participants info
        if "participants" in course:
            participants = course["participants"]
            st.markdown(f"""
            - {participants['technical_track']} participants in technical track
            - {participants['governance_track']} participants in governance track
            - {participants['total_cohorts']} cohorts total ({participants['technical_cohorts']} technical, {participants['governance_cohorts']} governance)
            """)
        
        # Display completion metrics
        if "completion" in course:
            completion = course["completion"]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="metric-card"><h4>Technical Track</h4><h2>{completion["technical_completed"]}</h2><p>Completed</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><h4>Governance Track</h4><h2>{completion["governance_completed"]}</h2><p>Completed</p></div>', unsafe_allow_html=True)
        
        # Display charts
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 📊 Course Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            # Demographics pie chart
            demographics_fig = create_demographics_chart()
            st.plotly_chart(demographics_fig, use_container_width=True)
        
        with col2:
            # Course completion chart
            completion_fig = create_course_completion_chart()
            st.plotly_chart(completion_fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display image with side-by-side layout
        text_content = """### Course Impact

The AI Safety Fundamentals course has been instrumental in building AI safety awareness and expertise across South Africa, with participants from diverse backgrounds and experience levels."""
        
        create_side_by_side_layout(
            text_content, 
            course.get("image_description", "AI Safety Fundamentals Course participants"), 
            course.get("image_url")
        )
        
        # Display research projects if available
        if "research_projects" in course:
            st.markdown(f"**Research Projects Presented {course.get('research_projects_presentation', 'June 30th')}:**")
            for project in course["research_projects"]:
                st.markdown(f"• {project}")
        
        # Display feedback if available
        if "feedback" in course:
            st.markdown(f"**Feedback:** {course['feedback']}")

def display_2024_events():
    # Events
    st.markdown('<div class="section-header">🎯 Events</div>', unsafe_allow_html=True)
    
    data = load_year_data("2024")
    if not data:
        return
    
    events = data.get("events", {})
    
    # Display workshops
    if "workshops" in events:
        st.markdown('<div class="subsection-header">Workshops</div>', unsafe_allow_html=True)
        for workshop in events["workshops"]:
            st.markdown(f'<div class="subsection-header">{workshop["title"]}</div>', unsafe_allow_html=True)
            
            if "duration" in workshop:
                st.markdown(f"**Duration:** {workshop['duration']}")
            
            if "type" in workshop:
                st.markdown(f"**Type:** {workshop['type']}")
            
            if "panelists" in workshop:
                panelists_list = "\n".join([f"- {panelist}" for panelist in workshop["panelists"]])
                st.markdown(f"""**Panelists:**

{panelists_list}""")
            
            if "components" in workshop:
                components_list = "\n".join([f"- {component}" for component in workshop["components"]])
                st.markdown(f"""**Components:**

{components_list}""")
            
            if "attendees" in workshop:
                st.markdown(f"**Attendees:** {workshop['attendees']}")
            
            if "participants" in workshop:
                st.markdown(f"**Participants:** {workshop['participants']}")
            
            if "description" in workshop:
                st.markdown(workshop["description"])
            
            if "feedback" in workshop:
                feedback = workshop["feedback"]
                st.markdown(f"**Rating:** {feedback.get('rating', '')} average ({feedback.get('responses', '')} responses)")
                if "notes" in feedback:
                    st.markdown(f"**Notes:** {feedback['notes']}")
            
            if "quote" in workshop:
                st.markdown(f"**Quote:** {workshop['quote']}")
            
            create_image_placeholder(workshop.get("image_description", ""), "below", workshop.get("image_url"))
    
    # Display meetups
    if "meetups" in events:
        meetups = events["meetups"]
        st.markdown('<div class="subsection-header">Meetups</div>', unsafe_allow_html=True)
        st.markdown(meetups.get("description", "Casual meetups with meals and guided discussions"))
        create_image_placeholder(meetups.get("image_description", "AI Safety meetup dinner"), "below", meetups.get("image_url"))
    
    # Display reading groups
    if "reading_groups" in events:
        reading_groups = events["reading_groups"]
        st.markdown('<div class="subsection-header">Reading Groups</div>', unsafe_allow_html=True)
        st.markdown(reading_groups.get("schedule", "Weekly reading groups on Wednesdays"))
        create_image_placeholder(reading_groups.get("image_description", "Reading group session"), "below", reading_groups.get("image_url"))
    
    # Display retreat
    if "retreat" in events:
        retreat = events["retreat"]
        st.markdown('<div class="subsection-header">Retreat</div>', unsafe_allow_html=True)
        st.markdown(f"""
        **Partnership:** {retreat.get('partnership', 'Condor Initiative')}
        
        **Duration:** {retreat.get('duration', '9 days')}
        
        **Participants:** {retreat.get('participants', '24 top South African AI safety talent, ML professors, international AI Safety experts')}
        
        **Outcome:** {retreat.get('outcome', 'Interest in forming AI Safety postdoc positions at UCT AI Institute and Wits MIND Institute')}
        """)
        create_image_placeholder(retreat.get("image_description", "Condor Camp retreat group photo"), "below", retreat.get("image_url"))

def display_2023_content(section="overview"):
    st.markdown('<div class="year-header">2023</div>', unsafe_allow_html=True)
    
    data = load_year_data("2023")
    if not data:
        return
    
    events = data.get("events", [])
    
    if section == "overview":
        # Show all events for overview
        for event in events:
            display_2023_event(event)
    elif section == "sacair":
        # Find and display SACAIR event
        sacair_event = next((e for e in events if "SACAIR" in e["title"]), None)
        if sacair_event:
            display_2023_event(sacair_event)
    elif section == "indabaxs":
        # Find and display IndabaXS event
        indabaxs_event = next((e for e in events if "IndabaXS" in e["title"]), None)
        if indabaxs_event:
            display_2023_event(indabaxs_event)
    elif section == "dl_indabax":
        # Find and display Deep Learning IndabaX event
        dl_event = next((e for e in events if "Deep Learning IndabaX" in e["title"]), None)
        if dl_event:
            display_2023_event(dl_event)

def display_2023_event(event):
    """Display a single 2023 event"""
    st.markdown(f'<div class="section-header">{event["title"]}</div>', unsafe_allow_html=True)
    
    if "duration" in event:
        st.markdown(f"**Duration:** {event['duration']}")
    
    if "content" in event:
        st.markdown(f"**Content:** {event['content']}")
    
    if "format" in event:
        st.markdown(f"**Format:** {event['format']}")
    
    if "presenters" in event:
        presenters_list = " and ".join(event["presenters"])
        st.markdown(f"**Presenters:** {presenters_list}")
    
    if "presentations" in event:
        presentations_list = "\n".join([f"- {pres['title']} ({pres['presenter']})" for pres in event["presentations"]])
        st.markdown(f"""**Presentations:**

{presentations_list}""")
    
    if "participants" in event:
        st.markdown(f"**Participants:** {event['participants']}")
    
    create_image_placeholder(event.get("image_description", ""), "below", event.get("image_url"))

def display_total_impact_banner():
    """Display total impact metrics banner at the top of all pages"""
    metrics = calculate_metrics()
    
    st.markdown("""
    <div class="total-impact-banner">
        <h2>📊 Total Impact Across All Years</h2>
        <div class="metrics-grid">
            <div class="metric-item">
                <div class="metric-number">{}</div>
                <div class="metric-label">Courses</div>
            </div>
            <div class="metric-item">
                <div class="metric-number">{}</div>
                <div class="metric-label">Participants</div>
            </div>
            <div class="metric-item">
                <div class="metric-number">{}</div>
                <div class="metric-label">Research Papers</div>
            </div>
            <div class="metric-item">
                <div class="metric-number">{}</div>
                <div class="metric-label">Workshops & Events</div>
            </div>
            <div class="metric-item">
                <div class="metric-number">{}</div>
                <div class="metric-label">University Groups</div>
            </div>
            <div class="metric-item">
                <div class="metric-number">{}</div>
                <div class="metric-label">Career Changes</div>
            </div>
        </div>
    </div>
    """.format(
        metrics["total_courses"],
        metrics["total_participants"], 
        metrics["total_research_papers"],
        metrics["total_workshops_events"],
        metrics["total_university_groups"],
        metrics["total_individual_impacts"]
    ), unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">🤖 AISSA Track Record</div>', unsafe_allow_html=True)
    st.markdown("### AI Safety South Africa - Our Journey and Impact")
    
    # Display total impact banner
    display_total_impact_banner()
    
    # Add participant growth chart
    st.markdown("### 📈 Participant Growth Over Time")
    growth_fig = create_participant_growth_chart()
    st.plotly_chart(growth_fig, use_container_width=True)
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    
    # Initialize session state
    if "selected_year" not in st.session_state:
        st.session_state.selected_year = "2025"
    if "selected_section" not in st.session_state:
        st.session_state.selected_section = "overview"
    
    # Year selection with expandable sections
    st.sidebar.markdown("### 📅 Years")
    
    # 2025 Section
    with st.sidebar.expander("📅 2025", expanded=(st.session_state.selected_year == "2025")):
        if st.button("📊 Overview", key="2025_overview"):
            st.session_state.selected_year = "2025"
            st.session_state.selected_section = "overview"
        if st.button("📚 Courses", key="2025_courses"):
            st.session_state.selected_year = "2025"
            st.session_state.selected_section = "courses"
        if st.button("🏫 University Groups", key="2025_university"):
            st.session_state.selected_year = "2025"
            st.session_state.selected_section = "university"
        if st.button("🎯 Events", key="2025_events"):
            st.session_state.selected_year = "2025"
            st.session_state.selected_section = "events"
        if st.button("🌟 Individual Impacts", key="2025_impacts"):
            st.session_state.selected_year = "2025"
            st.session_state.selected_section = "impacts"
        if st.button("🔬 Research", key="2025_research"):
            st.session_state.selected_year = "2025"
            st.session_state.selected_section = "research"
    
    # 2024 Section
    with st.sidebar.expander("📅 2024", expanded=(st.session_state.selected_year == "2024")):
        if st.button("📊 Overview", key="2024_overview"):
            st.session_state.selected_year = "2024"
            st.session_state.selected_section = "overview"
        if st.button("🏢 Co-working Space", key="2024_coworking"):
            st.session_state.selected_year = "2024"
            st.session_state.selected_section = "coworking"
        if st.button("🌐 Website", key="2024_website"):
            st.session_state.selected_year = "2024"
            st.session_state.selected_section = "website"
        if st.button("📰 Newsletter", key="2024_newsletter"):
            st.session_state.selected_year = "2024"
            st.session_state.selected_section = "newsletter"
        if st.button("📚 Courses", key="2024_courses"):
            st.session_state.selected_year = "2024"
            st.session_state.selected_section = "courses"
        if st.button("🎯 Events", key="2024_events"):
            st.session_state.selected_year = "2024"
            st.session_state.selected_section = "events"
    
    # 2023 Section
    with st.sidebar.expander("📅 2023", expanded=(st.session_state.selected_year == "2023")):
        if st.button("📊 Overview", key="2023_overview"):
            st.session_state.selected_year = "2023"
            st.session_state.selected_section = "overview"
        if st.button("🎓 SACAIR Tutorial", key="2023_sacair"):
            st.session_state.selected_year = "2023"
            st.session_state.selected_section = "sacair"
        if st.button("🎯 IndabaXS", key="2023_indabaxs"):
            st.session_state.selected_year = "2023"
            st.session_state.selected_section = "indabaxs"
        if st.button("🎓 Deep Learning IndabaX", key="2023_dl_indabax"):
            st.session_state.selected_year = "2023"
            st.session_state.selected_section = "dl_indabax"
    
    selected_year = st.session_state.selected_year
    selected_section = st.session_state.selected_section
    
    # Display content based on selection
    if selected_year == "2025":
        display_2025_content(selected_section)
    elif selected_year == "2024":
        display_2024_content(selected_section)
    elif selected_year == "2023":
        display_2023_content(selected_section)
    
    # Force rerun when year or section is selected
    if (st.session_state.get("selected_year") != selected_year or 
        st.session_state.get("selected_section") != selected_section):
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>AI Safety South Africa - Building a safer future through AI safety research and education</p>
        <p>Website: <a href='http://www.aisafetysa.com' target='_blank'>www.aisafetysa.com</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
