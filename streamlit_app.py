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
# Track selected category for the list view
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

# Temp state for New Recipe
if 'new_rec_ingredients' not in st.session_state:
    st.session_state.new_rec_ingredients = []
if 'new_rec_name' not in st.session_state:
    st.session_state.new_rec_name = ""
if 'new_rec_desc' not in st.session_state:
    st.session_state.new_rec_desc = ""
if 'new_rec_cat' not in st.session_state:
    st.session_state.new_rec_cat = "Select a category"
# Temp state for ingredient input text
if 'ing_in' not in st.session_state:
    st.session_state.ing_in = ""

# --- EDIT MODE STATE ---
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'edit_temp_data' not in st.session_state:
    st.session_state.edit_temp_data = {}
if 'edit_ing_in' not in st.session_state:
    st.session_state.edit_ing_in = ""

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
    # Reset edit mode when navigating
    st.session_state.edit_mode = False
    st.rerun()

# -----------------------------------------------------------------------------
# 2. LOAD ASSETS (Base64)
# -----------------------------------------------------------------------------
# Note: Ensure these paths exist in your local folder or the images won't load.
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

    /* --- TOP NAV --- */
    .top-nav {{
        width: 100%;
        background-color: white;
        padding: 20px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 999;
        border-radius: 0px 0px 25px 25px;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .top-nav h1 {{
        margin: 0;
        font-family: 'Pixelify Sans', sans-serif;
        font-size: 32px;
        font-weight: 900;
        color: #FF9B00;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-align: center;
        width: 100%;
    }}
    .nav-spacer {{ height: 100px; }}

    /* --- BUTTONS & INPUTS --- */
    
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

    /* SELECTBOX STYLING */
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

    /* RECIPE CARD & CONTAINER STYLING */
    /* This targets st.container(border=True) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #FFFFFF !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1) !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        opacity: 1 !important;
    }}
    
    /* --- GENERAL BUTTON CENTERING & SIZING --- */
    .stButton {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}

    .stButton button {{
        background-color: white !important;
        color: #FF9B00 !important;
        border: 2px solid #FF9B00 !important;
        border-radius: 15px !important;
        
        /* Force Text/Icon Centering & Equal Height */
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0px 15px !important; 
        
        font-weight: 800 !important;
        transition: 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        margin: 0 auto;
    }}
    .stButton button:hover {{
        background-color: #e68900 !important;
        color: white !important;
        border-color: #e68900 !important;
        transform: translateY(-2px);
    }}
    
    /* SECONDARY (Delete/Cancel) Button Styling */
    .delete-btn button, .cancel-btn button {{
        background-color: #ff4757 !important;
        color: white !important;
        border-color: #ff4757 !important;
    }}
    .delete-btn button:hover, .cancel-btn button:hover {{
        background-color: #ff4757 !important;
        color: white !important;
    }}

    /* ALIGNMENT FIX FOR EDIT BUTTONS */
    .save-btn, .cancel-btn {{
        width: 100%;
        display: block;
    }}

    /* FOOTER ICONS */
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

    .footer-add button {{
        color: white !important;
        font-size: 16px !important;
        font-weight: 900 !important;
        background-color: #FF9B00 !important;
        border-radius: 30px !important;
        width: 140px !important;
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

    /* ANIMATIONS */
    .hop {{ animation: hop 1.5s infinite; }}
    @keyframes hop {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-20px); }}
    }}

    /* --- INGREDIENT REMOVAL BTN --- */
    .small-del-btn button {{
        background-color: white !important;
        color: #ff4757 !important;
        border: 2px solid #ff4757 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        padding: 2px 8px !important;
        height: auto !important;
        min-height: 0px !important;
        margin-top: 10px !important;
        border-radius: 10px !important;
        width: auto !important;
        box-shadow: none !important;
        display: inline-block !important;
    }}
    .small-del-btn button:hover {{
        background-color: #ff4757 !important;
        color: white !important;
        transform: none !important;
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
    
    with c1:
        st.markdown('<div class="footer-btn">', unsafe_allow_html=True)
        if st.button("Categories", key="nav_cat", use_container_width=True):
            navigate_to("categories")
        st.markdown('</div>', unsafe_allow_html=True)
            
    with c2:
        if st.session_state.page == 'home':
            st.markdown('<div class="footer-add">', unsafe_allow_html=True)
            if st.button("New Recipe", key="nav_add", use_container_width=True):
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
    img_html = f'<img src="data:image/png;base64,{egg_img}" class="hop" style="height:200px;">' if egg_img else '<div class="hop" style="font-size:150px;">🥚</div>'
    st.markdown(f"""
        <div style="height: 70vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 20px;">
            {img_html}
            <h1 style="color: white; font-family: 'Pixelify Sans'; font-size: 50px; margin-top: 30px; margin-left: 10px; text-shadow: 2px 2px 0px #000; text-align: center; width: 100%;">DISH DIARY</h1>
            <p style="color: white; letter-spacing: 2px; text-shadow: 1px 1px 0px #000; font-size: 18px;">CREATE, COOK, ENJOY</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 2, 1]) 
    with col:
        if st.button("Tap here to enter!", use_container_width=True):
            navigate_to("home")

# --- HOME ---
def page_home():
    render_top_nav("RECIPE LIST")
    
    if not st.session_state.recipes:
        st.markdown("""
            <div style="text-align: center; margin-top: 40%; padding: 20px; color: #FFE100; font-size: 20px; text-shadow: 1px 1px 10px rgba(0,0,0,0.5);">
                <p style="font-weight: 900; font-size: 30px;">No recipes yet!</p>
                <p>Tap the <b>+</b> button below to add one.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        for recipe in st.session_state.recipes:
            with st.container(border=True):
                st.markdown(f"""
                    <div style="font-weight:800; color: white; font-size:22px; line-height:1.2; margin-bottom:5px;">
                        {recipe['name']}
                    </div>
                    <div style="font-size:12px; color:#333; text-transform:uppercase; font-weight:700; background:#eee; padding:5px 10px; border-radius:10px; display:inline-block;">
                        {recipe['category']}
                    </div>
                """, unsafe_allow_html=True)
                
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
    
    # --- INPUT SECTION ---
    c1, c2 = st.columns([3.5, 1.5]) 
    
    # Callback only for the button
    def add_ing_callback():
        val = st.session_state.ing_in
        if val and val.strip():
            st.session_state.new_rec_ingredients.append(val.strip())
            st.session_state.ing_in = "" # Clear input
    
    with c1:
        st.text_input("Ing", label_visibility="collapsed", placeholder="Add Item", key="ing_in")

    with c2:
        st.button("➕", key="add_ing_btn", use_container_width=True, on_click=add_ing_callback)

    # --- INGREDIENT LIST (GRID LAYOUT) ---
    if st.session_state.new_rec_ingredients:
        st.write("")
        st.markdown(f"<div style='font-size:14px; color:#555; margin-bottom:10px;'>{len(st.session_state.new_rec_ingredients)} items added:</div>", unsafe_allow_html=True)
        
        def remove_ing(idx_to_remove):
            st.session_state.new_rec_ingredients.pop(idx_to_remove)

        items = st.session_state.new_rec_ingredients
        
        # Grid: 3 columns per row
        for i in range(0, len(items), 3):
            cols = st.columns(3)
            batch = items[i:i+3]
            for j, ingredient in enumerate(batch):
                actual_index = i + j
                with cols[j]:
                    st.markdown(f"""
                        <div style='
                            background-color: #FF9B00; 
                            color: white; 
                            padding: 8px 5px; 
                            border-radius: 15px; 
                            text-align: center; 
                            font-weight: 700; 
                            font-size: 16px; 
                            line-height: 1.2;
                            min-height: 40px;
                            display: flex; 
                            align-items: center; 
                            justify-content: center;
                        '>
                            {ingredient}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="small-del-btn" style="text-align:center;">', unsafe_allow_html=True)
                    if st.button("Remove", key=f"del_ing_{actual_index}"):
                        remove_ing(actual_index)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.write("") 

        if st.button("Clear All Ingredients"):
            st.session_state.new_rec_ingredients = []
            st.rerun()
    
    st.write("")

    st.markdown("**Instructions**")
    st.session_state.new_rec_desc = st.text_area("Desc", label_visibility="collapsed", value=st.session_state.new_rec_desc, height=120, placeholder="Steps...")
    st.write("")

    is_fav = st.checkbox("Add to Favorites ❤️")
    st.write("")

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
                st.session_state.new_rec_ingredients = []
                st.session_state.new_rec_name = ""
                st.session_state.new_rec_desc = ""
                st.session_state.new_rec_cat = "Select a category"
                navigate_to("home")
            else:
                st.markdown(f"""
                <div style="background-color:white; color:#FF9B00; font-weight:700; padding:10px; border-radius:10px; text-align:center; margin-top:10px; box-shadow:0 4px 6px rgba(0,0,0,0.1); border:2px solid #FF9B00;">
                    Missing Name or Category
                </div>
                """, unsafe_allow_html=True)

    render_bottom_nav()

# --- CATEGORIES SELECTION ---
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
        cat_img_b64 = get_img_as_base64(f"assets/categories/{img_file}")
        
        img_tag = f'<img src="data:image/png;base64,{cat_img_b64}" style="width:40px; height:40px; margin-top:5px;">' if cat_img_b64 else "<span>❓</span>"

        # UPDATED: Use st.container(border=True) to create the white card background
        with st.container(border=True):
            # Try to vertical align if Streamlit version supports it, else standard
            try:
                c_icon, c_btn = st.columns([1, 4], vertical_alignment="center")
            except TypeError:
                c_icon, c_btn = st.columns([1, 4])
            
            with c_icon:
                st.markdown(f"<div style='text-align:center;'>{img_tag}</div>", unsafe_allow_html=True)
            
            with c_btn:
                # The button acts as the click target for the category
                if st.button(f"{cat_name} ({count})", key=f"cat_btn_{cat_name}", use_container_width=True):
                    st.session_state.selected_category = cat_name
                    navigate_to("category_list")

    render_bottom_nav()

# --- CATEGORY LIST (NEW PAGE) ---
def page_category_list():
    selected_cat = st.session_state.selected_category
    render_top_nav(selected_cat.upper())
    
    # Back Button
    if st.button("⬅️ Back to Categories"):
        navigate_to("categories")
    
    st.write("")
    
    # Filter recipes
    cat_recipes = [r for r in st.session_state.recipes if r['category'] == selected_cat]

    if not cat_recipes:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 30%; color: #FFE100; text-shadow: 1px 1px 10px rgba(0,0,0,0.5); padding: 20px;">
                <p style="font-weight: 900; font-size: 25px;">No {selected_cat} recipes yet!</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        for recipe in cat_recipes:
            with st.container(border=True):
                st.markdown(f"""
                    <div style="font-weight:800; color: white; font-size:22px; line-height:1.2; margin-bottom:5px;">
                        {recipe['name']}
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("") 
                
                c_view, c_fav = st.columns([1, 1])
                with c_view:
                    if st.button("View", key=f"cat_view_{recipe['id']}", use_container_width=True):
                        navigate_to("details", recipe['id'])
                with c_fav:
                    fav_icon = "❤️" if recipe['fav'] else "🤍"
                    if st.button(fav_icon, key=f"cat_fav_{recipe['id']}", use_container_width=True):
                        recipe['fav'] = not recipe['fav']
                        st.rerun()

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
                    <div style="font-weight:800; color: white; font-size:22px; line-height:1.2; margin-bottom:5px;">
                        {r['name']}
                    </div>
                    <div style="font-size:12px; color:#333; text-transform:uppercase; font-weight:700; background:#eee; padding:5px 10px; border-radius:10px; display:inline-block;">
                        {r['category']}
                    </div>
                """, unsafe_allow_html=True)
                
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

# --- DETAILS (UPDATED WITH ALIGNED BUTTONS) ---
def page_details():
    # Find recipe
    rec = next((r for r in st.session_state.recipes if r['id'] == st.session_state.selected_recipe_id), None)
    
    if not rec:
        st.error("Recipe not found.")
        if st.button("Back"): navigate_to("home")
        return

    # --- TOP ROW ---
    c_back, c_edit, c_fav = st.columns([1, 2, 1])
    
    with c_back:
        if st.button("⬅️"): navigate_to("home")
    
    with c_edit:
        if not st.session_state.edit_mode:
            if st.button("✏️ Edit Recipe", use_container_width=True):
                st.session_state.edit_mode = True
                st.session_state.edit_temp_data = {
                    "name": rec['name'],
                    "category": rec['category'],
                    "ingredients": rec['ingredients'].copy(),
                    "desc": rec['desc']
                }
                st.rerun()

    with c_fav:
        if not st.session_state.edit_mode:
            icon = "❤️" if rec['fav'] else "🤍"
            if st.button(icon, key="det_fav"):
                rec['fav'] = not rec['fav']
                st.rerun()

    st.write("")

    # ==========================
    #      EDIT MODE VIEW
    # ==========================
    if st.session_state.edit_mode:
        
        # 1. Name Edit
        st.markdown("**Recipe Name**")
        st.session_state.edit_temp_data['name'] = st.text_input("Name", value=st.session_state.edit_temp_data['name'], label_visibility="collapsed")
        st.write("")

        # 2. Category Edit
        st.markdown("**Category**")
        cat_options = ["Select a category", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert", "Drinks"]
        try:
            curr_idx = cat_options.index(st.session_state.edit_temp_data['category'])
        except: curr_idx = 0
        st.session_state.edit_temp_data['category'] = st.selectbox("Category", options=cat_options, index=curr_idx, label_visibility="collapsed")
        st.write("")

        # 3. Ingredients Edit
        st.markdown("**Ingredients**")
        
        # Add Input
        c_in, c_btn = st.columns([3.5, 1.5])
        def add_edit_ing():
            val = st.session_state.edit_ing_in
            if val and val.strip():
                st.session_state.edit_temp_data['ingredients'].append(val.strip())
                st.session_state.edit_ing_in = ""

        with c_in:
            st.text_input("New Ingredient", key="edit_ing_in", label_visibility="collapsed", placeholder="Add item")
        with c_btn:
            st.button("➕", key="edit_add_btn", use_container_width=True, on_click=add_edit_ing)

        # Ingredient List
        temp_ings = st.session_state.edit_temp_data['ingredients']
        if temp_ings:
            st.write("")
            for i in range(0, len(temp_ings), 3):
                cols = st.columns(3)
                batch = temp_ings[i:i+3]
                for j, item in enumerate(batch):
                    actual_idx = i + j
                    with cols[j]:
                        st.markdown(f"""
                        <div style='background-color: #FF9B00; color: white; padding: 8px 5px; border-radius: 15px; text-align: center; font-weight: 700; font-size: 16px; min-height: 40px; display: flex; align-items: center; justify-content: center;'>
                            {item}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown('<div class="small-del-btn" style="text-align:center;">', unsafe_allow_html=True)
                        if st.button("Remove", key=f"edit_rem_{actual_idx}"):
                            st.session_state.edit_temp_data['ingredients'].pop(actual_idx)
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.write("")

        st.write("")

        # 4. Instructions Edit
        st.markdown("**Instructions**")
        st.session_state.edit_temp_data['desc'] = st.text_area("Instructions", value=st.session_state.edit_temp_data['desc'], label_visibility="collapsed", height=150)
        st.write("")

        # SAVE / CANCEL BUTTONS
        col_save, col_cancel = st.columns(2)
        with col_save:
            st.markdown('<div class="save-btn">', unsafe_allow_html=True)
            if st.button("💾 Save Changes", type="primary", use_container_width=True):
                rec['name'] = st.session_state.edit_temp_data['name']
                rec['category'] = st.session_state.edit_temp_data['category']
                rec['ingredients'] = st.session_state.edit_temp_data['ingredients']
                rec['desc'] = st.session_state.edit_temp_data['desc']
                
                st.session_state.edit_mode = False
                st.success("Recipe Updated!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_cancel:
            st.markdown('<div class="cancel-btn">', unsafe_allow_html=True)
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.edit_mode = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================
    #      READ-ONLY VIEW
    # ==========================
    else:
        st.markdown(f"<h2 style='text-align:center; color:white; margin:0; text-shadow:1px 1px 2px black;'>{rec['name']}</h2>", unsafe_allow_html=True)
        st.write("")
        
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
        else:
             st.info("No ingredients listed.")
        
        st.write("")
        st.markdown("<h3 style='color:white; text-shadow:1px 1px 2px black;'>Instructions</h3>", unsafe_allow_html=True)
        if rec['desc']:
            st.markdown(f"<div style='background:rgba(255,255,255,0.9); padding:15px; border-radius:15px; color:#333; line-height:1.6;'>{rec['desc']}</div>", unsafe_allow_html=True)
        else:
             st.info("No instructions listed.")

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
elif st.session_state.page == 'category_list': page_category_list() # NEW PAGE
elif st.session_state.page == 'favorites': page_favorites()
elif st.session_state.page == 'new_recipe': page_new_recipe()
elif st.session_state.page == 'details': page_details()
