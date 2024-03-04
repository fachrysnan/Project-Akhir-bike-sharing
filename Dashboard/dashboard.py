import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

st.set_page_config(page_title="Bike Rental")

hour_df = pd.read_csv("hour.csv")
hour_df.head()

# Mengubah judul kolom

hour_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'hr' : 'hour',
    'weathersit': 'weathercond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka-angka menjadi keterangan nama

hour_df['month'] = hour_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

hour_df['year'] = hour_df['year'].map({
    0: 2011, 1: 2012
})

hour_df['season'] = hour_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
hour_df['weekday'] = hour_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
hour_df['weathercond'] = hour_df['weathercond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Menyiapkan helper functions

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

def create_seasonly_rent_df(df):
    seasonly_rent_df = df.groupby(by='season').agg({
        'count': 'sum'
    }).reset_index()
    return seasonly_rent_df

def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'season':'sum',
        'count': 'sum'
    })
    ordered_weeks = [
        'Mon','Tue','Wed','Thu','Fri','Sat','Sun'
    ]
    weekday_rent_df = weekday_rent_df.reindex(ordered_weeks, fill_value=0)
    return weekday_rent_df

def create_hourly_rent_df(df):
    hourly_rent_df = df.groupby(by='hour').agg({
        'season':'sum',
        'count': 'sum'
    }).reset_index()
    return hourly_rent_df

def create_yearly_rent_df(df):
    yearly_rent_df = df.groupby(by='year').agg({
        'count': 'sum'
    }).reset_index()
    return yearly_rent_df

# Membuat filter komponen

min_date = pd.to_datetime(hour_df['dateday']).dt.date.min()
max_date = pd.to_datetime(hour_df['dateday']).dt.date.max()

# Sidebar

with st.sidebar:
    st.title("Bike Rental: For Your Better Living")
    st.image('https://github.com/fachrysnan/Bike-sharing-dataset/blob/main/bike-rental-logo-with-a-bicycle-and-label-combination-for-any-business-vector.jpg?raw=true')
    selected_status = st.sidebar.selectbox(
        'Pilih Topik yang Ingin Ditampilkan', 
        options = [
            'Jumlah Pengguna Sepeda berdasarkan Hari dalam Seminggu','Jumlah Penyewa Sepeda Berdasarkan Jam', 'Jumlah Penyewa Sepeda berdasarkan Bulan','Jumlah Penyewa Sepeda berdasarkan Tahun'
            ]) 

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )
    st.markdown("""---""") 
  
# Menguhubungkan filter dengan main_df

main_df = hour_df[
    (hour_df['dateday'] >= str(start_date)) & 
    (hour_df['dateday'] <= str(end_date))
]

# Memasukan main_df ke helper functions yang telah dibuat 

yearly_users_df = create_yearly_rent_df(main_df)
monthly_users_df = create_monthly_rent_df(main_df)
weekday_users_df = create_weekday_rent_df(main_df)
seasonly_users_df = create_seasonly_rent_df(main_df)
hourly_users_df = create_hourly_rent_df(main_df)

# Membuat title

st.title("Bike Rental: Bike-Sharing Dashboard")

st.markdown("""---""")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['count'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("""---""")

# Membuat grafik

if selected_status == 'Jumlah Pengguna Sepeda berdasarkan Hari dalam Seminggu':    
    fig, ax = plt.subplots()
    sns.barplot(
        x='weekday',
        y='count',
        data=weekday_users_df,
        palette='rainbow',
        ax=ax)
    plt.title('Jumlah Pengguna Sepeda berdasarkan Hari dalam Seminggu')
    plt.xlabel('Hari dalam seminggu')
    plt.ylabel('Jumlah Penyewa Sepeda')
    st.pyplot(fig)

if selected_status == 'Jumlah Penyewa Sepeda Berdasarkan Jam': 
    fig2, ax = plt.subplots()
    sns.lineplot(
        data=hourly_users_df,
        x="hour",
        y="count",
        marker="o")
    plt.title('Jumlah Penyewa Sepeda berdasarkan Jam')
    plt.xlabel('Jam')
    plt.ylabel('Jumlah Penyewa Sepeda')
    plt.xticks(range(0, 24, 2))
    st.pyplot(fig2)

if selected_status == 'Jumlah Penyewa Sepeda berdasarkan Bulan': 
    fig3, ax = plt.subplots()
    sns.barplot(
        x='month',
        y='count',
        data=monthly_users_df,
        palette='rainbow')
    plt.title('Jumlah Penyewa Sepeda berdasarkan Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Penyewa Sepeda')
    st.pyplot(fig3)

if selected_status == 'Jumlah Penyewa Sepeda berdasarkan Tahun':  
    fig4, ax = plt.subplots()
    sns.barplot(
        data=yearly_users_df,
        x='year',
        y='count',
        ax=ax,
        palette='rainbow'
    )  
    plt.title('Jumlah Penyewa Sepeda berdasarkan Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Jumlah Penyewa Sepeda')
    st.pyplot(fig4)

st.caption('Copyright (c) Fachry Syifa Ananda 2024')

           

           

