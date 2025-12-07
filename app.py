import streamlit as st
import base64
import os
import uuid
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. SETUP & SESSION STATE
# -----------------------------------------------------------------------------

st.set_page_config(page_title="DishDiary", page_icon="🍳", layout="centered")

# --- STATE INITIALIZATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome' 
if 'recipes' not in st.session_state:
    st.session_state.recipes = [] 
if 'selected_recipe_id' not in st.session_state:
    st.session_state.selected_recipe_id = None

# Temp state for New Recipe
if 'new_rec_ingredients' not in st.session_state:
    st.session_state.new_rec_ingredients = []
if 'new_rec_name' not in st.session_state:
    st.session_state.new_rec_name = ""
if 'new_rec_desc' not in st.session_state:
    st.session_state.new_rec_desc = ""
if 'new_rec_cat' not in st.session_state:
    st.session_state.new_rec_cat = "Select a category"

# Helper to load image as base64
def get_img_as_base64(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Navigation Function
def navigate_to(page_name, recipe_id=None):
    st.session_state.page = page_name
    if recipe_id:
        st.session_state.selected_recipe_id = recipe_id
    st.rerun()

# -----------------------------------------------------------------------------
# 2. LOAD ASSETS (Base64)
# -----------------------------------------------------------------------------
egg_img = get_img_as_base64("assets/Egg.png")
icon_cat = get_img_as_base64("assets/Categories Icon.png")
icon_heart_r = get_img_as_base64("assets/Heart R.png")
icon_heart_w = get_img_as_base64("assets/Heart W.png")
icon_house = get_img_as_base64("assets/house.png")

# -----------------------------------------------------------------------------
# 3. CSS STYLING
# -----------------------------------------------------------------------------

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans&display=swap');

    /* GLOBAL */
    * {{ font-family: 'Poppins', sans-serif; }}
    
    .stApp {{
        background-image: linear-gradient(to bottom, #FFE100, #FF9B00);
        background-attachment: fixed;
    }}

    /* CONTAINER LIMIT */
    .block-container {{
        max-width: 500px;
        padding-top: 1rem;
        padding-bottom: 8rem;
        margin: auto;
    }}

    /* HIDE DEFAULTS */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}

    /* TOP NAV */
    .top-nav {{
        width: 100%;
        background-color: white;
        padding: 20px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999;
        text-align: center;
        border-radius: 0px 0px 25px 25px;
    }}
    .top-nav h1 {{
        margin: 0;
        font-family: 'Pixelify Sans', sans-serif;
        font-size: 32px;
        font-weight: 900;
        color: #FF9B00;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    .nav-spacer {{ height: 100px; }}

    /* --- INPUTS & SELECTBOX FIXES --- */
    
    .stTextInput input, .stTextArea textarea {{
        background-color: white !important;
        color: black !important;
        border: 2px solid #FF9B00 !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }}
    ::placeholder {{
        color: #888 !important;
        opacity: 1;
    }}

    div[data-baseweb="select"] {{
        background-color: white !important;
        border: 2px solid #FF9B00 !important;
        border-radius: 12px !important;
    }}
    
    div[data-baseweb="select"] > div {{
        background-color: transparent !important;
        color: black !important;
    }}
    div[data-baseweb="select"] span {{
        color: black !important;
    }}
    
    div[data-baseweb="select"] svg {{
        fill: #FF9B00 !important;
    }}

    ul[data-baseweb="menu"] {{
        background-color: white !important;
    }}
    ul[data-baseweb="menu"] li {{
        background-color: white !important;
        color: black !important;
    }}
    ul[data-baseweb="menu"] li:hover {{
        background-color: #FFF4E0 !important;
    }}
    
    /* -------------------------------- */

    /* RECIPE CARD CONTAINER - FORCED WHITE BACKGROUND */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #FFFFFF !important; /* Explicit White */
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1) !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        opacity: 1 !important;
    }}
    
    /* BUTTONS: WHITE FILL, ORANGE TEXT */
    .stButton button {{
        background-color: white !important;
        color: #FF9B00 !important;
        border: 2px solid #FF9B00 !important;
        border-radius: 15px !important;
        padding: 10px 15px !important;
        font-weight: 800 !important;
        transition: 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }}
    .stButton button:hover {{
        background-color: #e68900 !important;
        color: white !important;
        border-color: #e68900 !important;
        transform: translateY(-2px);
    }}
    
    /* SECONDARY (Delete) Button */
    .delete-btn button {{
        background-color: #ff4757 !important;
        color: white !important;
        border-color: #ff4757 !important;
    }}
    .delete-btn button:hover {{
        background-color: #ff4757 !important;
        color: white !important;
    }}

    /* FOOTER ICONS */
    
    /* Left: Categories */
    div[data-testid="column"]:nth-of-type(1) .footer-btn button {{
        background-image: url("data:image/png;base64,{icon_cat}");
        background-size: 30px;
        background-repeat: no-repeat;
        background-position: center;
        color: transparent !important;
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }}
    div[data-testid="column"]:nth-of-type(1) .footer-btn button:hover {{ transform: scale(1.1); background-color: transparent !important; }}

    /* Right: Favorites */
    div[data-testid="column"]:nth-of-type(3) .footer-btn button {{
        background-image: url("data:image/png;base64,{icon_heart_r}");
        background-size: 30px;
        background-repeat: no-repeat;
        background-position: center;
        color: transparent !important;
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }}
    div[data-testid="column"]:nth-of-type(3) .footer-btn button:hover {{ transform: scale(1.1); background-color: transparent !important; }}

    /* Middle: Home */
    .footer-home button {{
        background-image: url("data:image/png;base64,{icon_house}");
        background-size: 35px;
        background-repeat: no-repeat;
        background-position: center;
        color: transparent !important;
        background-color: #FF9B00 !important;
        border-radius: 50% !important;
        width: 60px !important; height: 60px !important;
        border: 4px solid white !important;
        box-shadow: 0 -5px 10px rgba(0,0,0,0.1) !important;
        display: block; margin: 0 auto;
        transform: translateY(-20px);
    }}
    .footer-home button:hover {{ transform: translateY(-25px) scale(1.05); }}

    /* Middle: New Recipe */
    .footer-add button {{
        color: white !important;
        font-size: 16px !important;
        font-weight: 900 !important; /* Bold */
        background-color: #FF9B00 !important;
        border-radius: 30px !important; /* Pill shape */
        width: 140px !important; /* Wider for text */
        height: 60px !important;
        border: 4px solid white !important;
        box-shadow: 0 -5px 10px rgba(0,0,0,0.1) !important;
        display: block; margin: 0 auto;
        transform: translateY(-20px);
        padding: 0 !important;
    }}
    .footer-add button:hover {{ 
        transform: translateY(-25px) scale(1.05);
        color: white !important;
        background-color: #e68900 !important;
    }}

    /* TAGS */
    .tag {{
        background: white; color: #FF9B00; padding: 6px 12px;
        border-radius: 20px; font-size: 14px; font-weight: 600;
        border: 2px solid #FF9B00; margin-right: 5px; display: inline-block; margin-bottom: 5px;
    }}

    /* CATEGORY LIST ITEM */
    .category-item {{
        background: white; 
        border-radius: 20px; 
        padding: 20px 25px; /* Increased Padding */
        margin-bottom: 15px; 
        display: flex; 
        align-items: center;
        justify-content: space-between; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        cursor: pointer;
        width: 100%;
    }}
    .category-item:hover {{ transform: scale(1.02); }}

    /* ANIMATIONS */
    .hop {{ animation: hop 1.5s infinite; }}
    @keyframes hop {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-20px); }}
    }}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. COMPONENTS
# -----------------------------------------------------------------------------

def render_top_nav(title):
    st.markdown(f"""
        <div class="top-nav">
            <h1>{title}</h1>
        </div>
        <div class="nav-spacer"></div>
    """, unsafe_allow_html=True)

def render_bottom_nav():
    st.write("")
    st.write("")
    st.markdown("---") 
    
    c1, c2, c3 = st.columns([1, 1, 1])
    
    # 1. Categories Button
    with c1:
        st.markdown('<div class="footer-btn">', unsafe_allow_html=True)
        if st.button("Categories", key="nav_cat", use_container_width=True):
            navigate_to("categories")
        st.markdown('</div>', unsafe_allow_html=True)
            
    # 2. Middle Button
    with c2:
        if st.session_state.page == 'home':
            st.markdown('<div class="footer-add">', unsafe_allow_html=True)
            if st.button("New Recipe", key="nav_add", use_container_width=True):
                # Reset
                st.session_state.new_rec_ingredients = []
                st.session_state.new_rec_name = ""
                st.session_state.new_rec_desc = ""
                st.session_state.new_rec_cat = "Select a category"
                navigate_to("new_recipe")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="footer-home">', unsafe_allow_html=True)
            if st.button("Home", key="nav_home", use_container_width=True):
                navigate_to("home")
            st.markdown('</div>', unsafe_allow_html=True)

    # 3. Favorites Button
    with c3:
        st.markdown('<div class="footer-btn">', unsafe_allow_html=True)
        if st.button("Favorites", key="nav_fav", use_container_width=True):
            navigate_to("favorites")
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. PAGES
# -----------------------------------------------------------------------------

# --- WELCOME ---
def page_welcome():
    # Use the Egg pixel art
    img_html = f'<img src="data:image/png;base64,{egg_img}" class="hop" style="height:200px;">' if egg_img else '<div class="hop" style="font-size:150px;">🥚</div>'

    st.markdown(f"""
        <div style="height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 20px;">
            {img_html}
            <h1 style="color: white; font-family: 'Pixelify Sans'; font-size: 50px; margin-top: 30px; text-shadow: 2px 2px 0px #000; text-align: center; width: 100%;">DISH DIARY</h1>
            <p style="color: white; letter-spacing: 2px; text-shadow: 1px 1px 0px #000; font-size: 18px;">CREATE, COOK, ENJOY</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Use 3 equal columns to center the middle one perfectly
    _, col, _ = st.columns([1, 1, 1]) 
    with col:
        if st.button("Tap here to enter!"):
            navigate_to("home")

# --- HOME ---
def page_home():
    render_top_nav("MY RECIPE LIST")
    
    if not st.session_state.recipes:
        st.markdown("""
            <div style="text-align: center; margin-top: 40%; padding: 20px; color: #FFE100; font-size: 20px; text-shadow: 1px 1px 10px rgba(0,0,0,0.5);">
                <p style="font-weight: 900; font-size: 30px;">No recipes yet!</p>
                <p>Tap the <b>+</b> button below to add one.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        for recipe in st.session_state.recipes:
            # Single White Box
            with st.container(border=True):
                st.markdown(f"""
                    <div style="font-weight:800; color: white; font-size:22px; line-height:1.2; margin-bottom:5px;">
                        {recipe['name']}
                    </div>
                    <div style="font-size:12px; color:#333; text-transform:uppercase; font-weight:700; background:#eee; padding:5px 10px; border-radius:10px; display:inline-block;">
                        {recipe['category']}
                    </div>
                """, unsafe_allow_html=True)
                
                # ADDED SPACER HERE FOR MARGIN
                st.write("") 
                
                c_view, c_fav = st.columns([1, 1])
                with c_view:
                    if st.button("View", key=f"view_{recipe['id']}", use_container_width=True):
                        navigate_to("details", recipe['id'])
                with c_fav:
                    fav_icon = "❤️" if recipe['fav'] else "🤍"
                    if st.button(fav_icon, key=f"fav_{recipe['id']}", use_container_width=True):
                        recipe['fav'] = not recipe['fav']
                        st.rerun()

    render_bottom_nav()

# --- NEW RECIPE ---
def page_new_recipe():
    render_top_nav("NEW RECIPE")
    st.write("") 

    st.markdown("**Recipe Name**")
    st.session_state.new_rec_name = st.text_input("Name", label_visibility="collapsed", value=st.session_state.new_rec_name, placeholder="e.g. Chocolate Cake")
    st.write("")

    st.markdown("**Category**")
    cat_options = ["Select a category", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert", "Drinks"]
    try:
        idx = cat_options.index(st.session_state.new_rec_cat)
    except: idx = 0
    st.session_state.new_rec_cat = st.selectbox("Cat", options=cat_options, index=idx, label_visibility="collapsed")
    st.write("")

    st.markdown("**Ingredients**")
    # CHANGED: 3.5 to 1.5 gives more space to button, less to input
    c1, c2 = st.columns([3.5, 1.5]) 
    with c1:
        new_ing = st.text_input("Ing", label_visibility="collapsed", placeholder="Add Item", key="ing_in")
    with c2:
        # CHANGED: Added use_container_width=True to make button fill the column
        if st.button("➕", key="add_ing", use_container_width=True):
            if new_ing:
                st.session_state.new_rec_ingredients.append(new_ing)
                st.rerun()

    if st.session_state.new_rec_ingredients:
        st.markdown('<div>', unsafe_allow_html=True)
        for ing in st.session_state.new_rec_ingredients:
             st.markdown(f'<span class="tag">{ing}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Clear Ingredients"):
            st.session_state.new_rec_ingredients = []
            st.rerun()
    
    st.write("")

    st.markdown("**Instructions**")
    st.session_state.new_rec_desc = st.text_area("Desc", label_visibility="collapsed", value=st.session_state.new_rec_desc, height=120, placeholder="Steps...")
    st.write("")

    is_fav = st.checkbox("Add to Favorites ❤️")
    st.write("")

    # Use 3 equal columns to center the middle button
    c_left, c_mid, c_right = st.columns([1, 1, 1])
    with c_mid:
        if st.button("DONE", type="primary", use_container_width=True):
            if st.session_state.new_rec_name and st.session_state.new_rec_cat != "Select a category":
                new_entry = {
                    "id": str(uuid.uuid4()),
                    "name": st.session_state.new_rec_name,
                    "category": st.session_state.new_rec_cat,
                    "ingredients": st.session_state.new_rec_ingredients,
                    "desc": st.session_state.new_rec_desc,
                    "fav": is_fav,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.recipes.append(new_entry)
                st.success("Saved!")
                navigate_to("home")
            else:
                # Custom WHITE Box for Error
                st.markdown(f"""
                <div style="
                    background-color: white;
                    color: #FF9B00;
                    font-weight: 700;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    margin-top: 10px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    border: 2px solid #FF9B00;
                ">
                    Missing Name or Category
                </div>
                """, unsafe_allow_html=True)

    render_bottom_nav()

# --- CATEGORIES ---
def page_categories():
    render_top_nav("CATEGORIES")
    st.write("")

    cats = [
        ("Breakfast", "pancake.png"), 
        ("Lunch", "rice bowl.png"), 
        ("Dinner", "soup.png"),
        ("Snack", "donut.png"), 
        ("Dessert", "cake.png"), 
        ("Drinks", "coffee.png")
    ]
    
    for cat_name, img_file in cats:
        count = sum(1 for r in st.session_state.recipes if r['category'] == cat_name)
        
        # Load the specific pixel icon
        cat_img_b64 = get_img_as_base64(f"assets/categories/{img_file}")
        if cat_img_b64:
             img_tag = f'<img src="data:image/png;base64,{cat_img_b64}" style="width:40px; height:40px;">'
        else:
             img_tag = "<span>❓</span>"

        # Using HTML directly to control layout (Flexbox)
        st.markdown(f"""
        <div class="category-item">
            <div style="display:flex; align-items:center; gap:20px; flex-grow:1;">
                {img_tag}
                <span style="font-weight:800; color:#FF9B00; font-size:22px; white-space:nowrap;">{cat_name}</span>
            </div>
            <span style="color:#888; font-weight:600; font-size:18px;">{count}</span>
        </div>
        """, unsafe_allow_html=True)

    render_bottom_nav()

# --- FAVORITES ---
def page_favorites():
    render_top_nav("FAVORITES")
    
    faves = [r for r in st.session_state.recipes if r['fav']]
    
    if not faves:
         st.markdown("""
            <div style="text-align: center; margin-top: 30%; color: #FFE100; text-shadow: 1px 1px 10px rgba(0,0,0,0.5); padding: 20px; font-size: 23px;">
                <p style="font-weight: 900; font-size: 30px;">No favorites yet!</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        for r in faves:
            with st.container(border=True):
                st.markdown(f"""
                    <div style="font-weight:800; color:#FF9B00; font-size:22px; line-height:1.2; margin-bottom:5px;">
                        {r['name']}
                    </div>
                    <div style="font-size:12px; color:#333; text-transform:uppercase; font-weight:700; background:#eee; padding:5px 10px; border-radius:10px; display:inline-block;">
                        {r['category']}
                    </div>
                """, unsafe_allow_html=True)
                
                # ADDED SPACER HERE FOR MARGIN
                st.write("") 
                
                c_view, c_unfav = st.columns([1, 1])
                with c_view:
                    if st.button("View", key=f"fav_view_{r['id']}", use_container_width=True):
                        navigate_to("details", r['id'])
                with c_unfav:
                    if st.button("💔", key=f"unfav_{r['id']}", use_container_width=True):
                        r['fav'] = False
                        st.rerun()

    render_bottom_nav()

# --- DETAILS ---
def page_details():
    rec = next((r for r in st.session_state.recipes if r['id'] == st.session_state.selected_recipe_id), None)
    if not rec:
        st.error("Recipe not found.")
        if st.button("Back"): navigate_to("home")
        return

    c_back, c_title, c_fav = st.columns([1, 4, 1])
    with c_back:
        if st.button("⬅️"): navigate_to("home")
    with c_title:
        st.markdown(f"<h2 style='text-align:center; color:white; margin:0; text-shadow:1px 1px 2px black;'>{rec['name']}</h2>", unsafe_allow_html=True)
    with c_fav:
        # Toggle icon
        icon = "❤️" if rec['fav'] else "🤍"
        if st.button(icon, key="det_fav"):
            rec['fav'] = not rec['fav']
            st.rerun()

    st.write("")
    
    # Metadata
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; border-bottom:2px solid white; padding-bottom:10px; margin-bottom:20px;">
        <span style="background:white; color:#FF9B00; padding:5px 15px; border-radius:15px; font-weight:800;">{rec['category']}</span>
        <span style="color:white; font-weight:600;">{rec['date']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color:white; text-shadow:1px 1px 2px black;'>Ingredients</h3>", unsafe_allow_html=True)
    if rec['ingredients']:
        for ing in rec['ingredients']:
            st.markdown(f"<div style='background:rgba(255,255,255,0.9); padding:10px; border-radius:10px; margin-bottom:5px; color:#333; font-weight:600;'>🥗 {ing}</div>", unsafe_allow_html=True)
    
    st.write("")
    st.markdown("<h3 style='color:white; text-shadow:1px 1px 2px black;'>Instructions</h3>", unsafe_allow_html=True)
    if rec['desc']:
        st.markdown(f"<div style='background:rgba(255,255,255,0.9); padding:15px; border-radius:15px; color:#333; line-height:1.6;'>{rec['desc']}</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("---")
    
    if "confirm_delete" not in st.session_state: st.session_state.confirm_delete = False
    
    if not st.session_state.confirm_delete:
        st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
        if st.button("🗑️ Delete Recipe"):
            st.session_state.confirm_delete = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Delete this recipe?")
        c1, c2 = st.columns(2)
        if c1.button("Yes"):
            st.session_state.recipes = [r for r in st.session_state.recipes if r['id'] != rec['id']]
            st.session_state.confirm_delete = False
            navigate_to("home")
        if c2.button("No"):
            st.session_state.confirm_delete = False
            st.rerun()

    render_bottom_nav()

# -----------------------------------------------------------------------------
# 6. ROUTER
# -----------------------------------------------------------------------------
if st.session_state.page == 'welcome': page_welcome()
elif st.session_state.page == 'home': page_home()
elif st.session_state.page == 'categories': page_categories()
elif st.session_state.page == 'favorites': page_favorites()
elif st.session_state.page == 'new_recipe': page_new_recipe()
elif st.session_state.page == 'details': page_details()