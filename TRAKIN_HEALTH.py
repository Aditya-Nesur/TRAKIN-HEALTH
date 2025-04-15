import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Predefined dishes with calorie values (5+ options per meal)
dishes = {
    "Breakfast": {
        "Select a dish": 0,
        "Idli with Sambar (2 pcs)": 300,
        "UPMA": 132,
        "ALOO PHARATHA": 300,
        "POHA": 250,
        "DOSA": 152,
        "SCRAMBLED EGGS": 107,
        "Regular white bread toast": 64,
        "Chole Bhature (1 plate)": 600,
        "Paneer Sandwich (2 slices)": 350,
        "Thepla with Pickle & Curd (2 pcs)": 300
    },
    "Lunch": {
        "Select a dish": 0,
        "Rice with Sambar & Rasam": 500,
        "South Indian Veg Thali": 650,
        "Fish Curry with Rice": 600,
        "Lemon Rice with Papad": 450,
        "Roti (2) with Dal & Sabzi": 450,
        "Rajma Chawal (1 plate)": 550,
        "Chole Chawal (1 plate)": 550,
        "Paneer Butter Masala with Naan": 700,
        "Stuffed Paratha (2) with Curd": 500
    },
    "Dinner": {
        "Select a dish": 0,
        "Chapati with Veg Kurma (2 pcs)": 400,
        "Dosa with Chutney (1 large)": 350,
        "Roti (2) with Palak Paneer": 450,
        "Dal Tadka with Jeera Rice": 500,
        "Aloo Gobi with Chapati (2)": 450,
        "Kadhi Chawal (1 bowl)": 500,
        "Litti Chokha (2 pcs)": 550
    }
}


class HealthTrackerApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Health Tracker")
        self.geometry("500x600")
        self.configure(bg="#E3F2FD")

        # Shared data: 
        # User details (name, age, weight, height, gender)
        self.user_details = {}
        # Global metrics (for the currently selected day)
        self.meal_selections = {}
        self.sleep = 0.0
        self.total_calories = 0
        self.bmi = 0
        self.health_score = 0

        # Weekly tracker variables:
        self.week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.current_day_index = 0
        # weekly_data: Key = day name, Value = dict of data for that day.
        self.weekly_data = {}

        # Container for all pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (EnterDetailsPage, IntakePage, OutputPage, PieChartPage):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(EnterDetailsPage)

    def show_frame(self, cont):
        """Raise the frame to the top (and update data if needed)."""
        frame = self.frames[cont]
        if hasattr(frame, "update_data"):
            frame.update_data()
        frame.tkraise()


class EnterDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E3F2FD")
        self.controller = controller

        title = tk.Label(self, text="Enter Your Details", font=("Arial", 16, "bold"), bg="#E3F2FD")
        title.pack(pady=10)

        details_frame = tk.Frame(self, bg="#E3F2FD")
        details_frame.pack(pady=10)

        # Name
        tk.Label(details_frame, text="Name:", font=("Arial", 12), bg="#E3F2FD")\
            .grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Age
        tk.Label(details_frame, text="Age:", font=("Arial", 12), bg="#E3F2FD")\
            .grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.age_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        # Weight
        tk.Label(details_frame, text="Weight (kg):", font=("Arial", 12), bg="#E3F2FD")\
            .grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.weight_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)

        # Height
        tk.Label(details_frame, text="Height (cm):", font=("Arial", 12), bg="#E3F2FD")\
            .grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.height_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.height_entry.grid(row=3, column=1, padx=5, pady=5)

        # Gender
        tk.Label(details_frame, text="Gender:", font=("Arial", 12), bg="#E3F2FD")\
            .grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")  # default value
        gender_option = tk.OptionMenu(details_frame, self.gender_var, "Male", "Female")
        gender_option.config(font=("Arial", 12))
        gender_option.grid(row=4, column=1, padx=5, pady=5)

        button = tk.Button(self, text="Next: Enter Intake", font=("Arial", 12),
                           bg="#2196F3", fg="white", command=self.save_details)
        button.pack(pady=15)

    def save_details(self):
        try:
            name = self.name_entry.get().strip()
            age = int(self.age_entry.get())
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            gender = self.gender_var.get()
            if not name:
                messagebox.showerror("Error", "Please enter your name.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for age, weight, and height.")
            return

        self.controller.user_details = {
            "name": name,
            "age": age,
            "weight": weight,
            "height": height,
            "gender": gender
        }
        self.controller.show_frame(IntakePage)


class IntakePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E3F2FD")
        self.controller = controller

        # Display the current day name at the top center.
        self.day_label = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#E3F2FD")
        self.day_label.pack(pady=5)

        # Navigation buttons for previous/next day.
        nav_frame = tk.Frame(self, bg="#E3F2FD")
        nav_frame.pack(pady=5)
        prev_btn = tk.Button(nav_frame, text="Previous Day", font=("Arial", 12),
                             bg="#9E9E9E", fg="white", command=self.prev_day)
        prev_btn.pack(side="left", padx=10)
        next_btn = tk.Button(nav_frame, text="Next Day", font=("Arial", 12),
                             bg="#9E9E9E", fg="white", command=self.next_day)
        next_btn.pack(side="left", padx=10)

        title = tk.Label(self, text="Enter Meal Selections & Sleep", font=("Arial", 16, "bold"), bg="#E3F2FD")
        title.pack(pady=10)

        # Create meal selection dropdowns.
        meals_frame = tk.Frame(self, bg="#E3F2FD")
        meals_frame.pack(pady=10)
        self.meal_vars = {}
        row_index = 0
        for meal in dishes:
            tk.Label(meals_frame, text=f"{meal}:", font=("Arial", 12), bg="#E3F2FD")\
                .grid(row=row_index, column=0, sticky="e", padx=5, pady=5)
            var = tk.StringVar()
            var.set("Select a dish")
            option = tk.OptionMenu(meals_frame, var, *list(dishes[meal].keys()))
            option.config(font=("Arial", 12))
            option.grid(row=row_index, column=1, padx=5, pady=5)
            self.meal_vars[meal] = var
            row_index += 1

        # Sleep hours entry.
        sleep_frame = tk.Frame(self, bg="#E3F2FD")
        sleep_frame.pack(pady=10)
        tk.Label(sleep_frame, text="Enter Sleep Hours:", font=("Arial", 12), bg="#E3F2FD")\
            .grid(row=0, column=0, padx=5, pady=5)
        self.sleep_entry = tk.Entry(sleep_frame, font=("Arial", 12))
        self.sleep_entry.grid(row=0, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg="#E3F2FD")
        btn_frame.pack(pady=15)
        calc_btn = tk.Button(btn_frame, text="Calculate Health Metrics", font=("Arial", 12),
                             bg="#2196F3", fg="white", command=self.calculate_metrics)
        calc_btn.grid(row=0, column=0, padx=10, pady=5)
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12),
                             bg="#9E9E9E", fg="white",
                             command=lambda: controller.show_frame(EnterDetailsPage))
        back_btn.grid(row=0, column=1, padx=10, pady=5)

    def update_data(self):
        # Update the day label based on the current day index.
        current_day = self.controller.week_days[self.controller.current_day_index]
        self.day_label.config(text=current_day)
        # Load saved data if available for this day.
        data = self.controller.weekly_data.get(current_day)
        if data:
            # Restore meal selections.
            for meal, var in self.meal_vars.items():
                value = data.get("meal_selections", {}).get(meal, "Select a dish")
                var.set(value)
            # Set sleep hours.
            self.sleep_entry.delete(0, tk.END)
            self.sleep_entry.insert(0, str(data.get("sleep", "")))
        else:
            # Clear fields if no data exists yet.
            for meal, var in self.meal_vars.items():
                var.set("Select a dish")
            self.sleep_entry.delete(0, tk.END)

    def save_current_day_data(self):
        # Save the current day's meal selections and sleep.
        selections = {}
        total_calories = 0
        for meal, var in self.meal_vars.items():
            selected_dish = var.get()
            selections[meal] = selected_dish
            total_calories += dishes[meal].get(selected_dish, 0)
        try:
            sleep_hours = float(self.sleep_entry.get())
        except ValueError:
            sleep_hours = 0
        current_day = self.controller.week_days[self.controller.current_day_index]
        # Save without computed metrics.
        self.controller.weekly_data[current_day] = {
            "meal_selections": selections,
            "sleep": sleep_hours,
            "total_calories": total_calories
        }

    def prev_day(self):
        self.save_current_day_data()
        self.controller.current_day_index = (self.controller.current_day_index - 1) % len(self.controller.week_days)
        self.update_data()

    def next_day(self):
        self.save_current_day_data()
        self.controller.current_day_index = (self.controller.current_day_index + 1) % len(self.controller.week_days)
        self.update_data()

    def calculate_metrics(self):
        # Gather current data.
        selections = {}
        total_calories = 0
        for meal, var in self.meal_vars.items():
            selected_dish = var.get()
            selections[meal] = selected_dish
            total_calories += dishes[meal].get(selected_dish, 0)
        try:
            sleep_hours = float(self.sleep_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid sleep hours.")
            return

        # Compute the adjusted BMI.
        weight = self.controller.user_details["weight"]
        height = self.controller.user_details["height"]
        bmi = weight / ((height / 100) ** 2)
        age = self.controller.user_details["age"]
        gender = self.controller.user_details.get("gender", "Male")
        if gender == "Male":
            adjusted_bmi = (1.2 * bmi) + (0.23 * age) - 5.4
        else:  # Female
            adjusted_bmi = (1.2 * bmi) + (0.23 * age) - 16.2

        score = (sleep_hours * 10) - (total_calories / 200) - adjusted_bmi
        score = max(0, min(score, 100))

        # Store current day data with computed metrics.
        current_day = self.controller.week_days[self.controller.current_day_index]
        self.controller.weekly_data[current_day] = {
            "meal_selections": selections,
            "sleep": sleep_hours,
            "total_calories": total_calories,
            "bmi": adjusted_bmi,
            "health_score": score
        }
        # Also update global variables so that OutputPage shows current day's metrics.
        self.controller.total_calories = total_calories
        self.controller.bmi = adjusted_bmi
        self.controller.health_score = score

        self.controller.show_frame(OutputPage)


class OutputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E3F2FD")
        self.controller = controller

        title = tk.Label(self, text="Your Health Metrics", font=("Arial", 16, "bold"), bg="#E3F2FD")
        title.pack(pady=10)

        # Display Health Score at the top and adjusted BMI below.
        self.metrics_label = tk.Label(self, font=("Arial", 12), bg="#E3F2FD")
        self.metrics_label.pack(pady=10)

        btn_frame = tk.Frame(self, bg="#E3F2FD")
        btn_frame.pack(pady=15)
        pie_btn = tk.Button(btn_frame, text="View Calorie Distribution", font=("Arial", 12),
                            bg="#4CAF50", fg="white", command=lambda: controller.show_frame(PieChartPage))
        pie_btn.grid(row=0, column=0, padx=10, pady=5)
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12),
                             bg="#9E9E9E", fg="white", command=lambda: controller.show_frame(IntakePage))
        back_btn.grid(row=0, column=1, padx=10, pady=5)
        home_btn = tk.Button(btn_frame, text="Home", font=("Arial", 12),
                             bg="#2196F3", fg="white", command=lambda: controller.show_frame(EnterDetailsPage))
        home_btn.grid(row=0, column=2, padx=10, pady=5)

    def update_data(self):
        health_score = self.controller.health_score
        bmi = self.controller.bmi
        self.metrics_label.config(text=f"Health Score: {health_score:.2f}\nBMI: {bmi:.2f}")


class PieChartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E3F2FD")
        self.controller = controller

        title = tk.Label(self, text="Calorie Distribution", font=("Arial", 16, "bold"), bg="#E3F2FD")
        title.pack(pady=10)

        self.canvas_frame = tk.Frame(self, bg="#E3F2FD")
        self.canvas_frame.pack(pady=10, fill="both", expand=True)

        btn_frame = tk.Frame(self, bg="#E3F2FD")
        btn_frame.pack(pady=15)
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12),
                             bg="#9E9E9E", fg="white", command=lambda: controller.show_frame(OutputPage))
        back_btn.grid(row=0, column=0, padx=10, pady=5)
        home_btn = tk.Button(btn_frame, text="Home", font=("Arial", 12),
                             bg="#2196F3", fg="white", command=lambda: controller.show_frame(EnterDetailsPage))
        home_btn.grid(row=0, column=1, padx=10, pady=5)

    def update_data(self):
        # Clear any existing content.
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        total_calories = self.controller.total_calories
        # Display Total Calories above the chart.
        tk.Label(self.canvas_frame, text=f"Total Calories: {total_calories} kcal",
                 font=("Arial", 12), bg="#E3F2FD").pack(pady=5)
        calorie_intake = {}
        for meal, dish in self.controller.meal_selections.items():
            calorie_intake[meal] = dishes[meal].get(dish, 0) if dish != "Select a dish" else 0

        if all(value == 0 for value in calorie_intake.values()):
            tk.Label(self.canvas_frame, text="No meal data available.",
                     font=("Arial", 12), bg="#E3F2FD").pack()
            return

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        colors = ["#FFB74D", "#4CAF50", "#2196F3"]
        ax.pie(calorie_intake.values(), labels=calorie_intake.keys(),
               autopct='%1.1f%%', colors=colors)
        ax.set_title("Calorie Distribution")
        fig.tight_layout()
        chart = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = HealthTrackerApp()
    app.mainloop()
