"""
AI Menu Recommendation System
A premium Streamlit app with rule-based food recommendations for Lahore.

Run:
    pip install streamlit
    streamlit run app.py
"""

import streamlit as st
import urllib.parse
import random

# ----------------------------- PAGE CONFIG ----------------------------- #
st.set_page_config(
    page_title="AI Menu Recommendation System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------- SESSION STATE ----------------------------- #
def init_state():
    defaults = {
        "logged_in": False,
        "user_name": "",
        "auth_mode": "login",   # login | guest | google
        "theme": "Dark",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ----------------------------- THEME / CSS ----------------------------- #
def inject_css(theme: str):
    if theme == "Dark":
        bg = "#0f172a"
        bg2 = "#111a32"
        text = "#e2e8f0"
        muted = "#94a3b8"
        glass = "rgba(255,255,255,0.04)"
        border = "rgba(255,255,255,0.08)"
    else:
        bg = "#f8fafc"
        bg2 = "#eef2ff"
        text = "#0f172a"
        muted = "#475569"
        glass = "rgba(255,255,255,0.7)"
        border = "rgba(15,23,42,0.08)"

    st.markdown(
        f"""
        <style>
        :root {{
            --indigo: #6366f1;
            --cyan: #06b6d4;
            --navy: #0f172a;
        }}

        html, body, [class*="css"], .stApp {{
            background: linear-gradient(135deg, {bg} 0%, {bg2} 100%) !important;
            color: {text} !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* Hide default Streamlit chrome on small screens neatly */
        #MainMenu, footer {{visibility: hidden;}}
        header {{background: transparent !important;}}

        /* Cursor glow blob */
        .cursor-glow {{
            position: fixed;
            top: 0; left: 0;
            width: 380px; height: 380px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99,102,241,0.25) 0%, rgba(6,182,212,0.10) 40%, transparent 70%);
            pointer-events: none;
            transform: translate(-50%, -50%);
            transition: transform 0.18s ease-out;
            z-index: 0;
            filter: blur(20px);
        }}

        /* Hero */
        .hero {{
            text-align: center;
            padding: 2.2rem 1rem 1rem 1rem;
            position: relative;
            z-index: 1;
        }}
        .hero h1 {{
            font-size: clamp(1.8rem, 4vw, 3rem);
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.02em;
        }}
        .hero-icon {{
            -webkit-text-fill-color: initial;
            background: none;
        }}
        .hero-text {{
            background: linear-gradient(90deg, var(--indigo), var(--cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .hero p {{
            color: {muted};
            font-size: clamp(0.95rem, 1.5vw, 1.1rem);
            margin-top: 0.4rem;
        }}

        /* Glass panel */
        .glass {{
            background: {glass};
            backdrop-filter: blur(14px);
            border: 1px solid {border};
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.18);
        }}

        /* Auth card */
        .auth-wrap {{
            max-width: 460px;
            margin: 4vh auto;
            position: relative;
            z-index: 1;
        }}

        /* Streamlit buttons */
        .stButton>button {{
            background: linear-gradient(135deg, var(--indigo), var(--cyan));
            color: white !important;
            border: none;
            border-radius: 14px;
            padding: 0.65rem 1.3rem;
            font-weight: 600;
            transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
            box-shadow: 0 6px 20px rgba(99,102,241,0.35);
            width: 100%;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(6,182,212,0.45);
            filter: brightness(1.05);
        }}

        /* Inputs */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {{
            background: {glass} !important;
            color: {text} !important;
            border-radius: 12px !important;
            border: 1px solid {border} !important;
        }}
        label, .stMarkdown, .stRadio label {{
            color: {text} !important;
        }}

        /* Recommendation card */
        .rec-card {{
            border-radius: 20px;
            padding: 1.2rem 1.3rem;
            margin-bottom: 1.1rem;
            border: 2px solid var(--card-border);
            background: var(--card-bg);
            box-shadow: 0 8px 24px rgba(0,0,0,0.10);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            position: relative;
            overflow: hidden;
        }}
        .rec-card:hover {{
            transform: translateY(-6px) scale(1.01);
            box-shadow: 0 18px 40px rgba(0,0,0,0.18);
        }}
        .rec-icon {{
            font-size: 2.4rem;
            line-height: 1;
            margin-bottom: 0.4rem;
            display: inline-block;
            animation: floaty 3.5s ease-in-out infinite;
        }}
        @keyframes floaty {{
            0%,100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-6px); }}
        }}
        .rec-name {{
            font-size: 1.25rem;
            font-weight: 800;
            color: #0f172a;
            margin: 0;
        }}
        .rec-desc {{
            color: #334155;
            font-size: 0.95rem;
            margin: 0.4rem 0 0.9rem 0;
        }}
        .rec-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }}
        .rec-price {{
            font-weight: 800;
            color: #0f172a;
            font-size: 1.05rem;
        }}
        .rec-loc {{
            color: #475569;
            font-size: 0.9rem;
            text-align: right;
            max-width: 60%;
        }}
        .rec-rating {{
            color: #b45309;
            font-weight: 700;
            margin-bottom: 0.7rem;
        }}
        .map-btn {{
            display: inline-block;
            background: linear-gradient(135deg, var(--indigo), var(--cyan));
            color: white !important;
            text-decoration: none !important;
            padding: 0.5rem 0.9rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.88rem;
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            box-shadow: 0 4px 14px rgba(99,102,241,0.35);
        }}
        .map-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 22px rgba(6,182,212,0.45);
        }}

        /* Footer */
        .app-footer {{
            text-align: center;
            margin-top: 2.5rem;
            padding: 1.2rem;
            color: {muted};
            font-size: 1rem;
            background: linear-gradient(90deg, rgba(99,102,241,0.10), rgba(6,182,212,0.10));
            border-radius: 16px;
        }}

        /* Mobile */
        @media (max-width: 768px) {{
            .rec-loc {{ text-align: left; max-width: 100%; }}
            .hero {{ padding: 1.2rem 0.5rem; }}
            .glass {{ padding: 1rem; border-radius: 16px; }}
        }}
        </style>

        <div class="cursor-glow" id="cursor-glow"></div>
        <script>
        (function() {{
            const glow = window.parent.document.getElementById('cursor-glow') || document.getElementById('cursor-glow');
            if (!glow) return;
            const move = (e) => {{
                glow.style.transform = `translate(${{e.clientX}}px, ${{e.clientY}}px) translate(-50%,-50%)`;
            }};
            window.addEventListener('mousemove', move);
            window.parent && window.parent.addEventListener && window.parent.addEventListener('mousemove', move);
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------- DATA ----------------------------- #
# Each item: name, desc, price, rating, emoji, cuisine, taste, category, health tags, budget, location, maps
MENU = [
    # ---------------- DESI ----------------
    # ---------------- Spicy / Savory ---------------
    {"name": "Nihari Special", "desc": "Slow-cooked beef shank in rich spicy gravy.", "price": 1800,
     "rating": 4.8, "emoji": "🍲", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions"], "budget": "High",
     "location": "Waris Nihari, Lakshmi Chowk, Lahore"},
    {"name": "Chicken Karahi", "desc": "Traditional tomato-based spicy chicken karahi.", "price": 1000,
     "rating": 4.7, "emoji": "🍗", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions"], "budget": "Medium",
     "location": "Butt Karahi, Lakshmi Chowk, Lahore"},
    {"name": "Daal Chawal", "desc": "Comforting lentils with steamed basmati rice.", "price": 250,
     "rating": 4.4, "emoji": "🍛", "cuisine": "Desi", "taste": ["Savory", "Healthy"],
     "category": "Food", "health": ["Vegan", "Low Calories", "Lactose Intolerant", "No Restrictions", "High Protein (Gym)", "Diabetic Friendly"], "budget": "Low",
     "location": "Student Biryani, Gulberg, Lahore"},
    {"name": "Seekh Kebab Plate", "desc": "Charcoal-grilled minced beef kebabs with naan.", "price": 900,
     "rating": 4.6, "emoji": "🍢", "cuisine": "BBQ", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["High Protein (Gym)", "No Restrictions"], "budget": "Medium",
     "location": "Bundu Khan, MM Alam Road, Lahore"},
    {"name": "Mutton Biryani", "desc": "Fragrant basmati rice layered with spicy tender mutton.", "price": 950,
     "rating": 4.7, "emoji": "🍚", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions", "High Protein (Gym)", "Lactose Intolerant"], "budget": "Medium",
     "location": "Pak Tea House, Mall Road, Lahore"},
    {"name": "Chicken Biryani", "desc": "Fragrant basmati rice layered with spicy chicken and aromatic herbs for a flavorful meal.", "price": 350,
     "rating": 4.7, "emoji": "🍚", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions", "High Protein (Gym)", "Lactose Intolerant"], "budget": "Low",
     "location": "Biryani Master, DHA, Lahore"},
    {"name": "Beef Biryani", "desc": "Fragrant basmati rice layered with spicy beef and aromatic herbs for a flavorful meal.", "price": 1500,
     "rating": 4.7, "emoji": "🍚", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions", "High Protein (Gym)", "Lactose Intolerant"], "budget": "High",
     "location": "Nalli Pur - Biryani & Pulao, Lakshmi Chowk, Lahore"},
    {"name": "Haleem", "desc": "A slow-cooked blend of meat, lentils, and wheat, known for its creamy and hearty texture.", "price": 300,
     "rating": 4.7, "emoji": "🍲", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions"], "budget": "Low",
     "location": "Haleem Kinara, DHA, Lahore"},
    {"name": "Paya", "desc": "Flavorful trotters simmered overnight in a spicy curry for a rich and comforting taste.", "price": 1200,
     "rating": 4.7, "emoji": "🥘", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions", "High Protein (Gym)", "Lactose Intolerant"], "budget": "High",
     "location": "Haleem Kinara, DHA, Lahore"},
    {"name": "Lahori Fried Fish", "desc": "Crispy battered fish fillets marinated with traditional Lahori spices and deep-fried to perfection.", "price": 1000,
     "rating": 4.8, "emoji": "🐟", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions", "High Protein (Gym)", "Lactose Intolerant"], "budget": "Medium",
     "location": "Arshad Lahori Fish Corner, Gulshan-e-Ravi, Lahore"},
    {"name": "Anda Shami Burger", "desc": "A soft bun filled with shami kebab, fried egg, chutneys, and fresh vegetables.", "price": 250,
     "rating": 4.7, "emoji": "🍔", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions", "Low Calories"], "budget": "Low",
     "location": "Liberty Burger, Liberty, Lahore"},
    {"name": "Chapli Kebab", "desc": "Juicy minced meat patties packed with herbs, spices, and a smoky flavor.", "price": 300,
     "rating": 4.6, "emoji": "🥩", "cuisine": "Desi", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions", "High Protein (Gym)"], "budget": "Low",
     "location": "Khan Chapli Kabab & Fish Corner, Gulberg, Lahore"},
     #-------------- Sweet ------------
    {"name": "Gulab Jamun", "desc": "Soft milk-based dumplings soaked in fragrant sugar syrup for a rich and sweet treat.", "price": 150,
     "rating": 4.9, "emoji": "🥮", "cuisine": "Desi", "taste": ["Sweet"],
     "category": "Food", "health": ["No Restrictions", "Vegan", "Lactose Intolerant"], "budget": "Low",
     "location": "Sharaqpuri Gulab Jamun by Soughat House, Gulberg, Lahore"},
    {"name": "Kheer", "desc": "Creamy rice pudding cooked with milk, sugar, and cardamom, often topped with nuts.", "price": 100,
     "rating": 4.4, "emoji": "🥧", "cuisine": "Desi", "taste": ["Sweet"],
     "category": "Food", "health": ["No Restrictions", "Vegan"], "budget": "Low",
     "location": "Chashni, DHA, Lahore"},
    {"name": "Rabri", "desc": "A refreshing dessert drink made with milk, vermicelli, basil seeds, jelly, and ice cream.", "price": 800,
     "rating": 4.6, "emoji": "🥛", "cuisine": "Desi", "taste": ["Sweet"],
     "category": "Drink", "health": ["No Restrictions", "Vegan"], "budget": "Medium",
     "location": "Mashallah Nafees Kasuri Faluda, Kasur Rd, Lahore"},
    {"name": "Falooda", "desc": "Thickened sweet milk dessert flavored with cardamom and garnished with dry fruits.", "price": 1000,
     "rating": 4.6, "emoji": "🍨", "cuisine": "Desi", "taste": ["Sweet"],
     "category": "Food", "health": ["No Restrictions", "Vegan"], "budget": "Medium",
     "location": "Mashallah Nafees Kasuri Faluda, Kasur Rd, Lahore"},
     {"name": "Jalebi", "desc": "Crispy fried sweet swirls in sugar syrup.", "price": 300,
     "rating": 4.6, "emoji": "🥨", "cuisine": "Desi", "taste": ["Sweet"],
     "category": "Food", "health": ["Vegan", "No Restrictions", "Lactose Intolerant"], "budget": "Low",
     "location": "Gawalmandi Food Street, Lahore"},
     {"name": "Ras Malai", "desc": "Soft cheese patties soaked in sweetened creamy milk flavored with saffron and cardamom.", "price": 1200,
     "rating": 4.5, "emoji": "🥣", "cuisine": "Desi", "taste": ["Sweet"],
     "category": "Food", "health": ["Vegan", "No Restrictions", "Lactose Intolerant"], "budget": "High",
     "location": "Amritsari Sweets Shop, Johar Town, Lahore"},


    # ---------------- CHINESE ----------------
    {"name": "Chicken Manchurian", "desc": "Crispy chicken tossed in tangy Manchurian sauce.", "price": 850,
     "rating": 4.5, "emoji": "🥡", "cuisine": "Chinese", "taste": ["Savory", "Spicy"],
     "category": "Food", "health": ["No Restrictions", "High Protein (Gym)"], "budget": "Medium",
     "location": "Yum Chinese & Thai, Gulberg, Lahore"},
    {"name": "Veggie Hakka Noodles", "desc": "Stir-fried noodles with fresh seasonal veggies.", "price": 600,
     "rating": 4.3, "emoji": "🍜", "cuisine": "Chinese", "taste": ["Savory", "Healthy"],
     "category": "Food", "health": ["Vegan", "Lactose Intolerant", "Low Calories"], "budget": "Low",
     "location": "China Town, Fortress Stadium, Lahore"},
     {"name": "Tanghulu", "desc": "Sweet crunchy candied fruit.", "price": 350,
     "rating": 4.3, "emoji": "🍡", "cuisine": "Chinese", "taste": ["Sweet"],
     "category": "Food", "health": ["Vegan", "Lactose Intolerant", "No Restrictions"], "budget": "Low",
     "location": "Haute Dolci Raya, DHA, Lahore"},
     {"name": "Mochi", "desc": "Soft Japanese-style sweet rice cake dessert.", "price": 400,
     "rating": 4.5, "emoji": "🍥", "cuisine": "Chinese", "taste": ["Sweet"],
     "category": "Food", "health": ["Vegan"], "budget": "Low",
     "location": "Dessert Corner, Lahore"},
     {"name": "Sweet & Sour Chicken", "desc": "Chicken in sweet tangy pineapple sauce.", "price": 900,
     "rating": 4.6, "emoji": "🍍", "cuisine": "Chinese", "taste": ["Sweet", "Savory"],
     "category": "Food", "health": ["No Restrictions"], "budget": "Medium",
     "location": "Yum Chinese, Lahore"},
     {"name": "Kung Pao Chicken", "desc": "Spicy chicken with peanuts and chili sauce.", "price": 950,
     "rating": 4.6, "emoji": "🌶️", "cuisine": "Chinese", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["High Protein (Gym)"], "budget": "Medium",
     "location": "Chinese Pavilion, Lahore"},
     {"name": "Dumplings", "desc": "Steamed stuffed dumplings with soy dip.", "price": 700,
     "rating": 4.5, "emoji": "🥟", "cuisine": "Chinese", "taste": ["Savory"],
     "category": "Food", "health": ["Low Calories"], "budget": "Medium",
     "location": "China Town, Lahore"},
     {"name": "Bubble Tea", "desc": "Milk tea with chewy tapioca pearls.", "price": 500,
     "rating": 4.7, "emoji": "🧋", "cuisine": "Chinese", "taste": ["Sweet"],
     "category": "Drink", "health": ["No Restrictions"], "budget": "Low",
     "location": "Cafe Street, Lahore"},

    # ---------------- ITALIAN ----------------
    {"name": "Margherita Pizza", "desc": "Wood-fired crust, San Marzano tomato, fresh mozzarella.", "price": 1500,
     "rating": 4.6, "emoji": "🍕", "cuisine": "Italian", "taste": ["Savory"],
     "category": "Food", "health": ["No Restrictions", "High Protein (Gym)"], "budget": "High",
     "location": "Cosa Nostra, Gulberg, Lahore"},
    {"name": "Chicken Alfredo Pasta", "desc": "Creamy pasta with grilled chicken.", "price": 1200,
    "rating": 4.5, "emoji": "🍝", "cuisine": "Italian", "taste": ["Savory"],
    "category": "Food", "health": ["High Protein (Gym)"], "budget": "Medium",
    "location": "Spaghetti House, Lahore"},
    {"name": "Tiramisu", "desc": "Coffee-flavored creamy dessert.", "price": 700,
    "rating": 4.7, "emoji": "🍰", "cuisine": "Italian", "taste": ["Sweet"],
    "category": "Food", "health": ["No Restrictions"], "budget": "Medium",
    "location": "Cafe Aylanto, Lahore"},
    {"name": "Panna Cotta", "desc": "Creamy vanilla Italian dessert.", "price": 650,
    "rating": 4.6, "emoji": "🍮", "cuisine": "Italian", "taste": ["Sweet"],
    "category": "Food", "health": ["No Restrictions"], "budget": "Medium",
    "location": "Italian Corner, Lahore"},
    {"name": "Garlic Bread", "desc": "Toasted bread with garlic butter.", "price": 400,
    "rating": 4.3, "emoji": "🥖", "cuisine": "Italian", "taste": ["Savory"],
    "category": "Food", "health": ["Low Calories"], "budget": "Low",
    "location": "Pizza Places, Lahore"},
    {"name": "Veggie Pizza", "desc": "Pizza topped with fresh vegetables.", "price": 1300,
    "rating": 4.4, "emoji": "🍕", "cuisine": "Italian", "taste": ["Healthy"],
    "category": "Food", "health": ["Vegan", "Low Calories"], "budget": "High",
    "location": "Italian Bistro, Lahore"},
    {"name": "Gelato", "desc": "Italian style creamy ice cream.", "price": 500,
    "rating": 4.8, "emoji": "🍦", "cuisine": "Italian", "taste": ["Sweet"],
    "category": "Food", "health": ["No Restrictions"], "budget": "Low",
    "location": "Gelato Spot, Lahore"},

    # ---------------- CONTINENTAL ----------------
    {"name": "Grilled Chicken Steak", "desc": "Lean grilled chicken with sautéed veggies.", "price": 1400,
     "rating": 4.5, "emoji": "🍗", "cuisine": "Continental", "taste": ["Healthy", "Savory"],
     "category": "Food", "health": ["High Protein (Gym)", "Low Calories", "Diabetic Friendly"], "budget": "High",
     "location": "Cafe Zouk, MM Alam Road, Lahore"},
    {"name": "Caesar Salad", "desc": "Crisp romaine, parmesan, croutons, Caesar dressing.", "price": 800,
     "rating": 4.3, "emoji": "🥗", "cuisine": "Continental", "taste": ["Healthy"],
     "category": "Food", "health": ["Low Calories", "Diabetic Friendly", "High Protein (Gym)"], "budget": "Medium",
     "location": "Arcadian Cafe, DHA, Lahore"},
     {"name": "Mushroom Soup", "desc": "Creamy mushroom soup bowl.", "price": 600,
    "rating": 4.4, "emoji": "🍲", "cuisine": "Continental", "taste": ["Healthy"],
    "category": "Food", "health": ["Low Calories"], "budget": "Low",
    "location": "Continental Cafe, Lahore"},
    {"name": "Fish & Chips", "desc": "Crispy fish with fries.", "price": 1200,
    "rating": 4.5, "emoji": "🐟", "cuisine": "Continental", "taste": ["Savory"],
    "category": "Food", "health": ["No Restrictions"], "budget": "High",
    "location": "Ocean Grill, Lahore"},
    {"name": "Avocado Toast", "desc": "Healthy toast with avocado spread.", "price": 700,
    "rating": 4.6, "emoji": "🥑", "cuisine": "Continental", "taste": ["Healthy"],
    "category": "Food", "health": ["Vegan", "Low Calories"], "budget": "Medium",
    "location": "Healthy Cafe, Lahore"},

    # ---------------- FAST FOOD ----------------
    {"name": "Zinger Burger", "desc": "Crispy chicken fillet with mayo and lettuce.", "price": 550,
     "rating": 4.4, "emoji": "🍔", "cuisine": "Fast Food", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions"], "budget": "Low",
     "location": "Johnny & Jugnu, Gulberg, Lahore"},
    {"name": "Loaded Fries", "desc": "Fries topped with cheese sauce and jalapenos.", "price": 450,
     "rating": 4.2, "emoji": "🍟", "cuisine": "Fast Food", "taste": ["Savory"],
     "category": "Food", "health": ["No Restrictions"], "budget": "Low",
     "location": "Howdy, MM Alam Road, Lahore"},
    {"name": "Chicken Shawarma", "desc": "Wrap filled with spiced chicken.", "price": 400,
    "rating": 4.5, "emoji": "🌯", "cuisine": "Fast Food", "taste": ["Savory"],
    "category": "Food", "health": ["High Protein (Gym)"], "budget": "Low",
    "location": "Shawarma Hub, Lahore"},
    {"name": "Chicken Nuggets", "desc": "Crispy fried chicken bites.", "price": 500,
    "rating": 4.3, "emoji": "🍗", "cuisine": "Fast Food", "taste": ["Savory"],
    "category": "Food", "health": ["No Restrictions"], "budget": "Low",
    "location": "Fast Food Corner, Lahore"},
    {"name": "Chocolate Shake", "desc": "Cold chocolate milkshake.", "price": 450,
    "rating": 4.6, "emoji": "🥤", "cuisine": "Fast Food", "taste": ["Sweet"],
    "category": "Drink", "health": ["No Restrictions"], "budget": "Low",
    "location": "Shake House, Lahore"},
    {"name": "Club Sandwich", "desc": "Layered sandwich with chicken & veggies.", "price": 600,
    "rating": 4.4, "emoji": "🥪", "cuisine": "Fast Food", "taste": ["Savory"],
    "category": "Food", "health": ["High Protein (Gym)"], "budget": "Medium",
    "location": "Cafe Fast, Lahore"},

    # ---------------- BBQ ----------------
    {"name": "Chicken Tikka", "desc": "Spicy charcoal-grilled chicken on the bone.", "price": 700,
     "rating": 4.6, "emoji": "🍖", "cuisine": "BBQ", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["High Protein (Gym)", "Diabetic Friendly", "Low Calories"], "budget": "Medium",
     "location": "Salt'n Pepper Village, Lahore"},
    {"name": "Beef Boti", "desc": "Marinated beef cubes grilled over open flame.", "price": 900,
     "rating": 4.5, "emoji": "🥩", "cuisine": "BBQ", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["High Protein (Gym)"], "budget": "Medium",
     "location": "Cooco's Den, Food Street, Lahore"},
    {"name": "Samosa", "desc": "Crispy fried pastry with filling.", "price": 100,
    "rating": 4.4, "emoji": "🥟", "cuisine": "Street Food", "taste": ["Savory"],
    "category": "Food", "health": ["No Restrictions"], "budget": "Low",
    "location": "Street Stalls, Lahore"},
    {"name": "Fruit Chaat", "desc": "Mixed fruits with spices.", "price": 250,
    "rating": 4.6, "emoji": "🍉", "cuisine": "Street Food", "taste": ["Sweet", "Healthy"],
    "category": "Food", "health": ["Vegan", "Low Calories"], "budget": "Low",
    "location": "Food Street, Lahore"},
    {"name": "Sugarcane Juice", "desc": "Fresh natural sweet juice.", "price": 150,
    "rating": 4.7, "emoji": "🧃", "cuisine": "Street Food", "taste": ["Sweet"],
    "category": "Drink", "health": ["Vegan", "Low Calories"], "budget": "Low",
    "location": "Roadside Stalls, Lahore"},
    {"name": "Chicken Malai Boti", "desc": "Creamy soft grilled chicken cubes.", "price": 850,
    "rating": 4.7, "emoji": "🍢", "cuisine": "BBQ", "taste": ["Savory"],
    "category": "Food", "health": ["High Protein (Gym)"], "budget": "Medium",
    "location": "Bundu Khan, Lahore"},
    {"name": "Beef Seekh Kebab", "desc": "Spiced minced beef grilled on skewers.", "price": 900,
    "rating": 4.6, "emoji": "🥩", "cuisine": "BBQ", "taste": ["Spicy", "Savory"],
    "category": "Food", "health": ["High Protein (Gym)", "No Restrictions"], "budget": "Medium",
    "location": "Food Street, Lahore"},
    {"name": "Behari Boti", "desc": "Tender beef marinated in rich spices.", "price": 950,
    "rating": 4.7, "emoji": "🔥", "cuisine": "BBQ", "taste": ["Spicy", "Savory"],
    "category": "Food", "health": ["High Protein (Gym)"], "budget": "Medium",
    "location": "Cooco's Den, Lahore"},
    {"name": "Grilled Fish Tikka", "desc": "Healthy grilled fish with spices.", "price": 1000,
    "rating": 4.5, "emoji": "🐟", "cuisine": "BBQ", "taste": ["Savory"],
    "category": "Food", "health": ["Low Calories", "High Protein (Gym)", "Diabetic Friendly"], "budget": "High",
    "location": "River View BBQ, Lahore"},
    {"name": "Reshmi Kebab", "desc": "Soft creamy chicken kebabs.", "price": 800,
    "rating": 4.6, "emoji": "🍢", "cuisine": "BBQ", "taste": ["Savory"],
    "category": "Food", "health": ["High Protein (Gym)"], "budget": "Medium",
    "location": "Barbecue Tonight, Lahore"},
    {"name": "Afghani Chicken", "desc": "Creamy whole chicken BBQ style.", "price": 1200,
    "rating": 4.7, "emoji": "🍗", "cuisine": "BBQ", "taste": ["Savory"],
    "category": "Food", "health": ["High Protein (Gym)"], "budget": "High",
    "location": "BBQ Tonight, Lahore"},
    {"name": "Chicken Wings BBQ", "desc": "Spicy grilled chicken wings.", "price": 650,
    "rating": 4.5, "emoji": "🍗", "cuisine": "BBQ", "taste": ["Spicy", "Savory"],
    "category": "Food", "health": ["No Restrictions", "High Protein (Gym)"], "budget": "Low",
    "location": "Fast BBQ Corner, Lahore"},

    # ---------------- STREET FOOD ----------------
    {"name": "Gol Gappay", "desc": "Crispy puris with tangy tamarind water.", "price": 150,
     "rating": 4.7, "emoji": "🥟", "cuisine": "Street Food", "taste": ["Spicy"],
     "category": "Food", "health": ["Vegan", "Lactose Intolerant", "Low Calories", "No Restrictions"], "budget": "Low",
     "location": "Liberty Market, Gulberg, Lahore"},
    {"name": "Dahi Bhalla", "desc": "Lentil dumplings in spiced yogurt with chutney.", "price": 200,
     "rating": 4.5, "emoji": "🥣", "cuisine": "Street Food", "taste": ["Spicy", "Savory"],
     "category": "Food", "health": ["No Restrictions"], "budget": "Low",
     "location": "Anarkali Bazaar, Lahore"},
    {"name": "Jalebi", "desc": "Crispy fried sweet swirls in sugar syrup.", "price": 300,
     "rating": 4.6, "emoji": "🍥", "cuisine": "Street Food", "taste": ["Sweet"],
     "category": "Food", "health": ["Vegan", "No Restrictions"], "budget": "Low",
     "location": "Gawalmandi Food Street, Lahore"},

    # ---------------- DRINKS ----------------
    {"name": "Kashmiri Chai", "desc": "Pink tea with crushed pistachios.", "price": 250,
     "rating": 4.6, "emoji": "🍵", "cuisine": "Desi", "taste": ["Sweet"],
     "category": "Drink", "health": ["No Restrictions"], "budget": "Low",
     "location": "Chai Shai, Liberty, Lahore"},
    {"name": "Fresh Lime Mojito", "desc": "Refreshing mint and lime fizz.", "price": 350,
     "rating": 4.5, "emoji": "🍹", "cuisine": "Continental", "taste": ["Sweet", "Healthy"],
     "category": "Drink", "health": ["Vegan", "Low Calories", "Lactose Intolerant"], "budget": "Low",
     "location": "Cafe Aylanto, MM Alam Road, Lahore"},
    {"name": "Cold Coffee", "desc": "Iced coffee blended with vanilla.", "price": 450,
     "rating": 4.4, "emoji": "☕", "cuisine": "Continental", "taste": ["Sweet"],
     "category": "Drink", "health": ["No Restrictions"], "budget": "Medium",
     "location": "Mocca Coffee, Gulberg, Lahore"},
    {"name": "Mango Lassi", "desc": "Creamy yogurt blended with sweet mangoes.", "price": 300,
     "rating": 4.7, "emoji": "🥭", "cuisine": "Desi", "taste": ["Sweet"],
     "category": "Drink", "health": ["No Restrictions"], "budget": "Low",
     "location": "Bundu Khan, MM Alam Road, Lahore"},
    {"name": "Protein Shake", "desc": "Banana, peanut butter, whey & oats.", "price": 600,
     "rating": 4.5, "emoji": "🥤", "cuisine": "Continental", "taste": ["Healthy", "Sweet"],
     "category": "Drink", "health": ["High Protein (Gym)", "Diabetic Friendly"], "budget": "Medium",
     "location": "Fuel Cafe, DHA, Lahore"},
    {"name": "Green Detox Juice", "desc": "Spinach, apple, lemon, ginger blend.", "price": 400,
     "rating": 4.3, "emoji": "🥒", "cuisine": "Continental", "taste": ["Healthy"],
     "category": "Drink", "health": ["Vegan", "Low Calories", "Diabetic Friendly", "Lactose Intolerant", "High Protein (Gym)"], "budget": "Medium",
     "location": "The Juice Bar, Gulberg, Lahore"},
]

# Card border palette
CARD_COLORS = [
    {"border": "#6366f1", "bg": "#eef0ff"},   # indigo
    {"border": "#06b6d4", "bg": "#e6fbff"},   # cyan
    {"border": "#f59e0b", "bg": "#fff7e6"},   # amber
    {"border": "#ef4444", "bg": "#ffecec"},   # red
    {"border": "#10b981", "bg": "#e7fbf3"},   # emerald
    {"border": "#a855f7", "bg": "#f5ecff"},   # purple
]


# ----------------------------- RECOMMENDATION LOGIC ----------------------------- #
def score_item(item, prefs):
    """Rule-based scoring."""
    score = 0
    if prefs["category"] == item["category"]:
        score += 5
    if prefs["cuisine"] == item["cuisine"]:
        score += 4
    elif prefs["category"] == "Drink" and item["category"] == "Drink":
        score += 1  # cuisine matters less for drinks
    if prefs["taste"] in item["taste"]:
        score += 3
    if prefs["budget"] == item["budget"]:
        score += 2
    if prefs["health"] in item["health"]:
        score += 4
    # elif prefs["health"] == "No Restrictions":
    #     score += 1
    return score


def recommend(prefs):
    scored = []

    for item in MENU:
        if item["category"] != prefs["category"]:
            continue
        score = score_item(item, prefs)

        # Only keep relevant matches
        # if score >= 10:
        scored.append((score, item))

    # Sort by highest score then rating
    scored.sort(key=lambda x: (-x[0], -x[1]["rating"]))

    # Return top matching items only
    results = [item for score, item in scored[:5]]
    return results

def maps_link(address: str) -> str:
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(address)


# ----------------------------- AUTH UI ----------------------------- #
def auth_screen():
    inject_css(st.session_state.theme)
    st.markdown(
        """
        <div class="hero">
            <h1><span class="hero-icon">🍽️</span> <span class="hero-text">AI Menu Recommender</span></h1>
            <p>Sign in to discover your perfect bite in Lahore.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown('<div class="glass auth-wrap">', unsafe_allow_html=True)
        tab = st.radio("Choose how to continue:", ["Email Login", "Guest", "Google"], horizontal=True)

        if tab == "Email Login":
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            if st.button("Sign In", key="signin"):
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_name = email.split("@")[0].title()
                    st.success("Welcome back! 🎉")
                    st.rerun()
                else:
                    st.warning("Please enter email & password.")
        elif tab == "Guest":
            st.info("Continue without an account. Your preferences won't be saved.")
            if st.button("Continue as Guest 👤"):
                st.session_state.logged_in = True
                st.session_state.user_name = "Guest"
                st.rerun()
        else:
            st.info("Sign in with your Google account (UI demo).")
            if st.button("🔵 Sign in with Google"):
                st.session_state.logged_in = True
                st.session_state.user_name = "Google User"
                st.success("Signed in with Google!")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------- MAIN APP ----------------------------- #
def render_card(item, idx):
    palette = CARD_COLORS[idx % len(CARD_COLORS)]
    stars = "⭐" * int(round(item["rating"]))
    link = maps_link(item["location"])
    st.markdown(
        f"""
        <div class="rec-card" style="--card-border:{palette['border']}; --card-bg:{palette['bg']};">
            <div class="rec-icon">{item['emoji']}</div>
            <p class="rec-name">{item['name']}</p>
            <p class="rec-desc">{item['desc']}</p>
            <div class="rec-row">
                <div class="rec-price">Rs. {item['price']:,} PKR</div>
                <div class="rec-loc">📍 {item['location']}</div>
            </div>
            <div class="rec-rating">{stars} <span style="color:#64748b;font-weight:500;">({item['rating']})</span></div>
            <a class="map-btn" href="{link}" target="_blank" rel="noopener">🗺️ View on Map</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main_app():
    inject_css(st.session_state.theme)

    # Top bar
    top = st.columns([3, 1, 1])
    with top[0]:
        st.markdown(
            f"""
            <div class="hero" style="text-align:left; padding-bottom:0;">
                <h1>Hi, {st.session_state.user_name} 👋</h1>
                <p>
                    Stop scrolling, start eating.<br>
                    Curated food picks that match your hunger, mood, and budget — instantly 🔥.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top[1]:
        theme = st.selectbox("🎨 Theme", ["Dark", "Light"],
                             index=0 if st.session_state.theme == "Dark" else 1)
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.rerun()
    with top[2]:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.rerun()

    # Preferences panel
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 🎯 Your Preferences")

    c1, c2, c3 = st.columns(3)
    with c1:
        taste = st.selectbox("Food Preference", ["Spicy", "Sweet", "Savory", "Healthy"])
        category = st.selectbox("Category", ["Food", "Drink"])
    with c2:
        budget = st.selectbox("Budget", ["Low", "Medium", "High"])
        cuisine = st.selectbox(
            "Cuisine",
            ["Desi", "Chinese", "Italian", "Continental", "Fast Food", "BBQ", "Street Food"],
        )
    with c3:
        health = st.selectbox(
            "Health Condition",
            ["No Restrictions", "Lactose Intolerant", "Diabetic Friendly",
             "High Protein (Gym)", "Low Calories", "Vegan"],
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Recommendation button
    btn_cols = st.columns([2, 1, 2])
    with btn_cols[1]:
        go = st.button("✨ Get Recommendations", key="recommend")

    if go:
        prefs = {
            "taste": taste, "budget": budget, "category": category,
            "cuisine": cuisine, "health": health,
        }
        results = recommend(prefs)
        st.balloons()
        st.success(
            f"Found {len(results)} matching {category.lower()} recommendations for {cuisine} cuisine! 🎉"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        # Responsive grid: 2 columns on desktop, stacks on mobile
        left, right = st.columns(2)
        for idx, item in enumerate(results):
            target = left if idx % 2 == 0 else right
            with target:
                render_card(item, idx)

    # Footer
    st.markdown(
        """
        <div class="app-footer">
            Your menu, upgraded. Your cravings, matched. ✨🍽️
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------- ENTRY POINT ----------------------------- #
def main():
    if not st.session_state.logged_in:
        auth_screen()
    else:
        main_app()


if __name__ == "__main__":
    main()
