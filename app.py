import streamlit as st
import pandas as pd
import json
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import pyttsx3
import os


# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="Disaster Monitoring System", layout="wide")

st.markdown("""
<style>
/* Make entire app use full height */
html, body, [data-testid="stAppViewContainer"] {
    height: 100%;
}

/* Main app container */
[data-testid="stApp"] {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* Main content area */
.main-content {
    flex: 1;
}

/* Footer */
.app-footer {
    text-align: center;
    font-size: 13px;
    color: #777;
    padding: 8px 0 12px 0;
    border-top: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)


# ======================================================
# LANGUAGE DEFINITIONS
# ======================================================
LANG = {
    "English": {
        "title": "Disaster Monitoring & Decision Support System",
        "filters": "Filters",
        "year": "Select Year",
        "type": "Disaster Type",
        "table": "Filtered Disaster Records",
        "map": "India Disaster Map (Historical GeoJSON)",
        "summary": "Disaster Summary Report",
        "assistant": "Disaster Assistant",
        "ask": "Ask a question",
        "legend": "Map Legend",
        "major": "Major Disaster",
        "minor": "Minor Disaster",
        "no_data": "No data available for selected filters",
        "analytics": "Advanced Disaster Analytics",
        "theme_note": "Theme can be changed from ☰ → Settings → Theme",
        "risk_dist": "Risk Level Distribution",
    "disaster_freq": "Disaster Type Frequency",
    "year_trend": "Year-wise Disaster Trend",
    "top_states": "Top Affected States",
    "count": "Count",
    "events": "Events" ,
    "key_metrics": "Key Disaster Metrics",
"total_deaths": "Total Deaths",
"total_affected": "Total Affected",
"avg_risk": "Average Risk Score",
"risk_level": "Dominant Risk Level",
"data_source": "Data Source: EM-DAT International Disaster Database. Administrative areas are represented at varying levels as provided by the source.",

"summary_report": "Disaster Summary Report",
"year_label": "Year",
"Disaster_Type": "Disaster Type",
"total_events": "Total Events",
"total_affected_population": "Total Affected Population",
"read_summary": "Read Summary"
  },

    "Tamil": {
        "title": "பேரிடர் கண்காணிப்பு மற்றும் முடிவு ஆதரவு அமைப்பு",
        "filters": "வடிகட்டிகள்",
        "year": "வருடம் தேர்வு",
        "type": "பேரிடர் வகை",
        "table": "வடிகட்டப்பட்ட பேரிடர் பதிவுகள்",
        "map": "இந்தியா பேரிடர் வரைபடம்",
        "summary": "பேரிடர் சுருக்க அறிக்கை",
        "assistant": "பேரிடர் உதவியாளர்",
        "ask": "கேள்வி கேளுங்கள்",
        "legend": "வரைபட விளக்கம்",
        "major": "முக்கிய பேரிடர்",
        "minor": "சிறிய பேரிடர்",
        "no_data": "தரவு கிடைக்கவில்லை",
        "analytics": "மேம்பட்ட பேரிடர் பகுப்பாய்வு",
        "theme_note": "☰ → Settings → Theme மூலம் தீம் மாற்றலாம்",
        "risk_dist": "அபாய நிலை பகிர்வு",
"disaster_freq": "பேரிடர் வகை அடர்த்தி",
"year_trend": "வருட வாரியான பேரிடர் போக்கு",
"top_states": "அதிகம் பாதிக்கப்பட்ட மாநிலங்கள்",
"count": "எண்ணிக்கை",
"events": "நிகழ்வுகள்",
"key_metrics": "முக்கிய பேரிடர் அளவீடுகள்",
"total_deaths": "மொத்த உயிரிழப்புகள்",
"total_affected": "மொத்த பாதிக்கப்பட்டோர்",
"avg_risk": "சராசரி ஆபத்து மதிப்பெண்",
"risk_level": "முக்கிய ஆபத்து நிலை",
"data_source": "தரவு மூலம்: EM-DAT சர்வதேச பேரிடர் தரவுத்தளம். நிர்வாக பகுதிகள் மூலத்தின் அடிப்படையில் மாறுபடும்.",

"summary_report": "பேரிடர் சுருக்க அறிக்கை",
"year_label": "வருடம்",
"disaster_type_label": "பேரிடர் வகை",
"total_events": "மொத்த நிகழ்வுகள்",
"total_affected_population": "மொத்த பாதிக்கப்பட்ட மக்கள்",
"read_summary": "சுருக்கத்தை வாசிக்க"


    },

    "Hindi": {
        "title": "आपदा निगरानी और निर्णय सहायता प्रणाली",
        "filters": "फ़िल्टर",
        "year": "वर्ष चुनें",
        "type": "आपदा प्रकार",
        "table": "फ़िल्टर किया गया आपदा डेटा",
        "map": "भारत आपदा मानचित्र",
        "summary": "आपदा सारांश रिपोर्ट",
        "assistant": "आपदा सहायक",
        "ask": "प्रश्न पूछें",
        "legend": "मानचित्र संकेत",
        "major": "प्रमुख आपदा",
        "minor": "छोटी आपदा",
        "no_data": "कोई डेटा उपलब्ध नहीं",
        "analytics": "उन्नत आपदा विश्लेषण",
        "theme_note": "☰ → Settings → Theme से थीम बदलें",
        "risk_dist": "जोखिम स्तर वितरण",
"disaster_freq": "आपदा प्रकार आवृत्ति",
"year_trend": "वर्षवार आपदा प्रवृत्ति",
"top_states": "सबसे अधिक प्रभावित राज्य",
"count": "संख्या",
"events": "घटनाएँ",
"key_metrics": "प्रमुख आपदा मीट्रिक",
"total_deaths": "कुल मौतें",
"total_affected": "कुल प्रभावित",
"avg_risk": "औसत जोखिम स्कोर",
"risk_level": "प्रमुख जोखिम स्तर",
"data_source": "डेटा स्रोत: EM-DAT अंतर्राष्ट्रीय आपदा डेटाबेस। प्रशासनिक क्षेत्र स्रोत के अनुसार भिन्न होते हैं।",
"summary_report": "आपदा सारांश रिपोर्ट",
"year_label": "वर्ष",
"disaster_type_label": "आपदा प्रकार",
"total_events": "कुल घटनाएँ",
"total_affected_population": "कुल प्रभावित जनसंख्या",
"read_summary": "सारांश पढ़ें"

    },

    "Telugu": {
        "title": "విపత్తు పర్యవేక్షణ మరియు నిర్ణయ సహాయ వ్యవస్థ",
        "filters": "ఫిల్టర్లు",
        "year": "సంవత్సరం",
        "type": "విపత్తు రకం",
        "table": "వడపోత చేసిన విపత్తు డేటా",
        "map": "భారత విపత్తు పటం",
        "summary": "విపత్తు సారాంశ నివేదిక",
        "assistant": "విపత్తు సహాయకుడు",
        "ask": "ప్రశ్న అడగండి",
        "legend": "పటం వివరణ",
        "major": "ముఖ్య విపత్తు",
        "minor": "చిన్న విపత్తు",
        "no_data": "డేటా లేదు",
        "analytics": "అధునాతన విపత్తు విశ్లేషణ",
        "theme_note": "☰ → Settings → Theme ద్వారా థీమ్ మార్చండి",
        "risk_dist": "ప్రమాద స్థాయి పంపిణీ",
"disaster_freq": "విపత్తు రకం అవృత్తి",
"year_trend": "సంవత్సరాల వారీ విపత్తుల ధోరణి",
"top_states": "అత్యధికంగా ప్రభావిత రాష్ట్రాలు",
"count": "సంఖ్య",
"events": "సంఘటనలు",
"key_metrics": "ముఖ్య విపత్తు సూచికలు",
"total_deaths": "మొత్తం మరణాలు",
"total_affected": "మొత్తం ప్రభావితులు",
"avg_risk": "సగటు ప్రమాద స్కోర్",
"risk_level": "ప్రధాన ప్రమాద స్థాయి",
"data_source": "డేటా మూలం: EM-DAT అంతర్జాతీయ విపత్తు డేటాబేస్. పరిపాలనా ప్రాంతాలు మూలం ఆధారంగా మారుతాయి.",

"summary_report": "విపత్తు సారాంశ నివేదిక",
"year_label": "సంవత్సరం",
"disaster_type_label": "విపత్తు రకం",
"total_events": "మొత్తం సంఘటనలు",
"total_affected_population": "మొత్తం ప్రభావిత జనాభా",
"read_summary": "సారాంశం వినండి"

    },

    "Malayalam": {
        "title": "ദുരന്ത നിരീക്ഷണവും തീരുമാന സഹായ സംവിധാനവും",
        "filters": "ഫിൽട്ടറുകൾ",
        "year": "വർഷം",
        "type": "ദുരന്ത തരം",
        "table": "ഫിൽട്ടർ ചെയ്ത ദുരന്ത ഡാറ്റ",
        "map": "ഇന്ത്യ ദുരന്ത ഭൂപടം",
        "summary": "ദുരന്ത സംഗ്രഹ റിപ്പോർട്ട്",
        "assistant": "ദുരന്ത സഹായി",
        "ask": "ചോദ്യം ചോദിക്കുക",
        "legend": "ഭൂപട വിശദീകരണം",
        "major": "പ്രധാന ദുരന്തം",
        "minor": "ചെറിയ ദുരന്തം",
        "no_data": "ഡാറ്റ ലഭ്യമല്ല",
        "analytics": "ഉന്നത ദുരന്ത വിശകലനം",
        "theme_note": "☰ → Settings → Theme വഴി തീം മാറ്റാം",
        "risk_dist": "അപകട നില വിതരണങ്ങൾ",
"disaster_freq": "ദുരന്ത തരം ആവർത്തനം",
"year_trend": "വർഷാനുസൃത ദുരന്ത പ്രവണത",
"top_states": "ഏറ്റവും ബാധിച്ച സംസ്ഥാനങ്ങൾ",
"count": "എണ്ണം",
"events": "സംഭവങ്ങൾ",
"key_metrics": "പ്രധാന ദുരന്ത സൂചികകൾ",
"total_deaths": "ആകെ മരണങ്ങൾ",
"total_affected": "ആകെ ബാധിതർ",
"avg_risk": "ശരാശരി അപകട സ്‌കോർ",
"risk_level": "പ്രധാന അപകട നില",
"data_source": "ഡാറ്റ ഉറവിടം: EM-DAT അന്താരാഷ്ട്ര ദുരന്ത ഡാറ്റാബേസ്. ഭരണ മേഖലകൾ ഉറവിടത്തിന് അനുസരിച്ച് വ്യത്യാസപ്പെടാം.",

"summary_report": "ദുരന്ത സംഗ്രഹ റിപ്പോർട്ട്",
"year_label": "വർഷം",
"disaster_type_label": "ദുരന്ത തരം",
"total_events": "ആകെ സംഭവങ്ങൾ",
"total_affected_population": "ആകെ ബാധിത ജനസംഖ്യ",
"read_summary": "സംഗ്രഹം വായിക്കുക"


    },

    "French": {
        "title": "Système de surveillance et d’aide à la décision en cas de catastrophe",
        "filters": "Filtres",
        "year": "Sélectionner l’année",
        "type": "Type de catastrophe",
        "table": "Dossiers de catastrophes filtrés",
        "map": "Carte des catastrophes en Inde",
        "summary": "Rapport de synthèse des catastrophes",
        "assistant": "Assistant catastrophe",
        "ask": "Poser une question",
        "legend": "Légende de la carte",
        "major": "Catastrophe majeure",
        "minor": "Catastrophe mineure",
        "no_data": "Aucune donnée disponible",
        "analytics": "Analyse avancée des catastrophes",
        "theme_note": "☰ → Paramètres → Thème",
        "risk_dist": "Répartition des niveaux de risque",
"disaster_freq": "Fréquence des types de catastrophes",
"year_trend": "Tendance annuelle des catastrophes",
"top_states": "États les plus touchés",
"count": "Nombre",
"events": "Événements",
"key_metrics": "Indicateurs clés des catastrophes",
"total_deaths": "Décès totaux",
"total_affected": "Total des personnes affectées",
"avg_risk": "Score de risque moyen",
"risk_level": "Niveau de risque dominant",
"data_source": "Source des données : Base de données internationale EM-DAT. Les zones administratives varient selon la source.",

"summary_report": "Rapport de synthèse des catastrophes",
"year_label": "Année",
"disaster_type_label": "Type de catastrophe",
"total_events": "Nombre total d'événements",
"total_affected_population": "Population totale affectée",
"read_summary": "Lire le résumé"


    },

    "Kannada": {
        "title": "ವಿಪತ್ತು ಮೇಲ್ವಿಚಾರಣೆ ಮತ್ತು ನಿರ್ಣಯ ಬೆಂಬಲ ವ್ಯವಸ್ಥೆ",
        "filters": "ಫಿಲ್ಟರ್‌ಗಳು",
        "year": "ವರ್ಷ ಆಯ್ಕೆ",
        "type": "ವಿಪತ್ತು ಪ್ರಕಾರ",
        "table": "ಫಿಲ್ಟರ್ ಮಾಡಿದ ವಿಪತ್ತು ದಾಖಲೆಗಳು",
        "map": "ಭಾರತ ವಿಪತ್ತು ನಕ್ಷೆ",
        "summary": "ವಿಪತ್ತು ಸಾರಾಂಶ ವರದಿ",
        "assistant": "ವಿಪತ್ತು ಸಹಾಯಕ",
        "ask": "ಪ್ರಶ್ನೆ ಕೇಳಿ",
        "legend": "ನಕ್ಷೆ ವಿವರಣೆ",
        "major": "ಪ್ರಮುಖ ವಿಪತ್ತು",
        "minor": "ಸಣ್ಣ ವಿಪತ್ತು",
        "no_data": "ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ",
        "analytics": "ಮುನ್ನಡೆದ ವಿಪತ್ತು ವಿಶ್ಲೇಷಣೆ",
        "theme_note": "☰ → Settings → Theme ಮೂಲಕ ಥೀಮ್ ಬದಲಾಯಿಸಿ",
        "risk_dist": "ಅಪಾಯ ಮಟ್ಟ ವಿತರಣೆ",
"disaster_freq": "ವಿಪತ್ತು ಪ್ರಕಾರ ಅವೃತ್ತಿ",
"year_trend": "ವರ್ಷಾನುಸಾರ ವಿಪತ್ತು ಪ್ರವೃತ್ತಿ",
"top_states": "ಅತ್ಯಧಿಕವಾಗಿ பாதಿತ ರಾಜ್ಯಗಳು",
"count": "ಎಣಿಕೆ",
"events": "ಘಟನೆಗಳು",
"key_metrics": "ಮುಖ್ಯ ವಿಪತ್ತು ಮಾಪಕಗಳು",
"total_deaths": "ಒಟ್ಟು ಸಾವುಗಳು",
"total_affected": "ಒಟ್ಟು ಪರಿಣಾಮಿತರು",
"avg_risk": "ಸರಾಸರಿ ಅಪಾಯ ಅಂಕ",
"risk_level": "ಪ್ರಮುಖ ಅಪಾಯ ಮಟ್ಟ",
"data_source": "ಡೇಟಾ ಮೂಲ: EM-DAT ಅಂತರರಾಷ್ಟ್ರೀಯ ವಿಪತ್ತು ಡೇಟಾಬೇಸ್. ಆಡಳಿತಾತ್ಮಕ ಪ್ರದೇಶಗಳು ಮೂಲದ ಪ್ರಕಾರ ಬದಲಾಗುತ್ತವೆ.",

"summary_report": "ವಿಪತ್ತು ಸಾರಾಂಶ ವರದಿ",
"year_label": "ವರ್ಷ",
"disaster_type_label": "ವಿಪತ್ತು ಪ್ರಕಾರ",
"total_events": "ಒಟ್ಟು ಘಟನೆಗಳು",
"total_affected_population": "ಒಟ್ಟು ಪರಿಣಾಮಿತ ಜನಸಂಖ್ಯೆ",
"read_summary": "ಸಾರಾಂಶ ಓದಿ"


    },

    "Spanish": {
        "title": "Sistema de monitoreo y apoyo a la toma de decisiones ante desastres",
        "filters": "Filtros",
        "year": "Seleccionar año",
        "type": "Tipo de desastre",
        "table": "Registros de desastres filtrados",
        "map": "Mapa de desastres de la India",
        "summary": "Informe resumido de desastres",
        "assistant": "Asistente de desastres",
        "ask": "Hacer una pregunta",
        "legend": "Leyenda del mapa",
        "major": "Desastre mayor",
        "minor": "Desastre menor",
        "no_data": "No hay datos disponibles",
        "analytics": "Análisis avanzado de desastres",
        "theme_note": "☰ → Configuración → Tema",
        "risk_dist": "Distribución del nivel de riesgo",
"disaster_freq": "Frecuencia del tipo de desastre",
"year_trend": "Tendencia anual de desastres",
"top_states": "Estados más afectados",
"count": "Cantidad",
"events": "Eventos",
"key_metrics": "Métricas clave de desastres",
"total_deaths": "Muertes totales", 
"total_affected": "Total afectado",
"avg_risk": "Puntuación de riesgo promedio",
"risk_level": "Nivel de riesgo dominante",
"data_source": "Fuente de datos: Base de datos internacional de desastres EM-DAT. Las áreas administrativas varían según la fuente.",
"summary_report": "Informe resumido de desastres",
"year_label": "Año",
"disaster_type_label": "Tipo de desastre",
"total_events": "Total de eventos",
"total_affected_population": "Población total afectada",
"read_summary": "Leer resumen"
    },

    "German": {
        "title": "System zur Katastrophenüberwachung und Entscheidungsunterstützung",
        "filters": "Filter",
        "year": "Jahr auswählen",
        "type": "Katastrophentyp",
        "table": "Gefilterte Katastrophendaten",
        "map": "Katastrophenkarte von Indien",
        "summary": "Katastrophen-Zusammenfassung",
        "assistant": "Katastrophenassistent",
        "ask": "Eine Frage stellen",
        "legend": "Kartenlegende",
        "major": "Großkatastrophe",
        "minor": "Kleine Katastrophe",
        "no_data": "Keine Daten verfügbar",
        "analytics": "Erweiterte Katastrophenanalyse",
        "theme_note": "☰ → Einstellungen → Design",
        "risk_dist": "Risikostufenverteilung",
"disaster_freq": "Häufigkeit der Katastrophentypen",
"year_trend": "Jährlicher Katastrophentrend",
"top_states": "Am stärksten betroffene Bundesstaaten",
"count": "Anzahl",
"events": "Ereignisse",
"key_metrics": "Zentrale Katastrophenkennzahlen",
"total_deaths": "Gesamtzahl der Todesfälle",
"total_affected": "Gesamtzahl der Betroffenen",
"avg_risk": "Durchschnittlicher Risikowert",
"risk_level": "Dominantes Risikoniveau",
"data_source": "Datenquelle: EM-DAT Internationale Katastrophendatenbank. Verwaltungsgrenzen variieren je nach Quelle.",

"summary_report": "Katastrophenübersicht",
"year_label": "Jahr",
"disaster_type_label": "Katastrophentyp",
"total_events": "Gesamtanzahl der Ereignisse",
"total_affected_population": "Gesamt betroffene Bevölkerung",
"read_summary": "Zusammenfassung lesen"


    },

    "Arabic": {
        "title": "نظام مراقبة الكوارث ودعم اتخاذ القرار",
        "filters": "عوامل التصفية",
        "year": "اختر السنة",
        "type": "نوع الكارثة",
        "table": "سجلات الكوارث المصفاة",
        "map": "خريطة الكوارث في الهند",
        "summary": "تقرير ملخص الكوارث",
        "assistant": "مساعد الكوارث",
        "ask": "اطرح سؤالاً",
        "legend": "مفتاح الخريطة",
        "major": "كارثة كبرى",
        "minor": "كارثة صغرى",
        "no_data": "لا توجد بيانات",
        "analytics": "تحليل متقدم للكوارث",
        "theme_note": "☰ → الإعدادات → المظهر",
        "risk_dist": "توزيع مستوى المخاطر",
"disaster_freq": "تكرار نوع الكوارث",
"year_trend": "الاتجاه السنوي للكوارث",
"top_states": "الولايات الأكثر تضرراً",
"count": "العدد",
"events": "الأحداث",
"key_metrics": "المؤشرات الرئيسية للكوارث",
"total_deaths": "إجمالي الوفيات",
"total_affected": "إجمالي المتضررين",
"avg_risk": "متوسط درجة الخطورة",
"risk_level": "مستوى الخطورة السائد",
"data_source": "مصدر البيانات: قاعدة بيانات EM-DAT الدولية للكوارث. تختلف المناطق الإدارية حسب المصدر.",

"summary_report": "تقرير ملخص الكوارث",
"year_label": "السنة",
"disaster_type_label": "نوع الكارثة",
"total_events": "إجمالي الأحداث",
"total_affected_population": "إجمالي السكان المتضررين",
"read_summary": "قراءة الملخص"


    }
}


language = st.sidebar.selectbox("🌐 Language", list(LANG.keys()))
L = LANG[language]

# ======================================================
# TITLE
# ======================================================
st.title(f"🌍 {L['title']}")
st.info(L["theme_note"])

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_geojson():
    with open("data/new_original_india_disasters_synthetic_verified.geojson", "r") as f:
        return json.load(f)

def geojson_to_df(geojson):
    rows = []
    for f in geojson["features"]:
        p = f["properties"]
        rows.append({
            "Year": p["year"],
            "Disaster_Type": p["disaster_type"],
            "State": p.get("state", "Unknown"),
            "Deaths": p.get("Deaths", 0),
            "Affected_Population": p.get("Affected_Population", 0),
            "Risk_Score": p.get("Risk_Score", 0),
            "Risk_Level": p.get("incident_level", "Unknown"),
            "Event_Name": p.get("event_name", ""),
            "Source": p.get("source", "")
        })
    return pd.DataFrame(rows)

# ✅ FIRST load geojson
geojson = load_geojson()

# ✅ THEN convert to dataframe
df = geojson_to_df(geojson)


# ======================================================
# FILTERS
# ======================================================
st.sidebar.header(L["filters"])

year = st.sidebar.selectbox(
    L["year"],
    ["All"] + sorted(df["Year"].unique(), reverse=True)
)

disaster_type = st.sidebar.selectbox(
    L["type"],
    ["All"] + sorted(df["Disaster_Type"].unique())
)

filtered_df = df.copy()
if year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == year]
if disaster_type != "All":
    filtered_df = filtered_df[filtered_df["Disaster_Type"] == disaster_type]

# ======================================================
# TABULATION
# ======================================================
st.subheader(f"📋 {L['table']}")
st.dataframe(filtered_df, use_container_width=True)

# ======================================================
# MAP (BIG HOVER TOOLTIP – NO CLICK)
# ======================================================
st.subheader(f"🗺️ {L['map']}")

def filter_geo(features, filtered_df):
    allowed_keys = set(
        filtered_df.apply(
            lambda r: f"{r['Year']}_{r['Disaster_Type']}_{r.get('Event_Name','')}",
            axis=1
        )
    )

    out = []
    for f in features:
        p = f["properties"]
        key = f"{p['year']}_{p['disaster_type']}_{p.get('event_name','')}"

        if key in allowed_keys:
            out.append(f)

    return out

geo_filtered = filter_geo(geojson["features"], filtered_df)

if not geo_filtered:
    st.warning(L["no_data"])
else:
    m = folium.Map(
        location=[22.5, 78.9],
        zoom_start= 45,
        min_zoom=30,
        max_bounds=True,
        tiles=None
    )

    folium.TileLayer("OpenStreetMap", no_wrap=True).add_to(m)
    india_bounds = [[6.5, 68.0], [37.5, 97.5]]
    cluster = MarkerCluster().add_to(m)

    for f in geo_filtered:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"]
        color = "red" if p["incident_level"] == "Major" else "blue"

        hover_html = f"""
        <div style="font-size:14px; line-height:1.6; width:330px;">
        <b>{p['event_name']}</b><br><br>
        <b>Year:</b> {p['year']}<br>
        <b>Disaster Type:</b> {p['disaster_type']}<br>
        <b>Incident Level:</b> {p['incident_level']}<br><br>
        <b>Deaths:</b> {p.get('Deaths','N/A')}<br>
        <b>Affected Population:</b> {p.get('Affected_Population','N/A')}<br>
        <b>Risk Score:</b> {round(p.get('Risk_Score',0),2)}<br><br>
        <b>Source:</b> {p['source']}
        </div>
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.75,
            tooltip=folium.Tooltip(hover_html, sticky=True)
        ).add_to(cluster)

    m.fit_bounds(india_bounds)
    st_folium(m, width=1400, height=600, returned_objects=[])

    st.markdown(f"""
    **{L['legend']}**  
    🔴 {L['major']}  
    🔵 {L['minor']}
    """)

# ======================================================
# SUMMARY + OWNER SECTION (SIDE BY SIDE)
# ======================================================
st.markdown("---")

col_summary, col_owner = st.columns([2, 1])

# ---------------- SUMMARY ----------------
with col_summary:
    st.subheader(f"📄 {L.get('summary_report', 'Disaster Summary Report')}")

    if not filtered_df.empty:
        summary_md = f"""
**{L.get('year_label', 'Year')}**: {year}  
**{L.get('disaster_type_label', 'Disaster Type')}**: {disaster_type}  
**{L.get('total_events', 'Total Events')}**: {len(filtered_df)}  
**{L.get('total_deaths', 'Total Deaths')}**: {int(filtered_df['Deaths'].sum()):,}  
**{L.get('total_affected_population', 'Total Affected Population')}**: {int(filtered_df['Affected_Population'].sum()):,}  
**{L.get('avg_risk', 'Average Risk Score')}**: {round(filtered_df['Risk_Score'].mean(), 2)}
"""
        st.markdown(summary_md)

        if st.button(f"🔊 {L.get('read_summary', 'Read Summary')}"):
            engine = pyttsx3.init()
            engine.say(summary_md)
            engine.runAndWait()
    else:
        st.warning(L.get("no_data", "No data available"))

# ---------------- OWNER INFO ----------------
with col_owner:
    st.subheader("👤 Project Owner")

    st.markdown("""
    <style>
    .owner-container {
        margin-top: -6px;
    }

    .owner-row {
        display: flex;
        align-items: center;
        gap: 15px;
        margin: 8px 0;
        font-size: 15px;
    }

    .owner-label {
        min-width: 95px;
        font-weight: 600;
    }

    .owner-btn {
        padding: 7px 10px;
        border-radius: 6px;
        border: 1px solid #aaa;
        background: transparent;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
        transition: all 0.2s ease;
        line-height: 1.4;
    }

    .owner-btn:hover {
        background: rgba(0,0,0,0.05);
        transform: scale(1.06);
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }
    </style>

    <div class="owner-container">
        <b>Name:</b> MohanKumar<br>
        <b>Role:</b> Electronics & Disaster Analytics Developer
    </div>

    <div class="owner-row">
        🔗 <span class="owner-label">LinkedIn</span>
        <a class="owner-btn" href="https://www.linkedin.com/in/amohankumar07" target="_blank">
            Click Here
        </a>
    </div>

    <div class="owner-row">
        📸 <span class="owner-label">Instagram</span>
        <a class="owner-btn" href="https://www.instagram.com/my_dear_lightbright" target="_blank">
            Click Here
        </a>
    </div>

    <div class="owner-row">
        📧 <span class="owner-label">Email</span>
        <a class="owner-btn" href="mailto:mohankumar071104@gmail.com">
            Click Here
        </a>
    </div>

    <div class="owner-row">
        👽 <span class="owner-label">Github</span>
        <a class="owner-btn" href="https://github.com/IamMohan07/">
            Click Here
        </a>
    </div>
    """,
    unsafe_allow_html=True)


# ======================================================
# PREDEFINED AI ASSISTANT
# ======================================================
st.sidebar.subheader(f"🤖 {L['assistant']}")
q = st.sidebar.text_input(L["ask"])

if q:
    q = q.lower()
    if "flood" in q:
        st.sidebar.success("Floods are the most frequent disasters in India.")
    elif "cyclone" in q:
        st.sidebar.success("Cyclones mainly affect coastal regions.")
    elif "risk" in q:
        st.sidebar.success("High risk correlates with population density.")
    else:
        st.sidebar.info("Ask about floods, cyclones, or risk.")

# ======================================================
# SIDEBAR FOOTER (NO EXTRA SPACE)
# ======================================================
st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        font-size:12px;
        opacity:0.75;
        margin-top:3px;
        padding-top:15px;
        border-top:1px solid rgba(0,0,0,0.08);
    ">
        Made by <b>Mohan</b> with ❤️
    </div>
    """,
    unsafe_allow_html=True
)



# ======================================================
# ADVANCED ANALYTICS (2 x 2 GRID)
# ======================================================
st.markdown("---")
st.subheader(f"📊 {L['analytics']}")

# -------- Prepare data safely --------

# 1️⃣ Risk Level Distribution
risk_df = (
    filtered_df["Risk_Level"]
    .value_counts()
    .reset_index()
)
risk_df.columns = ["Risk_Level", "Count"]

# 2️⃣ Disaster Type Frequency
type_df = (
    filtered_df["Disaster_Type"]
    .value_counts()
    .reset_index()
)
type_df.columns = ["Disaster_Type", "Count"]

# 3️⃣ Year-wise Disaster Trend
year_df = (
    filtered_df.groupby("Year")
    .size()
    .reset_index(name="Events")
)

# 4️⃣ Top Affected States
state_df = (
    filtered_df.groupby("State")["Affected_Population"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# -------- 2 x 2 Layout --------
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# -------- Chart 1: Risk Level Distribution --------
with row1_col1:
    fig1 = px.bar(
        risk_df,
        x="Risk_Level",
        y="Count",
        color="Risk_Level",
        title= L["risk_level"],
        labels={"Count": L["count"],
                "Risk_Level": L["risk_level"]}
    )
    st.plotly_chart(fig1, use_container_width=True)

# -------- Chart 2: Disaster Type Frequency --------
with row1_col2:
    fig2 = px.bar(
        type_df,
        x="Disaster_Type",
        y="Count",
        color="Disaster_Type",
        title=L["disaster_freq"],
        labels={"Count": L["count"],
                "Disaster_Type": L["type"]}
    )
    st.plotly_chart(fig2, use_container_width=True)

# -------- Chart 3: Year-wise Disaster Trend --------
with row2_col1:
    fig3 = px.line(
        year_df,
        x="Year",
        y="Events",
        markers=True,
        title=L["year_trend"],
        labels={"Events": L["events"],
                "Year": L["year_label"]}
    )
    st.plotly_chart(fig3, use_container_width=True)

# -------- Chart 4: Top Affected States --------
with row2_col2:
    fig4 = px.bar(
        state_df,
        x="State",
        y="Affected_Population",
        color="Affected_Population",
        title=L["top_states"],
        labels={"Affected_Population": L["count"],
                "State": L["top_states"]}
    )
    st.plotly_chart(fig4, use_container_width=True)

    

# ======================================================
# KEY METRICS SECTION (LANGUAGE AWARE)
# ======================================================
st.markdown("---")
st.subheader(f"📌 {L.get('key_metrics', 'Key Disaster Metrics')}")

c1, c2, c3, c4 = st.columns(4)

# ---- Metric 1: Total Deaths ----
total_deaths = int(filtered_df["Deaths"].sum()) if not filtered_df.empty else 0
c1.metric(
    L.get("total_deaths", "Total Deaths"),
    f"{total_deaths:,}"
)

# ---- Metric 2: Total Affected ----
total_affected = int(filtered_df["Affected_Population"].sum()) if not filtered_df.empty else 0
c2.metric(
    L.get("total_affected", "Total Affected"),
    f"{total_affected:,}"
)

# ---- Metric 3: Average Risk Score ----
avg_risk = round(filtered_df["Risk_Score"].mean(), 2) if not filtered_df.empty else 0
c3.metric(
    L.get("avg_risk", "Average Risk Score"),
    avg_risk
)

# ---- Metric 4: Dominant Risk Level ----
dominant_risk = (
    filtered_df["Risk_Level"].mode()[0]
    if not filtered_df.empty
    else "N/A"
)
c4.metric(
    L.get("risk_level", "Dominant Risk Level"),
    dominant_risk
)


# ======================================================
# FOOTNOTE
# ======================================================

st.markdown("---")
st.markdown(
    f"📌 *{L.get('data_source', 'Data Source: EM-DAT International Disaster Database.')}*"
)

# ======================================================
# FINAL FOOTER
# ======================================================
# Close main content
st.markdown('</div>', unsafe_allow_html=True)

# Footer — TRUE PAGE END
st.markdown("""
<div class="app-footer">
© 2026 Mohan Kumar. All Rights Reserved.
</div>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Full height layout */
html, body, [data-testid="stAppViewContainer"] {
    height: 100%;
    margin: 0;
    padding: 0;
}

/* Streamlit app root */
[data-testid="stApp"] {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* Main content grows naturally */
.main-content {
    flex: 1;
    padding-bottom: 0px !important;
}

/* REMOVE Streamlit's default bottom spacing */
[data-testid="block-container"] {
    padding-bottom: 0px !important;
    margin-bottom: 0px !important;
}

/* Footer */
.app-footer {
    text-align: center;
    font-size: 13px;
    color: #777;
    padding: 6px 0 6px 0;
    border-top: 1px solid #eee;
    margin: 0;
}
</style>
""", unsafe_allow_html=True)
