import streamlit as st
import pandas as pd

# --- Mappings ---
country_region_map = {
    "BRA": "Latin America",
    "TWN": "Asia",
    "MYS": "Asia",
    "FRA": "Europe",
    "ITA": "Europe",
}
country_map = {
    "BRA": "Brazil",
    "TWN": "Taiwan",
    "MYS": "Malaysia",
    "FRA": "France",
    "ITA": "Italy",
}
# Chanel email to Alias mapping (for test/demo)
mail_alias_map = {
    "jean.dupont@chanel.com": "alanjapai",
    "sarah.martin@chanel.com": "aramuz",
    "paul.laurent@chanel.com": "arscine",
    "chloe.bernard@chanel.com": "galipand",
    "tom.elmaleh@chanel.com": "tomel"
}

columns = ["BI", "Environment", "Code Sector", "Code Country", "Alias", "Country", "Chanel Email", "Sector"]
sample_data = [
    {
        "BI": "CERP",
        "Environment": "Production",
        "Code Sector": "EUROPE",
        "Code Country": "FRA",
        "Alias": "global/alanjapai",
        "Country": "France",
        "Chanel Email": "jean.dupont@chanel.com",
        "Sector": "Europe"
    },
    {
        "BI": "Sales & Stocks",
        "Environment": "Test",
        "Code Sector": "ASIA",
        "Code Country": "MYS",
        "Alias": "global/arscine",
        "Country": "Malaysia",
        "Chanel Email": "paul.laurent@chanel.com",
        "Sector": "Asia"
    },
    {
        "BI": "Ultimate",
        "Environment": "Production",
        "Code Sector": "LATIN AMERICA",
        "Code Country": "BRA",
        "Alias": "global/galipand",
        "Country": "Brazil",
        "Chanel Email": "chloe.bernard@chanel.com",
        "Sector": "Latin America"
    },
    {
        "BI": "Aftersales",
        "Environment": "Production",
        "Code Sector": "ASIA",
        "Code Country": "*",
        "Alias": "global/aramuz",
        "Country": "*",
        "Chanel Email": "sarah.martin@chanel.com",
        "Sector": "Asia"
    }
]
df = pd.DataFrame(sample_data, columns=columns)

st.set_page_config(page_title="WFJ-BI Access Management", layout="wide")
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #101010;
        color: #fff;
        border: none;
        border-radius:8px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        font-size: 1rem;
        transition: background 0.2s;
    }
    div.stButton > button:first-child:hover {
        background-color: #232323;
        color: #fff;
    }
    .form-box {
        max-width: 480px;
        margin-left: auto;
        margin-right: auto;
        padding: 2em 2em 1.5em 2em;
        background: #fff;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .form-box .stTextInput, .form-box .stSelectbox, .form-box .stButton, .form-box .stRadio, .form-box .stMarkdown {
        max-width: 360px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.image("chanel.png", width=250)
st.title("WFJ-BI Access Management")

if "show_form" not in st.session_state:
    st.session_state["show_form"] = False

def toggle_form():
    st.session_state["show_form"] = not st.session_state["show_form"]

st.button(
    "Add a member",
    on_click=toggle_form,
    key="add_member_btn",
    help="Click to grant BI access to a new user",
)

if st.session_state["show_form"]:
    with st.container():
        st.markdown('<div class="form-box">', unsafe_allow_html=True)
        st.markdown("### Grant access to a new member")

        # 1. BI selection
        bi_choice = st.selectbox(
            "Select the BI application",
            ["CERP", "Ultimate", "Sales & Stocks", "Aftersales", "Topaze"],
            key="bi_choice"
        )

        # 2. Environment
        env_choice = st.selectbox(
            "Environment",
            ["Production", "Test"],
            key="env_choice"
        )

        # 3. Email and alias
        email = st.text_input("Chanel Email*", key="email_chanel")
        alias_suggestion = mail_alias_map.get(email.strip().lower(), email.split("@")[0] if "@" in email else "")
        st.markdown(
            f"""
            <div style="
                background-color: #fafbfc;
                color: #b0b5ba;
                padding: 0.5em 1em;
                border-radius: 6px;
                border: 1px solid #e6e6e6;
                margin-bottom: 1em;
                font-size: 1rem;
                ">
                <b>Detected alias:</b> {alias_suggestion}
            </div>
            """,
            unsafe_allow_html=True
        )

        # 4. Access type
        access_type = st.selectbox(
            "Access type",
            ["By country", "By sector", "Keyusers"],
            key="access_type"
        )

        code_country = None
        sector_value = None
        country_value = None

        if access_type == "By country":
            country_selected = st.selectbox("Country*", sorted(country_map.values()), key="country_select")
            sector_value = ""
            if country_selected:
                code_country = [k for k, v in country_map.items() if v == country_selected][0]
                sector_value = country_region_map.get(code_country, "")
                country_value = country_selected
            st.markdown(
                f"""
                <div style="
                    background-color: #fafbfc;
                    color: #b0b5ba;
                    padding: 0.5em 1em;
                    border-radius: 6px;
                    border: 1px solid #e6e6e6;
                    margin-bottom: 1em;
                    font-size: 1rem;
                    ">
                    <b>Detected sector:</b> {sector_value}
                </div>
                """,
                unsafe_allow_html=True
            )
        elif access_type == "By sector":
            sector_value = st.selectbox("Sector*", sorted(set(country_region_map.values())), key="sector_select")
            st.text_input("Country*", value="*", disabled=True, key="country_star")
            code_country = "*"
            country_value = "*"
        elif access_type == "Keyusers":
            st.text_input("Sector*", value="*", disabled=True, key="sector_keyuser")
            st.text_input("Country*", value="*", disabled=True, key="country_keyuser")
            sector_value = "*"
            code_country = "*"
            country_value = "*"

        ready = (
            email and alias_suggestion and bi_choice and env_choice and access_type and (
                (access_type == "By country" and country_value)
                or (access_type == "By sector" and sector_value)
                or (access_type == "Keyusers")
            )
        )

        if st.button("Add", disabled=not ready, key="btn_add"):
            code_sector = sector_value.upper() if sector_value and sector_value != "*" else "*"
            new_row = {
                "BI": bi_choice,
                "Environment": env_choice,
                "Code Sector": code_sector,
                "Code Country": code_country,
                "Alias": alias_suggestion,
                "Country": country_value,
                "Chanel Email": email,
                "Sector": sector_value
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Access granted to {email} ({alias_suggestion}) on {bi_choice} [{env_choice}] for {sector_value}/{country_value}")

        st.markdown('</div>', unsafe_allow_html=True)

# --- Remove access (with button) ---
if "show_delete" not in st.session_state:
    st.session_state["show_delete"] = False

def toggle_delete():
    st.session_state["show_delete"] = not st.session_state["show_delete"]

st.button(
    "Remove access for a member",
    on_click=toggle_delete,
    key="toggle_delete_btn"
)

if st.session_state["show_delete"]:
    with st.container():
        st.markdown('<div class="form-box">', unsafe_allow_html=True)
        st.markdown("### Remove all accesses for a member")
        email_supp = st.text_input("Chanel Email to remove*", key="supp_email")
        alias_supp = mail_alias_map.get(email_supp.strip().lower(), email_supp.split("@")[0] if "@" in email_supp else "")

        if email_supp:
            rows_to_remove = df[df["Chanel Email"] == email_supp]
            if not rows_to_remove.empty:
                st.markdown(
                    f"<b>Detected alias:</b> {alias_supp}<br><b>Found accesses:</b>",
                    unsafe_allow_html=True
                )
                st.dataframe(
                    rows_to_remove[["Chanel Email", "Alias", "Country", "Sector"]],
                    use_container_width=True,
                    height=150
                )
                if st.button("Remove all accesses for this email", key="btn_remove"):
                    df.drop(rows_to_remove.index, inplace=True)
                    st.success(f"All accesses for {email_supp} ({alias_supp}) were removed.")
            else:
                st.info("No access found for this email.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Filters ---
st.markdown("### Filters")
col1, col2, col3 = st.columns(3)

sector_list = ["All"] + sorted(df["Sector"].dropna().unique())
sector_sel = col1.selectbox("Filter by sector", sector_list)

country_list = ["All"] + sorted(df["Country"].dropna().unique())
country_sel = col2.selectbox("Filter by country", country_list)

email_list = ["All"] + sorted(df["Chanel Email"].dropna().unique())
email_sel = col3.selectbox("Filter by Chanel email", email_list)

df_display = df.copy()
if sector_sel != "All":
    df_display = df_display[df_display["Sector"] == sector_sel]
if country_sel != "All":
    df_display = df_display[df_display["Country"] == country_sel]
if email_sel != "All":
    df_display = df_display[df_display["Chanel Email"] == email_sel]

st.markdown("### List of accesses")
st.dataframe(
    df_display[["Chanel Email", "Alias", "Country", "Sector"]],
    use_container_width=True,
    height=400
)