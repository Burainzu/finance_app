import streamlit as st
import sqlite3
import pandas as pd  # type: ignore
from datetime import date

# Custom CSS untuk tema soda yang cerah dan menyegarkan
def set_soda_theme():
    st.markdown("""
        <style>
        /* Tema Soda - Warna cerah, segar, dan energik */
        :root {
            --primary: #FF6B9D;      /* Pink cerah */
            --secondary: #00D4FF;    /* Cyan terang */
            --success: #6FFF5E;      /* Hijau neon */
            --warning: #FFD60A;      /* Kuning bright */
            --dark: #1a1a2e;         /* Gelap */
            --light: #f8f9ff;        /* Putih biru */
        }
        
        /* Background utama */
        .stApp {
            background: linear-gradient(135deg, #f8f9ff 0%, #e0f7ff 50%, #fff5e6 100%);
        }
        
        /* Header styling */
        .stTitle {
            color: #1a1a2e !important;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            font-weight: 900;
        }
        
        h1, h2, h3 {
            color: #1a1a2e !important;
            font-weight: 800 !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FF6B9D 0%, #FF8AB5 100%);
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #fff !important;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            -webkit-text-fill-color: white;
        }
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] [role="button"],
        [data-testid="stSidebar"] div {
            color: white;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(90deg, #FF6B9D 0%, #00D4FF 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 25px rgba(255, 107, 157, 0.4) !important;
        }
        
        /* Input fields */
        .stTextInput input,
        .stNumberInput input,
        .stDateInput input,
        .stSelectbox select,
        .stMultiSelect select,
        .stTextArea textarea {
            background-color: #FFFFFF !important;
            border: 2px solid #00D4FF !important;
            border-radius: 10px !important;
            padding: 10px !important;
            color: #1a1a2e !important;
            transition: all 0.3s ease !important;
        }

        .stSelectbox option,
        .stMultiSelect option,
        select option {
            background-color: #FFFFFF !important;
            color: #1a1a2e !important;
        }
        
        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus,
        .stSelectbox select:focus,
        .stMultiSelect select:focus,
        .stTextArea textarea:focus {
            border-color: #FF6B9D !important;
            box-shadow: 0 0 15px rgba(255, 107, 157, 0.4) !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: linear-gradient(90deg, #00D4FF 0%, #6FFF5E 100%) !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
        }
        
        /* Metric cards */
        .metric-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #e0f7ff 100%);
            border: 2px solid #00D4FF;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
        }
        
        /* Success/Info/Error messages */
        .stSuccess {
            background-color: #e8f5e9 !important;
            border-left: 4px solid #6FFF5E !important;
            border-radius: 8px !important;
        }
        
        .stError {
            background-color: #ffebee !important;
            border-left: 4px solid #FF6B9D !important;
            border-radius: 8px !important;
        }
        
        .stInfo {
            background-color: #e0f7ff !important;
            border-left: 4px solid #00D4FF !important;
            border-radius: 8px !important;
        }
        
        .stWarning {
            background-color: #fff9e6 !important;
            border-left: 4px solid #FFD60A !important;
            border-radius: 8px !important;
        }
        
        /* Container styling */
        .stContainer {
            background: white;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }
        
        /* Divider styling */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, #FF6B9D, #00D4FF, #6FFF5E);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] button {
            color: #1a1a2e !important;
            font-weight: 700 !important;
        }
        
        .stTabs [aria-selected="true"] {
            border-bottom: 3px solid #FF6B9D !important;
        }
        
        /* Transaction row styling */
        .transaction-row {
            background: linear-gradient(90deg, #FFFFFF 0%, #f0fbff 100%);
            border-left: 4px solid #00D4FF;
            border-radius: 10px;
            padding: 12px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }
        
        .transaction-row:hover {
            box-shadow: 0 6px 20px rgba(0, 212, 255, 0.3);
            transform: translateX(5px);
        }
        
        /* Edit mode indicator */
        .edit-mode-banner {
            background: linear-gradient(90deg, #FFD60A, #FF6B9D);
            color: white;
            padding: 12px;
            border-radius: 10px;
            text-align: center;
            font-weight: 700;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(255, 214, 10, 0.3);
        }
        
        /* Global text color - ensure all text is dark */
        * {
            color: #1a1a2e !important;
        }
        
        /* Override specific elements */
        .stMarkdown p, .stMarkdown span, .stMarkdown div, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #1a1a2e !important;
        }
        
        .stText, .stCaption, .stMetric {
            color: #1a1a2e !important;
        }
        
        /* Labels for inputs */
        .stSelectbox label, .stDateInput label, .stNumberInput label, .stTextInput label, .stTextArea label {
            color: #1a1a2e !important;
            font-weight: 600 !important;
        }
        
        /* Tab labels */
        .stTabs [data-baseweb="tab-list"] button {
            color: #1a1a2e !important;
            font-weight: 700 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Database setup
def init_db():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Create wallets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_id INTEGER,
            date DATE NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            description TEXT,
            category_id INTEGER,
            FOREIGN KEY (wallet_id) REFERENCES wallets(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Database helper functions
def get_connection():
    return sqlite3.connect('finance.db')

# Wallet functions
def create_wallet(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO wallets (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def get_wallets():
    conn = get_connection()
    wallets = pd.read_sql('SELECT * FROM wallets ORDER BY id', conn)
    conn.close()
    return wallets

def delete_wallet(wallet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE wallet_id = ?', (wallet_id,))
    cursor.execute('DELETE FROM wallets WHERE id = ?', (wallet_id,))
    conn.commit()
    conn.close()

def get_wallet_balance(wallet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END), 0)
        FROM transactions WHERE wallet_id = ?
    ''', (wallet_id,))
    balance = cursor.fetchone()[0]
    conn.close()
    return balance

# Category functions
def create_category(name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_categories():
    conn = get_connection()
    categories = pd.read_sql('SELECT * FROM categories ORDER BY name', conn)
    conn.close()
    return categories

def delete_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE transactions SET category_id = NULL WHERE category_id = ?', (category_id,))
    cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()

# Transaction functions
def create_transaction(wallet_id, transaction_date, amount, trans_type, description, category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (wallet_id, date, amount, type, description, category_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (wallet_id, transaction_date, amount, trans_type, description, category_id))
    conn.commit()
    conn.close()

def get_transactions(wallet_id):
    conn = get_connection()
    transactions = pd.read_sql('''
        SELECT t.id, t.date, t.amount, t.type, t.description, c.name as category
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        WHERE t.wallet_id = ?
        ORDER BY t.date DESC, t.id DESC
    ''', conn, params=(wallet_id,))
    conn.close()
    return transactions

def update_transaction(trans_id, transaction_date, amount, trans_type, description, category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions 
        SET date = ?, amount = ?, type = ?, description = ?, category_id = ?
        WHERE id = ?
    ''', (transaction_date, amount, trans_type, description, category_id, trans_id))
    conn.commit()
    conn.close()

def delete_transaction(trans_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (trans_id,))
    conn.commit()
    conn.close()

def get_transaction_by_id(trans_id):
    conn = get_connection()
    transaction = pd.read_sql('SELECT * FROM transactions WHERE id = ?', conn, params=(trans_id,))
    conn.close()
    return transaction

# Initialize database
init_db()

# Streamlit UI Configuration
st.set_page_config(
    page_title="Aplikasi Pencatatan Keuangan", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Soda Theme
set_soda_theme()

st.title("🥤 Aplikasi Pengelola Keuangan - Soda Style")

# Initialize session state
if 'selected_wallet' not in st.session_state:
    st.session_state.selected_wallet = None
if 'edit_transaction_id' not in st.session_state:
    st.session_state.edit_transaction_id = None

# Sidebar for wallet selection
with st.sidebar:
    st.header("👛 KELOLA DOMPET")
    wallets = get_wallets()
    
    if not wallets.empty:
        wallet_options = wallets[['id', 'name']].values.tolist()
        wallet_names = [f"💳 {w[1]}" for w in wallet_options]
        wallet_ids = [w[0] for w in wallet_options]
        
        selected_index = 0
        if st.session_state.selected_wallet:
            try:
                selected_index = wallet_ids.index(st.session_state.selected_wallet)
            except ValueError:
                selected_index = 0
        
        selected_wallet_name = st.selectbox(
            "🗂️ Pilih Dompet",
            wallet_names,
            index=selected_index,
            key="wallet_select"
        )
        st.session_state.selected_wallet = wallet_ids[wallet_names.index(selected_wallet_name)]
        
        # Show wallet balance
        balance = get_wallet_balance(st.session_state.selected_wallet)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255,255,255,0.3), rgba(255,255,255,0.15)); padding: 15px; border-radius: 10px; text-align: center; margin: 15px 0; border: 2px solid #FF6B9D;">
        <h3 style="color: #1a1a2e; margin: 0; font-weight: 900;">💰 Saldo Dompet</h3>
        <h2 style="color: #FF6B9D; text-shadow: 0 1px 3px rgba(0,0,0,0.1); margin: 10px 0; font-weight: 900;">Rp {:,.0f}</h2>
        </div>
        """.format(balance), unsafe_allow_html=True)
        
        if st.button("🗑️ Hapus Dompet", key="delete_wallet", use_container_width=True):
            delete_wallet(st.session_state.selected_wallet)
            st.session_state.selected_wallet = None
            st.success("Dompet berhasil dihapus!")
            st.rerun()
    else:
        st.info("📭 Belum ada dompet. Silakan buat dompet baru.")
    
    st.divider()
    
    # Create new wallet
    with st.expander("➕ Buat Dompet Baru", expanded=False):
        new_wallet_name = st.text_input("Nama Dompet Baru", placeholder="Cth: Tabungan, Operasional, dll")
        if st.button("✅ Buat Dompet", key="create_wallet", use_container_width=True):
            if new_wallet_name:
                create_wallet(new_wallet_name)
                st.success(f"✅ Dompet '{new_wallet_name}' berhasil dibuat!")
                st.rerun()
            else:
                st.error("❌ Nama dompet tidak boleh kosong!")
    
    st.divider()
    
    # Category management
    st.header("📁 KATEGORI")
    categories = get_categories()
    
    if not categories.empty:
        st.write(f"📊 Total kategori: **{len(categories)}**")
        for idx, row in categories.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(f"🏷️ {row['name']}")
            with col2:
                if st.button("🗑️", key=f"del_cat_{row['id']}", help="Hapus kategori"):
                    delete_category(row['id'])
                    st.success("Kategori dihapus!")
                    st.rerun()
    
    with st.expander("➕ Tambah Kategori Baru", expanded=False):
        new_category = st.text_input("Nama Kategori", placeholder="Cth: Makan, Transport, dll", key="new_category")
        if st.button("✅ Tambah Kategori", key="add_category", use_container_width=True):
            if new_category:
                if create_category(new_category):
                    st.success(f"✅ Kategori '{new_category}' berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("❌ Kategori sudah ada!")
            else:
                st.error("❌ Nama kategori tidak boleh kosong!")

# Main content
if st.session_state.selected_wallet:
    selected_wallet_id = st.session_state.selected_wallet
    wallet_name = wallets[wallets['id'] == selected_wallet_id]['name'].values[0]
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, rgba(255,107,157,0.15), rgba(0,212,255,0.15), rgba(111,255,94,0.15)); padding: 20px; border-radius: 12px; margin: 20px 0; border: 2px solid #FF6B9D;">
    <h2 style="color: #1a1a2e; text-shadow: 0 1px 3px rgba(0,0,0,0.05); margin: 0; font-weight: 900;">📊 Pengelolaan Transaksi: <span style="font-weight: 900; color: #FF6B9D;">{wallet_name}</span></h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab layout
    tab1, tab2 = st.tabs(["📝 Tambah/Edit Transaksi", "📋 Daftar Transaksi"])
    
    with tab1:
        st.subheader("📝 Form Transaksi Baru")
        
        categories = get_categories()
        category_options = [""] + categories['name'].tolist() if not categories.empty else [""]
        
        # Edit mode atau create mode
        if st.session_state.edit_transaction_id:
            trans_data = get_transaction_by_id(st.session_state.edit_transaction_id)
            if not trans_data.empty:
                trans = trans_data.iloc[0]
                default_date = pd.to_datetime(trans['date']).date()
                default_amount = trans['amount']
                default_type = trans['type']
                default_desc = trans['description']
                default_category = categories[categories['id'] == trans['category_id']]['name'].values[0] if trans['category_id'] and not categories.empty else ""
                
                # Edit mode banner
                st.markdown(f"""
                    <div class="edit-mode-banner">
                    ✏️ MODE EDIT - Transaksi #{trans['id']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.session_state.edit_transaction_id = None
                st.rerun()
        else:
            default_date = date.today()
            default_amount = 0.0
            default_type = "expense"
            default_desc = ""
            default_category = ""
        
        # Form layout yang lebih baik
        col1, col2 = st.columns(2)
        with col1:
            trans_date = st.date_input(
                "📅 Tanggal Transaksi", 
                value=default_date,
                help="Pilih tanggal terjadinya transaksi"
            )
        with col2:
            trans_type = st.selectbox(
                "💳 Tipe Transaksi",
                ["income", "expense"],
                index=0 if default_type == "income" else 1,
                format_func=lambda x: "📈 Uang Masuk" if x == "income" else "📉 Uang Keluar",
                help="Pilih apakah ini pemasukan atau pengeluaran"
            )
        
        col3, col4 = st.columns(2)
        with col3:
            amount = st.number_input(
                "💵 Nominal (Rp)",
                value=default_amount,
                min_value=0.0,
                step=1000.0,
                help="Masukkan jumlah uang"
            )
        with col4:
            category = st.selectbox(
                "🏷️ Kategori",
                category_options,
                index=category_options.index(default_category) if default_category in category_options else 0,
                help="Pilih kategori transaksi (opsional)"
            )
        
        description = st.text_area(
            "📝 Keterangan / Memo",
            value=default_desc,
            height=100,
            placeholder="Tulis deskripsi transaksi di sini...",
            help="Penjelasan singkat tentang transaksi"
        )
        
        # Action buttons
        st.divider()
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if st.button("💾 Simpan Transaksi", key="save_trans", use_container_width=True):
                if amount <= 0:
                    st.error("❌ Nominal harus lebih dari Rp 0!")
                else:
                    category_id = None
                    if category and not categories.empty:
                        cat_row = categories[categories['name'] == category]
                        if not cat_row.empty:
                            category_id = cat_row.iloc[0]['id']
                    
                    if st.session_state.edit_transaction_id:
                        update_transaction(st.session_state.edit_transaction_id, trans_date, amount, 
                                         trans_type, description, category_id)
                        st.success("✅ Transaksi berhasil diperbarui!")
                        st.session_state.edit_transaction_id = None
                    else:
                        create_transaction(selected_wallet_id, trans_date, amount, 
                                        trans_type, description, category_id)
                        st.success("✅ Transaksi berhasil ditambahkan!")
                    st.rerun()
        
        with col2:
            if st.session_state.edit_transaction_id:
                if st.button("❌ Batal Edit", key="cancel_edit", use_container_width=True):
                    st.session_state.edit_transaction_id = None
                    st.rerun()
            else:
                st.button("🔄 Reset", key="reset_form", use_container_width=True, 
                         help="Kosongkan form untuk transaksi baru")
        
        with col3:
            st.write("")  # Spacer
    
    with tab2:
        st.subheader("📋 Daftar Semua Transaksi")
        
        transactions = get_transactions(selected_wallet_id)
        
        if not transactions.empty:
            # Summary cards
            total_income = transactions[transactions['type'] == 'income']['amount'].sum()
            total_expense = transactions[transactions['type'] == 'expense']['amount'].sum()
            net_balance = total_income - total_expense
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(111,255,94,0.2), rgba(144,238,144,0.2)); padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #6FFF5E;">
                <h4 style="color: #1a1a2e; text-shadow: 0 1px 3px rgba(0,0,0,0.05); font-weight: 900;">📈 Pemasukan</h4>
                <h2 style="color: #6FFF5E; text-shadow: 0 1px 3px rgba(0,0,0,0.05); font-weight: 900;">Rp {:,.0f}</h2>
                </div>
                """.format(total_income), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(255,107,157,0.2), rgba(255,138,181,0.2)); padding: 20px; border-radius: 12px; text-align: center; border: 2px solid #FF6B9D;">
                <h4 style="color: #1a1a2e; text-shadow: 0 1px 3px rgba(0,0,0,0.05); font-weight: 900;">📉 Pengeluaran</h4>
                <h2 style="color: #FF6B9D; text-shadow: 0 1px 3px rgba(0,0,0,0.05); font-weight: 900;">Rp {:,.0f}</h2>
                </div>
                """.format(total_expense), unsafe_allow_html=True)
            
            with col3:
                balance_color = "#6FFF5E" if net_balance >= 0 else "#FF6B9D"
                border_color = "2px solid #6FFF5E" if net_balance >= 0 else "2px solid #FF6B9D"
                text_color = "#1a1a2e"
                val_color = balance_color
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba({}, {}, {}, 0.1), rgba({}, {}, {}, 0.05)); padding: 20px; border-radius: 12px; text-align: center; border: {}">
                <h4 style="color: {}; text-shadow: 0 1px 3px rgba(0,0,0,0.05); font-weight: 900;">💰 Saldo Bersih</h4>
                <h2 style="color: {}; text-shadow: 0 1px 3px rgba(0,0,0,0.05); font-weight: 900;">Rp {:,.0f}</h2>
                </div>
                """.format(
                    int(balance_color[1:3], 16), int(balance_color[3:5], 16), int(balance_color[5:7], 16),
                    int(balance_color[1:3], 16), int(balance_color[3:5], 16), int(balance_color[5:7], 16),
                    border_color, text_color, val_color, net_balance
                ), unsafe_allow_html=True)
            
            st.divider()
            
            # Filter section
            col1, col2 = st.columns(2)
            with col1:
                filter_type = st.selectbox(
                    "🔍 Filter Tipe",
                    ["Semua", "Pemasukan", "Pengeluaran"],
                    help="Tampilkan transaksi berdasarkan tipe"
                )
            
            # Apply filter
            if filter_type == "Pemasukan":
                filtered_trans = transactions[transactions['type'] == 'income']
            elif filter_type == "Pengeluaran":
                filtered_trans = transactions[transactions['type'] == 'expense']
            else:
                filtered_trans = transactions
            
            # Display transactions
            st.write(f"📊 Total transaksi: **{len(filtered_trans)}** transaksi")
            st.divider()
            
            for idx, row in filtered_trans.iterrows():
                with st.container():
                    type_emoji = "📈" if row['type'] == 'income' else "📉"
                    type_color = "#6FFF5E" if row['type'] == 'income' else "#FF6B9D"
                    
                    col1, col2, col3, col4, col5, col6 = st.columns([1.5, 1.5, 2, 2, 0.8, 0.8])
                    
                    with col1:
                        st.markdown(f"<div style='color: #1a1a2e; font-weight: 600;'>📅 {row['date']}</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"<div style='color: {type_color}; font-size: 20px; text-align: center;'>{type_emoji}</div>", unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"<div style='color: #1a1a2e; font-weight: 700; font-size: 16px;'>Rp {row['amount']:,.0f}</div>", unsafe_allow_html=True)
                    
                    with col4:
                        cat = row['category'] if row['category'] else "—"
                        desc = row['description'] if row['description'] else "—"
                        st.markdown(f"<div style='color: #1a1a2e; font-size: 14px;'>🏷️ <b>{cat}</b> | {desc[:20]}...</div>", unsafe_allow_html=True)
                    
                    with col5:
                        if st.button("✏️ Edit", key=f"edit_{row['id']}", help="Edit transaksi ini"):
                            st.session_state.edit_transaction_id = row['id']
                            st.rerun()
                    
                    with col6:
                        if st.button("🗑️", key=f"del_{row['id']}", help="Hapus transaksi ini"):
                            delete_transaction(row['id'])
                            st.success("✅ Transaksi berhasil dihapus!")
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("📭 Belum ada transaksi. Silakan tambahkan transaksi baru di tab 'Tambah/Edit Transaksi'!")
else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(111,255,94,0.15)); padding: 40px; border-radius: 15px; text-align: center; margin: 50px 0; border: 2px solid #00D4FF;">
    <h1 style="color: #1a1a2e; text-shadow: 0 1px 3px rgba(0,0,0,0.05); margin: 0; font-weight: 900;">👈 Mulai Kelola Keuangan Anda!</h1>
    <h3 style="color: #1a1a2e; text-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 15px; font-weight: 700;">Silakan buat atau pilih dompet di sidebar untuk memulai pencatatan transaksi.</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Tambahkan info box
    st.info("💡 **Tips:** Gunakan sidebar di kiri untuk mengelola dompet dan kategori transaksi Anda.")
