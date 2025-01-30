from typing import Dict, Any

class DutchTranslator:
    """Handle Dutch translations for the report"""
    
    def __init__(self):
        self.translations = {
            # General Report
            'seo_analysis_report': 'SEO Analyse Rapport',
            'moz_metrics': 'Moz Statistieken',
            'scraped_data': 'Opgehaalde Gegevens',
            'generated_by_seo_tool': 'Gegenereerd door SEO Analyse Tool',

            # SEO Metrics
            'domain_authority': 'Domein Autoriteit',
            'page_authority': 'Pagina Autoriteit',
            'backlinks': 'Backlinks',
            'total_links': 'Totale Links',
            'linking_domains': 'Verwijzende Domeinen',
            'spam_score': 'Spam Score',
            'last_crawled': 'Laatst Gecrawld',

            # Technical SEO
            'technical_seo': 'Technische SEO',
            'meta_tags': 'Meta Tags',
            'missing_meta': 'Ontbrekende Meta Tags',
            'image_optimization': 'Afbeeldingsoptimalisatie',
            'headings': 'Koppen',
            'links': 'Links',
            'content_quality': 'Content Kwaliteit',
            'word_count': 'Aantal Woorden',
            'paragraphs': 'Paragrafen',
            'has_structured_data': 'Bevat Gestructureerde Gegevens',

            # Search Console Metrics
            'clicks': 'Clicks',
            'impressions': 'Impressies',
            'ctr': 'Click Through Rate',
            'position': 'Gemiddelde Positie',

            # Priority Levels
            'high': 'Hoog',
            'medium': 'Gemiddeld',
            'low': 'Laag',

            # Time and Cost
            'estimated_time': 'Geschatte Tijd',
            'estimated_cost': 'Geschatte Kosten',
            'hours': 'Uren',

            # Common Terms
            'overview': 'Overzicht',
            'issues': 'Problemen',
            'recommendations': 'Aanbevelingen',
            'total': 'Totaal',
            'status': 'Status',
            'priority': 'Prioriteit',
            'action_required': 'Actie Vereist'
        }

    def translate(self, key: str) -> str:
        """Get Dutch translation for a key"""
        return self.translations.get(key, key)

    def translate_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Translate dictionary keys to Dutch"""
        return {
            self.translate(k): v 
            for k, v in data.items()
        }
