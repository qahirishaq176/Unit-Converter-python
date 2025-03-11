import streamlit as st

st.title('🌐 Ultimate Unit Converter Pro')
st.markdown('### 🚀 Convert between 50+ units instantly with precision!')

# Session State setup
if 'history' not in st.session_state:
    st.session_state.history = []
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
    
# Expanded conversion options
CONVERSIONS = {
    'Length': {
        'Kilometers to miles': 0.621371,
        'Miles to kilometers': 1/0.621371,
        'Meters to feet': 3.28084,
        'Feet to meters': 1/3.28084,
        'Inches to centimeters': 2.54,
        'Centimeters to inches': 1/2.54
    },
    'Weight': {
        'Kilograms to pounds': 2.20462,
        'Pounds to kilograms': 1/2.20462,
        'Grams to ounces': 0.035274,
        'Ounces to grams': 1/0.035274,
        'Tons to kilograms': 1000,
        'Kilograms to tons': 0.001
    },
    'Time': {
        'Seconds to minutes': 1/60,
        'Minutes to seconds': 60,
        'Hours to days': 1/24,
        'Days to hours': 24,
        'Weeks to months': 0.230137,
        'Months to years': 1/12
    },
    'Temperature': {
        'Celsius to Fahrenheit': lambda c: (c * 9/5) + 32,
        'Fahrenheit to Celsius': lambda f: (f - 32) * 5/9,
        'Celsius to Kelvin': lambda c: c + 273.15,
        'Kelvin to Celsius': lambda k: k - 273.15
    },
    'Area': {
        'Square meters to square feet': 10.7639,
        'Square feet to square meters': 1/10.7639,
        'Acres to hectares': 0.404686,
        'Hectares to acres': 2.47105
    },
    'Digital Storage': {
        'Bytes to kilobytes': 1/1024,
        'Kilobytes to megabytes': 1/1024,
        'Megabytes to gigabytes': 1/1024,
        'Gigabytes to terabytes': 1/1024
    }
}

# Improved Layout Structure
with st.container():
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        category = st.selectbox('📦 Select Category', list(CONVERSIONS.keys()), 
                              help="Choose from 6 different measurement categories")
        
    with col2:
        conversions = CONVERSIONS[category]
        unit = st.selectbox('🔄 Select Conversion', list(conversions.keys()),
                          help="Choose your desired conversion type")

# Real-time Conversion Section
with st.container():
    col3, col4 = st.columns(2, gap="large")
    with col3:
        value = st.number_input('🔢 Enter Value', min_value=0.0, value=1.0, step=0.1,
                              key="input_value", help="Enter positive numerical value to convert")
        
        # Negative value handling
        if value < 0:
            st.warning("⚠️ Please enter positive values only")
            value = abs(value)

        # Advanced Settings
        with st.expander("⚙️ Custom Conversion Factor", expanded=False):
            custom_factor = st.number_input("Set Custom Factor", 
                                          value=list(conversions.values())[0] if not callable(list(conversions.values())[0]) else 1.0,
                                          disabled=(category == 'Temperature'),
                                          key="custom_factor")

    # Real-time Results Display
    with col4:
        # Calculate result immediately on input change
        try:
            if category == 'Temperature':
                result = conversions[unit](value)
            else:
                factor = conversions[unit] if not callable(conversions[unit]) else 1.0
                result = value * (custom_factor if st.session_state.get('use_custom') else factor)
            
            # Update history automatically
            history_entry = f"{value:.2f} {unit.split(' to ')[0]} → {result:.4f} {unit.split(' to ')[1]}"
            if len(st.session_state.history) == 0 or st.session_state.history[0] != history_entry:
                st.session_state.history.insert(0, history_entry)
                if len(st.session_state.history) > 5:
                    st.session_state.history.pop()
            
            # Display result card
            with st.container():
                st.markdown(f"<div class='result-card'>", unsafe_allow_html=True)
                st.markdown("### 📦 Conversion Result")
                st.metric(label="Result", value=f"{result:.6f}")
                
                # Additional conversions
                if category == 'Length' and 'Kilometers' in unit:
                    st.caption(f"Also: {(value * 1000):.2f} meters | {(value * 1093.61):.2f} yards")
                
                # Visual feedback
                if result != 0:
                    st.balloons()
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error in conversion: {str(e)}")

# History and Favorites Section
with st.container():
    col5, col6 = st.columns([2, 1], gap="large")
    
    with col5:
        with st.expander("📜 Conversion History (Last 5)", expanded=True):
            for entry in st.session_state.history:
                st.markdown(f"<div class='history-item'>{entry}</div>", unsafe_allow_html=True)
    
    with col6:
        if st.session_state.favorites:
            st.subheader("⭐ Favorite Conversions")
            for fav in st.session_state.favorites:
                st.button(fav, use_container_width=True)

# Footer
st.markdown("""
<div class="footer">
    <p style="margin:0">Developed with ❤️ by <strong>Qahir Ishaq</strong></p>
    <small>© 2023 Ultimate Unit Converter Pro. All rights reserved.</small>
</div>
""", unsafe_allow_html=True)