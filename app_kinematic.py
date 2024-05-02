import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

def create_single_plot(a1, a2, theta1, theta2):
    # Convert degrees to radians
    theta1_rad = math.radians(theta1)
    theta2_rad = math.radians(theta2)

    # Calculate positions
    x1 = a1 * math.cos(theta1_rad)
    y1 = a1 * math.sin(theta1_rad)
    x2 = x1 + a2 * math.cos(theta1_rad + theta2_rad)
    y2 = y1 + a2 * math.sin(theta1_rad + theta2_rad)

    # Prepare the plot
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'aspect': 'equal'})
    if y2 >= 0:
        ax.plot([0, x1, x2], [0, y1, y2], marker='o')
        ax.set_xlim(-a1-a2, a1+a2)
        ax.set_ylim(-a1-a2, a1+a2)
        ax.set_title(f'Theta1: {theta1}°, Theta2: {theta2}°')
    return fig, (x2, y2)

def create_single_plot_inverse(l1, l2, x,y):
    # Calculate c1 using the correct formula and exponentiation
    c1 = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
    print(c1)
    # Ensure to calculate s2 correctly
    s2 = math.sqrt(1 - c1**2)

    # Calculate theta2
    theta2 = math.atan2(s2, c1)

    # Compute k1 and k2
    k1 = l1 + l2 * math.cos(theta2)
    k2 = l2 * math.sin(theta2)

    # Compute r
    r = math.sqrt(k1**2 + k2**2)

    # Compute gamma
    gamma = math.atan2(k2, k1)

    # Correct expressions for k1 and k2 using trigonometric functions
    k1 = r * math.cos(gamma)
    k2 = r * math.sin(gamma)

    # Calculate theta1
    theta1 = math.atan2(y, x) - math.atan2(k2, k1)

    x2 = l1 * math.cos(theta1 )
    y2 = l1 * math.sin(theta1)


    # Prepare the plot
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'aspect': 'equal'})
    if y >= 0:
        ax.plot([0, x2, x], [0, y2, y], marker='o')
        ax.set_xlim(-l1-l2, l1+l2)
        ax.set_ylim(-l1-l2, l1+l2)
        ax.set_title('Inverse kinematics')
    return fig, (math.degrees(theta1), math.degrees(theta2))

# Sidebar inputs
st.sidebar.title('Input Parameters')
choice = st.sidebar.selectbox('What kinematic are you interested in ', ('Forward kinematics', 'Backward kinematics', 'Trajectory'))
if choice == 'Forward kinematics' :
    a1 = st.sidebar.number_input('Arm Length a1:', min_value=10, max_value=50, value=30)
    a2 = st.sidebar.number_input('Arm Length a2:', min_value=10, max_value=50, value=20)
    theta1 = st.sidebar.slider('Theta1 (degrees):', 0, 180, 45)
    theta2 = st.sidebar.slider('Theta2 (degrees):', 0, 180, 45)
    # Main panel
    st.title('Robot Arm Configuration Plot')
    if st.sidebar.button('Generate Plot'):
        fig, (x2, y2) = create_single_plot(a1, a2, theta1, theta2)
        st.pyplot(fig)
        st.write(f"Coordinates of the last point: ({x2:.2f}, {y2:.2f})")

elif choice == 'Backward kinematics':
    l1 = st.sidebar.number_input('Arm Length a1:', min_value=10, max_value=50, value=30)
    l2 = st.sidebar.number_input('Arm Length a2:', min_value=10, max_value=50, value=20)
    x = st.sidebar.slider('x :', 0, l1+l2, 2)
    y = st.sidebar.slider('y:', 0, l1+l2, 2)
    # Main panel
    st.title('Robot Arm Configuration Plot')
    if st.sidebar.button('Generate Plot'):
        fig, (theta1, theta2) = create_single_plot_inverse(l1, l2, x, y)
        st.pyplot(fig)
        st.write(f"The angle theta 1: ({theta1:.2f}, {theta2:.2f})")
else :
    # Example lists of x and y coordinates
    l1 = st.sidebar.number_input('Arm Length a1:', min_value=10, max_value=50, value=30)
    l2 = st.sidebar.number_input('Arm Length a2:', min_value=10, max_value=50, value=20)

    x1 = st.sidebar.slider('x1 :', 0, l1+l2, 2)
    y1 = st.sidebar.slider('y1:', 0, l1+l2, 2)
    x2 = st.sidebar.slider('x2 :', 0, l1+l2, 2)
    y2 = st.sidebar.slider('y2:', 0, l1+l2, 2)
    x3 = st.sidebar.slider('x3 :', 0, l1+l2, 2)
    y3 = st.sidebar.slider('y3:', 0, l1+l2, 2)

    x_coords=[x1,x2,x3]
    y_coords=[y1,y2,y3]
    # Loop through each coordinate pair
    st_container = st.container()

    # Loop through each coordinate pair
    for x, y in zip(x_coords, y_coords):
        # Call your inverse kinematics plotting function
        fig, angles = create_single_plot_inverse(l1, l2, x, y)
        # Display angles in the app
        st_container.write(f"Angles for (x={x}, y={y}) are: Theta1={angles[0]} degrees, Theta2={angles[1]} degrees")
        # Optionally display the plot (if fig is not None)
        if fig:
            st_container.pyplot(fig)
