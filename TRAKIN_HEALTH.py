import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Predefined dishes with calorie values (at least 5 per meal)
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
        # - User details (name, age, weight, height, gender)
        self.user_details = {}
        # - Global metrics for currently selected day.
        self.meal_selections = {}  # Updated in calculate_metrics.
        self.sleep = 0.0
        self.total_calories = 0
        self.bmi = 0
        self.health_score = 0

        # Weekly tracker variables.
        self.week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.current_day_index = 0
        # Instead of (or in addition to) a dictionary we now have an array:
        self.weekly_scores = [0] * len(self.week_days)
        # We still keep a dictionary for per-day details if needed.
        self.weekly_data = {}

        # Container for all pages.
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
        """Raise the frame to the top (update data if needed)."""
        frame = self.frames[cont]
        if hasattr(frame, "update_data"):
            frame.update_data()
        frame.tkraise()


class EnterDetailsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E3F2FD")
        self.controller = controller

        title = tk.Label(
            self,
            text="Enter Your Details",
            font=("Arial", 50, "bold"),
            bg="#A9a9a9",
            fg="#FFFF00",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            borderwidth=5,
            anchor=tk.CENTER,
            cursor="hand2"
        )
        title.pack(pady=10)

        details_frame = tk.Frame(self, bg="#E3F2FD")
        details_frame.pack(pady=10)

        # Name entry.
        tk.Label(details_frame, text="Name:", font=("Arial",38), bg="#E3F2FD",
            ).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(details_frame, font=("Arial",38))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Age entry.
        tk.Label(details_frame, text="Age:", font=("Arial",38), bg="#E3F2FD").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.age_entry = tk.Entry(details_frame, font=("Arial",38))
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        # Weight entry.
        tk.Label(details_frame, text="Weight (kg):", font=("Arial",38), bg="#E3F2FD").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.weight_entry = tk.Entry(details_frame, font=("Arial",38))
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)

        # Height entry.
        tk.Label(details_frame, text="Height (cm):", font=("Arial",38), bg="#E3F2FD").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.height_entry = tk.Entry(details_frame, font=("Arial",38))
        self.height_entry.grid(row=3, column=1, padx=5, pady=5)

        # Gender selection.
        tk.Label(details_frame, text="Gender:", font=("Arial",38), bg="#E3F2FD").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.gender_var = tk.StringVar()
        self.gender_var.set("Male")
        gender_option = tk.OptionMenu(details_frame, self.gender_var, "Male", "Female")
        gender_option.config(font=("Arial",38))
        gender_option.grid(row=4, column=1, padx=5, pady=5)

        button = tk.Button(self, text="Next: Enter Intake", font=("Arial",38),bg="#9e9e9e", fg="white",
        relief=tk.RAISED, borderwidth=5,
         command=self.save_details)
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

        # Display current day name at the top center.
        self.day_label = tk.Label(self, text="", font=("Arial", 43, "bold"), bg="#E3F2FD")
        self.day_label.pack(pady=5)

        # Navigation buttons for previous/next day.
        nav_frame = tk.Frame(self, bg="#E3F2FD")
        nav_frame.pack(pady=5)
        prev_btn = tk.Button(nav_frame, text="Previous Day", font=("Arial",38),
                             bg="#9E9E9E", fg="white",
        relief=tk.RAISED, borderwidth=5, command=self.prev_day)
        prev_btn.pack(side="left", padx=10)
        next_btn = tk.Button(nav_frame, text="Next Day", font=("Arial",38),
                             bg="#9E9E9E", fg="white",relief=tk.RAISED, borderwidth=5, command=self.next_day)
        next_btn.pack(side="left", padx=10)

        title = tk.Label(self, text="Enter Meal Selections & Sleep",
            font=("Arial", 50, "bold"),
            bg="#A9a9a9",
            fg="#FFFF00",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            borderwidth=5,
            anchor=tk.CENTER,
            cursor="hand2")
        title.pack(pady=10)

        # Create dropdowns for meals.
        meals_frame = tk.Frame(self, bg="#E3F2FD")
        meals_frame.pack(pady=10)
        self.meal_vars = {}
        row_index = 0
        for meal in dishes:
            tk.Label(meals_frame, text=f"{meal}:", font=("Arial",38), bg="#E3F2FD")\
                .grid(row=row_index, column=0, sticky="e", padx=5, pady=5)
            var = tk.StringVar()
            var.set("Select a dish")
            option = tk.OptionMenu(meals_frame, var, *list(dishes[meal].keys()))
            option.config(font=("Arial",38))
            option.grid(row=row_index, column=1, padx=5, pady=5)
            self.meal_vars[meal] = var
            row_index += 1

        # Sleep hours entry.
        sleep_frame = tk.Frame(self, bg="#E3F2FD")
        sleep_frame.pack(pady=10)
        tk.Label(sleep_frame, text="Enter Sleep Hours:", font=("Arial",38), bg="#E3F2FD")\
            .grid(row=0, column=0, padx=5, pady=5)
        self.sleep_entry = tk.Entry(sleep_frame, font=("Arial",38))
        self.sleep_entry.grid(row=0, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self, bg="#E3F2FD")
        btn_frame.pack(pady=15)
        calc_btn = tk.Button(btn_frame, text="Calculate Health Metrics", font=("Arial",38),
                             bg="#9E9E9E", fg="white",
        relief=tk.RAISED, borderwidth=5, command=self.calculate_metrics)
        calc_btn.grid(row=0, column=0, padx=10, pady=5)
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 38),
                             bg="#9E9E9E", fg="white", command=lambda: controller.show_frame(EnterDetailsPage))
        back_btn.grid(row=0, column=1, padx=10, pady=5)

    def update_data(self):
        current_day = self.controller.week_days[self.controller.current_day_index]
        self.day_label.config(text=current_day)

        data = self.controller.weekly_data.get(current_day, {})
        meal_selections = data.get("meal_selections", {})
        for meal, var in self.meal_vars.items():
            var.set(meal_selections.get(meal, "Select a dish"))

        self.sleep_entry.delete(0, tk.END)
        self.sleep_entry.insert(0, str(data.get("sleep", "")))

        # Update weekly_scores when the day changes and data exists
        if current_day in self.controller.weekly_data and "health_score" in self.controller.weekly_data[current_day]:
            self.controller.weekly_scores[self.controller.current_day_index] = self.controller.weekly_data[current_day]["health_score"]
        else:
            self.controller.weekly_scores[self.controller.current_day_index] = 0 # Or some default value

    def save_current_day_data(self):
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
        self.controller.weekly_data[current_day] = {
            "meal_selections": selections,
            "sleep": sleep_hours,
            "total_calories": total_calories
        }
        # Save the score if it has been calculated for the current day
        if current_day in self.controller.weekly_data and "health_score" in self.controller.weekly_data[current_day]:
            self.controller.weekly_scores[self.controller.current_day_index] = self.controller.weekly_data[current_day]["health_score"]

    def prev_day(self):
        self.save_current_day_data()
        self.controller.current_day_index = (self.controller.current_day_index - 1) % len(self.controller.week_days)
        self.update_data()

    def next_day(self):
        self.save_current_day_data()
        self.controller.current_day_index = (self.controller.current_day_index + 1) % len(self.controller.week_days)
        self.update_data()

    def calculate_metrics(self):
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

        weight = self.controller.user_details["weight"]
        height = self.controller.user_details["height"]
        bmi = weight / ((height / 100) ** 2)
        age = self.controller.user_details["age"]
        gender = self.controller.user_details.get("gender", "Male")
        # Adjust BMI based on gender.
        if gender == "Male":
            adjusted_bmi = (1.2 * bmi) + (0.23 * age) - 5.4
        else:
            adjusted_bmi = (1.2 * bmi) + (0.23 * age) - 16.2

        score = (sleep_hours * 10) - (total_calories / 200) - adjusted_bmi
        score = max(0, min(score, 100))

        current_day = self.controller.week_days[self.controller.current_day_index]
        # Save the computed metrics in the weekly tracker.
        self.controller.weekly_data[current_day] = {
            "meal_selections": selections,
            "sleep": sleep_hours,
            "total_calories": total_calories,
            "bmi": adjusted_bmi,
            "health_score": score
        }
        # Also update global variables (though these aren't directly used for the weekly report anymore).
        self.controller.meal_selections = selections
        self.controller.total_calories = total_calories
        self.controller.bmi = adjusted_bmi
        self.controller.health_score = score

        # Update the weekly_scores array.
        self.controller.weekly_scores[self.controller.current_day_index] = score

        self.controller.show_frame(OutputPage)

class OutputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E3F2FD")
        self.controller = controller

        title = tk.Label(self, text="Your Health Metrics", font=("Arial", 50, "bold"), bg="#E3F2FD")
        title.pack(pady=10)

        self.metrics_label = tk.Label(self, font=("Arial", 38), bg="#E3F2FD")
        self.metrics_label.pack(pady=10)

        btn_frame = tk.Frame(self, bg="#E3F2FD")
        btn_frame.pack(pady=15)
        pie_btn = tk.Button(btn_frame, text="View Calorie Distribution", font=("Arial", 38),
                            bg="#4CAF50", fg="white", command=lambda: self.controller.show_frame(PieChartPage))
        pie_btn.grid(row=0, column=0, padx=10, pady=5)
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 38),
                             bg="#9E9E9E", fg="white", command=lambda: self.controller.show_frame(IntakePage))
        back_btn.grid(row=0, column=1, padx=10, pady=5)
        home_btn = tk.Button(btn_frame, text="Home", font=("Arial", 38),
                             bg="#2196F3", fg="white", command=lambda: self.controller.show_frame(EnterDetailsPage))
        home_btn.grid(row=0, column=2, padx=10, pady=5)
        # New report button.
        report_btn = tk.Button(btn_frame, text="Weekly Report", font=("Arial", 38),
                               bg="#FF5722", fg="white", command=self.show_weekly_report)
        report_btn.grid(row=0, column=3, padx=10, pady=5)

    def update_data(self):
        health_score = self.controller.health_score
        bmi = self.controller.bmi
        self.metrics_label.config(text=f"Health Score: {health_score:.2f}\nBMI: {bmi:.2f}")

    def show_weekly_report(self):
        # Use the weekly_scores array to plot the bar graph.
        days = self.controller.week_days
        scores = self.controller.weekly_scores  # This array holds a score for each day.
        plt.figure(figsize=(8, 5))
        plt.bar(days, scores, color="#FF5722")
        plt.title("Weekly Health Score Report")
        plt.xlabel("Day")
        plt.ylabel("Health Score")
        plt.ylim(0, 100)
        plt.show()


class PieChartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E3F2FD")
        self.controller = controller

        title = tk.Label(self, text="Calorie Distribution", font=("Arial", 50, "bold"), bg="#E3F2FD")
        title.pack(pady=10)

        self.canvas_frame = tk.Frame(self, bg="#E3F2FD")
        self.canvas_frame.pack(pady=10, fill="both", expand=True)

        btn_frame = tk.Frame(self, bg="#E3F2FD")
        btn_frame.pack(pady=15)
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 38),
                             bg="#9E9E9E", fg="white", command=lambda: self.controller.show_frame(OutputPage))
        back_btn.grid(row=0, column=0, padx=10, pady=5)
        home_btn = tk.Button(btn_frame, text="Home", font=("Arial", 38),
                             bg="#2196F3", fg="white", command=lambda: self.controller.show_frame(EnterDetailsPage))
        home_btn.grid(row=0, column=1, padx=10, pady=5)

    def update_data(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        total_calories = self.controller.total_calories
        tk.Label(self.canvas_frame, text=f"Total Calories: {total_calories} kcal",
                 font=("Arial", 38), bg="#E3F2FD").pack(pady=5)
        calorie_intake = {}
        for meal, dish in self.controller.meal_selections.items():
            calorie_intake[meal] = dishes[meal].get(dish, 0) if dish != "Select a dish" else 0
        if all(value == 0 for value in calorie_intake.values()):
            tk.Label(self.canvas_frame, text="No meal data available.",
                     font=("Arial", 38), bg="#E3F2FD").pack()
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
