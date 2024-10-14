import streamlit as st
import threading
import time
import random

# Order Class to store order details
class Order:
    def __init__(self, order_id, customer_name, food_item, cook_time):
        self.order_id = order_id
        self.customer_name = customer_name
        self.food_item = food_item
        self.cook_time = cook_time
        self.status = "Waiting"

    def get_order_details(self):
        return {
            'Order ID': self.order_id,
            'Customer Name': self.customer_name,
            'Food Item': self.food_item,
            'Cook Time': self.cook_time,
            'Status': self.status
        }

# Chef Class for assigning orders to chefs
class Chef:
    def __init__(self, name):
        self.name = name

    def assign_order(self, order):
        order.status = "In Progress"
        st.write(f"{self.name} is cooking order {order.order_id} for {order.customer_name}...")
        time.sleep(order.cook_time)
        order.status = "Completed"
        st.write(f"Order {order.order_id} is completed by {self.name} and is ready to be served!")

# OrderManager Class to handle order scheduling
class OrderManager:
    def __init__(self):
        self.orders = []
        self.chefs = [Chef(f"Chef {i}") for i in range(1, 3)]  # Two chefs for simplicity

    def add_order(self, order):
        self.orders.append(order)

    def schedule_orders(self):
        # FCFS Scheduling: Orders are processed in the order they were added
        for order in self.orders:
            if order.status == "Waiting":
                # Assign the order to the next available chef
                chef_thread = threading.Thread(target=self.chefs[0].assign_order, args=(order,))
                chef_thread.start()

    def get_orders(self):
        return self.orders

# Streamlit GUI

# Initialize the OrderManager only once
if 'order_manager' not in st.session_state:
    st.session_state['order_manager'] = OrderManager()

order_manager = st.session_state['order_manager']

st.title("Restaurant Food Management System")

# User input for new orders
if 'order_collected' not in st.session_state:
    st.session_state['order_collected'] = False

if not st.session_state['order_collected']:
    with st.form("new_order_form"):
        customer_name = st.text_input("Customer Name")
        food_item = st.text_input("Food Item Ordered")
        cook_time = st.number_input("Estimated Cooking Time (seconds)", min_value=1, step=1)
        submitted = st.form_submit_button("Add Order")

        if submitted and customer_name and food_item:
            order_id = f"Order_{random.randint(1000, 9999)}"
            new_order = Order(order_id, customer_name, food_item, cook_time)
            order_manager.add_order(new_order)
            st.success(f"Order {order_id} added successfully!")

    # Display current orders
    st.subheader("Orders Added So Far")
    orders = order_manager.get_orders()
    if orders:
        for order in orders:
            st.write(f"Order ID: {order.order_id}, Customer: {order.customer_name}, "
                    f"Food: {order.food_item}, Time: {order.cook_time}s, Status: {order.status}")
    else:
        st.write("No orders yet!")

    # Button to stop taking orders and start processing
    if st.button("Submit All Orders"):
        st.session_state['order_collected'] = True

# After all orders are collected, process them
if st.session_state['order_collected']:
    st.subheader("Processing Orders")
    st.write("All orders have been collected. Cooking will now begin...")

    # Start scheduling and processing orders
    order_manager.schedule_orders()

    # Display final status of orders
    orders = order_manager.get_orders()
    for order in orders:
        st.write(f"Order ID: {order.order_id}, Customer: {order.customer_name}, "
                f"Food: {order.food_item}, Time: {order.cook_time}s, Status: {order.status}")

    # Instead of using st.experimental_rerun(), we will clear the session state and inform the user to refresh the page manually.
    if st.button("Reset"):
        # Clear session state
        for key in st.session_state.keys():
            del st.session_state[key]
        st.write("Orders and state have been reset. Please refresh the page manually to start again.")
