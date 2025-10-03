import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import json
import os

# Page configuration
st.set_page_config(
    page_title="AISSA Track Record",
    page_icon="images/favicon.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external CSS
with open("styles.css", "r") as f:
    css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

def create_image_placeholder(description):
    """Create a placeholder for images that will be added later"""
    return st.markdown(f"""
    <div class="image-placeholder">
        📸 Image Placeholder: {description}
    </div>
    """, unsafe_allow_html=True)

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
    """Calculate metrics programmatically from the JSON data"""
    
    # Load data for all years
    data_2025 = load_year_data("2025")
    data_2024 = load_year_data("2024")
    data_2023 = load_year_data("2023")
    
    if not all([data_2025, data_2024, data_2023]):
        return {
            "total_courses": 0,
            "total_participants": 0,
            "total_research_papers": 0,
            "total_workshops_events": 0,
            "total_university_groups": 0,
            "total_individual_impacts": 0
        }
    
    # 2025 data
    courses_2025 = len(data_2025.get("courses", []))
    university_groups_2025 = len(data_2025.get("university_groups", []))
    research_papers_2025 = len(data_2025.get("research", []))
    individual_impacts_2025 = len(data_2025.get("individual_impacts", []))
    
    # 2024 data
    courses_2024 = len(data_2024.get("courses", []))
    course_participants_2024 = data_2024.get("courses", [{}])[0].get("completion", {}).get("total_completed", 0)
    workshops_2024 = len(data_2024.get("events", {}).get("workshops", []))
    research_projects_2024 = len(data_2024.get("courses", [{}])[0].get("research_projects", []))
    retreat_participants_2024 = 24  # Condor Camp
    
    # 2023 data
    tutorials_2023 = len(data_2023.get("events", []))
    total_participants_2023 = 85  # ~30 + ~15 + ~40
    
    # Calculate totals
    total_courses = courses_2025 + courses_2024
    total_participants = 60 + course_participants_2024 + total_participants_2023  # 60 from 2025 courses
    total_research_papers = research_papers_2025
    total_workshops_events = workshops_2024 + tutorials_2023 + 2  # +2 for 2025 events
    total_university_groups = university_groups_2025
    total_individual_impacts = individual_impacts_2025
    
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
                st.markdown(f'<div class="metric-card"><h4>Participants</h4><h2>{metrics.get("accepted", "")}</h2><p>Accepted</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><h4>Completed</h4><h2>{metrics.get("completed", "")}</h2><p>{metrics.get("completion_rate", "")} completion rate</p></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-card"><h4>Rating</h4><h2>{metrics.get("rating", "")}/10</h2><p>Overall average</p></div>', unsafe_allow_html=True)
        
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
            topics_list = [f"- {topic}" for topic in course["african_context_topics"]]
            st.markdown(f"""
            **Participants mentioned interest in African context topics:**\n
            {topics_list}
            """)
        
        # Display impact if available
        if "impact" in course:
            st.markdown(f"**Impact:** {course['impact']}")
        
        # Display image placeholder
        create_image_placeholder(course.get("image_description", ""))

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
            st.markdown(f"""
            **Community Organizers:**
            {organizers_list}
            """)
        
        # Display first meetup info if available
        if "first_meetup" in group:
            meetup = group["first_meetup"]
            rating_text = f", rated {meetup['rating']}" if "rating" in meetup else ""
            st.markdown(f"**First Meetup:** {meetup['attendees']} attendees{rating_text}")
        
        # Display image placeholder
        create_image_placeholder(group.get("image_description", ""))

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
            create_image_placeholder(talk.get("image_description", ""))
    
    # Display notable meetups
    if "notable_meetups" in events:
        st.markdown('<div class="subsection-header">Notable Meetups</div>', unsafe_allow_html=True)
        for meetup in events["notable_meetups"]:
            st.markdown(f"**{meetup['title']}**")
            st.markdown(f"{meetup['description']} - {meetup['attendees']}")
            create_image_placeholder(meetup.get("image_description", ""))

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
            create_image_placeholder(impact.get("image_description", f"Photo of {impact['name']}"))

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
        
        # Display image placeholder
        create_image_placeholder(item.get("image_description", ""))

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
    create_image_placeholder(coworking.get("image_description", "Innovation City co-working space"))

def display_2024_website():
    # Website
    st.markdown('<div class="section-header">🌐 Website</div>', unsafe_allow_html=True)
    
    data = load_year_data("2024")
    if not data:
        return
    
    website = data.get("website", {})
    
    st.markdown(website.get("description", "Built website to house newsletter and enable greater outreach and credibility"))
    st.markdown(f"**Website:** [{website.get('url', 'www.aisafetyct.com')}](http://{website.get('url', 'www.aisafetyct.com')})")
    create_image_placeholder(website.get("image_description", "AISSA website homepage"))

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
    create_image_placeholder(newsletter.get("image_description", "Newsletter articles"))

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
        
        # Display image placeholder
        create_image_placeholder(course.get("image_description", "AI Safety Fundamentals Course participants"))
        
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
                st.markdown(f"""
                **Panelists:**
                {panelists_list}
                """)
            
            if "components" in workshop:
                components_list = "\n".join([f"- {component}" for component in workshop["components"]])
                st.markdown(f"""
                **Components:**
                {components_list}
                """)
            
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
            
            create_image_placeholder(workshop.get("image_description", ""))
    
    # Display meetups
    if "meetups" in events:
        meetups = events["meetups"]
        st.markdown('<div class="subsection-header">Meetups</div>', unsafe_allow_html=True)
        st.markdown(meetups.get("description", "Casual meetups with meals and guided discussions"))
        create_image_placeholder(meetups.get("image_description", "AI Safety meetup dinner"))
    
    # Display reading groups
    if "reading_groups" in events:
        reading_groups = events["reading_groups"]
        st.markdown('<div class="subsection-header">Reading Groups</div>', unsafe_allow_html=True)
        st.markdown(reading_groups.get("schedule", "Weekly reading groups on Wednesdays"))
        create_image_placeholder(reading_groups.get("image_description", "Reading group session"))
    
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
        create_image_placeholder(retreat.get("image_description", "Condor Camp retreat group photo"))

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
        st.markdown(f"""
        **Presentations:**
        {presentations_list}
        """)
    
    if "participants" in event:
        st.markdown(f"**Participants:** {event['participants']}")
    
    create_image_placeholder(event.get("image_description", ""))

def main():
    # Header
    st.markdown('<div class="main-header">🤖 AISSA Track Record</div>', unsafe_allow_html=True)
    st.markdown("### AI Safety South Africa - Our Journey and Impact")
    
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
    
    # Quick stats in sidebar - calculated programmatically
    st.sidebar.markdown("### 📊 Total Impact")
    
    metrics = calculate_metrics()
    
    st.sidebar.metric("Total Courses", metrics["total_courses"])
    st.sidebar.metric("Total Participants", metrics["total_participants"])
    st.sidebar.metric("Research Papers", metrics["total_research_papers"])
    st.sidebar.metric("Workshops & Events", metrics["total_workshops_events"])
    st.sidebar.metric("University Groups", metrics["total_university_groups"])
    st.sidebar.metric("Individual Career Changes", metrics["total_individual_impacts"])
    
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
