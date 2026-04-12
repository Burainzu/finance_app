import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

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

# Streamlit UI
st.set_page_config(page_title="Aplikasi Pencatatan Keuangan", layout="wide")

st.title("💰 Aplikasi Pencatatan Keuangan")

# Initialize session state
if 'selected_wallet' not in st.session_state:
    st.session_state.selected_wallet = None
if 'edit_transaction_id' not in st.session_state:
    st.session_state.edit_transaction_id = None

# Sidebar for wallet selection
with st.sidebar:
    st.header("👛 Dompet")
    wallets = get_wallets()
    
    if not wallets.empty:
        wallet_options = wallets[['id', 'name']].values.tolist()
        wallet_names = [f"{w[1]}" for w in wallet_options]
        wallet_ids = [w[0] for w in wallet_options]
        
        selected_index = 0
        if st.session_state.selected_wallet:
            try:
                selected_index = wallet_ids.index(st.session_state.selected_wallet)
            except ValueError:
                selected_index = 0
        
        selected_wallet_name = st.selectbox("Pilih Dompet", wallet_names, index=selected_index)
        st.session_state.selected_wallet = wallet_ids[wallet_names.index(selected_wallet_name)]
        
        # Show wallet balance
        balance = get_wallet_balance(st.session_state.selected_wallet)
        st.metric("Saldo", f"Rp {balance:,.2f}")
        
        if st.button("Hapus Dompet", key="delete_wallet"):
            delete_wallet(st.session_state.selected_wallet)
            st.session_state.selected_wallet = None
            st.rerun()
    else:
        st.info("Belum ada dompet. Silakan buat dompet baru.")
    
    st.divider()
    
    # Create new wallet
    with st.expander("➕ Buat Dompet Baru"):
        new_wallet_name = st.text_input("Nama Dompet")
        if st.button("Buat Dompet", key="create_wallet"):
            if new_wallet_name:
                create_wallet(new_wallet_name)
                st.success(f"Dompet '{new_wallet_name}' berhasil dibuat!")
                st.rerun()
            else:
                st.error("Nama dompet tidak boleh kosong!")
    
    st.divider()
    
    # Category management
    st.header("📁 Kategori")
    categories = get_categories()
    
    if not categories.empty:
        for idx, row in categories.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.text(row['name'])
            with col2:
                if st.button("🗑️", key=f"del_cat_{row['id']}"):
                    delete_category(row['id'])
                    st.rerun()
    
    with st.expander("➕ Tambah Kategori"):
        new_category = st.text_input("Nama Kategori", key="new_category")
        if st.button("Tambah Kategori", key="add_category"):
            if new_category:
                if create_category(new_category):
                    st.success(f"Kategori '{new_category}' berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("Kategori sudah ada!")
            else:
                st.error("Nama kategori tidak boleh kosong!")

# Main content
if st.session_state.selected_wallet:
    selected_wallet_id = st.session_state.selected_wallet
    wallet_name = wallets[wallets['id'] == selected_wallet_id]['name'].values[0]
    
    st.header(f"📊 Transaksi - {wallet_name}")
    
    # Tab layout
    tab1, tab2 = st.tabs(["📝 Tambah/Edit Transaksi", "📋 Daftar Transaksi"])
    
    with tab1:
        st.subheader("Form Transaksi")
        
        categories = get_categories()
        category_options = [""] + categories['name'].tolist() if not categories.empty else [""]
        
        # Edit mode or create mode
        if st.session_state.edit_transaction_id:
            trans_data = get_transaction_by_id(st.session_state.edit_transaction_id)
            if not trans_data.empty:
                trans = trans_data.iloc[0]
                default_date = pd.to_datetime(trans['date']).date()
                default_amount = trans['amount']
                default_type = trans['type']
                default_desc = trans['description']
                default_category = categories[categories['id'] == trans['category_id']]['name'].values[0] if trans['category_id'] and not categories.empty else ""
                st.info(f"Mode Edit: Transaksi #{trans['id']}")
            else:
                st.session_state.edit_transaction_id = None
                st.rerun()
        else:
            default_date = date.today()
            default_amount = 0.0
            default_type = "expense"
            default_desc = ""
            default_category = ""
        
        col1, col2 = st.columns(2)
        with col1:
            trans_date = st.date_input("Tanggal", value=default_date)
            trans_type = st.selectbox("Tipe", ["income", "expense"], 
                                    index=0 if default_type == "income" else 1,
                                    format_func=lambda x: "Uang Masuk" if x == "income" else "Uang Keluar")
        with col2:
            amount = st.number_input("Nominal (Rp)", value=default_amount, min_value=0.0, step=1000.0)
            category = st.selectbox("Kategori", category_options, 
                                  index=category_options.index(default_category) if default_category in category_options else 0)
        
        description = st.text_area("Keterangan", value=default_desc)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Simpan Transaksi", key="save_trans"):
                if amount <= 0:
                    st.error("Nominal harus lebih dari 0!")
                else:
                    category_id = None
                    if category and not categories.empty:
                        cat_row = categories[categories['name'] == category]
                        if not cat_row.empty:
                            category_id = cat_row.iloc[0]['id']
                    
                    if st.session_state.edit_transaction_id:
                        update_transaction(st.session_state.edit_transaction_id, trans_date, amount, 
                                         trans_type, description, category_id)
                        st.success("Transaksi berhasil diperbarui!")
                        st.session_state.edit_transaction_id = None
                    else:
                        create_transaction(selected_wallet_id, trans_date, amount, 
                                        trans_type, description, category_id)
                        st.success("Transaksi berhasil ditambahkan!")
                    st.rerun()
        
        with col2:
            if st.session_state.edit_transaction_id:
                if st.button("❌ Batal Edit", key="cancel_edit"):
                    st.session_state.edit_transaction_id = None
                    st.rerun()
    
    with tab2:
        st.subheader("Daftar Transaksi")
        
        transactions = get_transactions(selected_wallet_id)
        
        if not transactions.empty:
            # Summary
            total_income = transactions[transactions['type'] == 'income']['amount'].sum()
            total_expense = transactions[transactions['type'] == 'expense']['amount'].sum()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Pemasukan", f"Rp {total_income:,.2f}")
            col2.metric("Total Pengeluaran", f"Rp {total_expense:,.2f}")
            col3.metric("Saldo Bersih", f"Rp {(total_income - total_expense):,.2f}")
            
            st.divider()
            
            # Transaction table
            for idx, row in transactions.iterrows():
                with st.container():
                    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 3, 3, 3, 1, 1])
                    
                    type_emoji = "📈" if row['type'] == 'income' else "📉"
                    type_color = "green" if row['type'] == 'income' else "red"
                    
                    with col1:
                        st.text(row['date'])
                    with col2:
                        amount_str = f"Rp {row['amount']:,.2f}"
                        st.markdown(f"{type_emoji} <span style='color:{type_color}'>{amount_str}</span>", unsafe_allow_html=True)
                    with col3:
                        st.text("Uang Masuk" if row['type'] == 'income' else "Uang Keluar")
                    with col4:
                        st.text(row['description'] if row['description'] else "-")
                    with col5:
                        st.text(row['category'] if row['category'] else "-")
                    with col6:
                        if st.button("✏️", key=f"edit_{row['id']}"):
                            st.session_state.edit_transaction_id = row['id']
                            st.rerun()
                    with col7:
                        if st.button("🗑️", key=f"del_{row['id']}"):
                            delete_transaction(row['id'])
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("Belum ada transaksi. Silakan tambahkan transaksi baru!")
else:
    st.info("👈 Silakan pilih atau buat dompet di sidebar untuk memulai.")
