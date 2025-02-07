import streamlit as st
from typing import Dict, Any, List

class ReportDisplay:
    """Component for displaying SEO reports"""
    
    @staticmethod
    def show_overview_metrics(data: Dict[str, Any]):
        st.subheader("SEO-Metrics & Overzicht")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Domein Autoriteit",
                value=data.get('domain_authority', 0)
            )
        
        with col2:
            st.metric(
                label="Page Autoriteit",
                value=data.get('page_authority', 0)
            )
            
        with col3:
            st.metric(
                label="Aantal Backlinks",
                value=data.get('backlinks', 0)
            )
    
    @staticmethod
    def show_technical_analysis(data: Dict[str, Any], enhanced_insights: List[Dict[str, Any]] = None):
        """Display technical SEO analysis with enhanced insights"""
        # Meta Tags Section
        st.subheader("Meta Tags")
        meta_data = data.get('meta_tags', {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Title Length", len(meta_data.get('title', '')) if meta_data.get('title') else 0)
        with col2:
            st.metric("Description Length", len(meta_data.get('meta_description', '')) if meta_data.get('meta_description') else 0)
        
        # Headings Structure
        st.subheader("Heading Structure")
        headings_data = data.get('headings', {})
        heading_cols = st.columns(6)
        for i, col in enumerate(heading_cols, 1):
            with col:
                st.metric(f"H{i}", headings_data.get(f'h{i}', 0))
        
        # Technical Elements
        st.subheader("Technical Elements")
        tech_data = data.get('technical', {})
        tech_cols = st.columns(3)
        with tech_cols[0]:
            st.metric("Canonical", "✓" if tech_data.get('has_canonical') else "✗")
        with tech_cols[1]:
            st.metric("Viewport", "✓" if tech_data.get('has_viewport') else "✗")
        with tech_cols[2]:
            st.metric("Favicon", "✓" if tech_data.get('has_favicon') else "✗")

        # Enhanced AI Insights
        if enhanced_insights:
            st.markdown("### AI-Enhanced Technical Insights")
            for insight in enhanced_insights:
                with st.expander(insight.get('title', '')):
                    st.write(insight.get('description', ''))
                    
                    cols = st.columns(4)
                    with cols[0]:
                        st.metric("Priority", insight.get('metadata', {}).get('priority', ''))
                    with cols[1]:
                        st.metric("Impact", f"{float(insight.get('metadata', {}).get('impact', 0))*100:.0f}%")
                    with cols[2]:
                        st.metric("Time", insight.get('metadata', {}).get('implementation_time', ''))
                    with cols[3]:
                        st.metric("Cost", insight.get('metadata', {}).get('estimated_cost', ''))
                    
                    if insight.get('implementation_steps'):
                        st.markdown("#### Implementation Steps")
                        for step in insight['implementation_steps']:
                            st.markdown(f"- {step}")
    
    @staticmethod
    def show_content_analysis(data: Dict[str, Any], enhanced_insights: List[Dict] = None):
        """Display content analysis with optional enhanced insights"""
        # Display basic content analysis
        st.subheader("Content Analysis")
        
        content_data = data.get('content', {})
        
        # Basic metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Word Count", content_data.get('word_count', 0))
        with col2:
            st.metric("Paragraphs", content_data.get('paragraphs', 0))
        
        # Enhanced insights if available
        if enhanced_insights:
            st.subheader("Enhanced Content Insights")
            for insight in enhanced_insights:
                with st.expander(insight.get('title', 'Content Insight')):
                    st.write(insight.get('description', ''))
                    cols = st.columns(3)
                    with cols[0]:
                        st.metric("Priority", insight.get('priority', 'Medium'))
                    with cols[1]:
                        st.metric("Impact", f"{insight.get('impact', 0)*100:.0f}%")
                    with cols[2]:
                        st.metric("Confidence", f"{insight.get('confidence', 0)*100:.0f}%")
    @staticmethod
    def show_backlink_analysis(data: Dict[str, Any]):
        with st.expander("Backlink Analyse", expanded=True):
            st.markdown("### Backlink Profiel")
            
            # Backlink metrics
            if 'backlinks' in data:
                st.table(data['backlinks'])

    @staticmethod
    def show_recommendations(recommendations: List[Dict[str, Any]]):
        with st.expander("SEO Aanbevelingen & Kosten", expanded=True):
            for rec in recommendations:
                st.markdown(f"""
                **{rec['task']}**
                - Prioriteit: {rec['priority']}
                - Tijd: {rec['time']}
                - Kosten: {rec['cost']}
                """)