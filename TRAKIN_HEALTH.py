import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Predefined dishes with calorie values (5+ options per meal)
dishes = {
    "Breakfast": {
        "Select a dish": 0,
        "Idli (2 pcs)": 300,
        "Upma": 132,
        "Aloo Paratha": 300,
        "Poha": 250,
        "Dosa": 152,
        "Scrambled Eggs": 107,
        "Toasted white bread": 64,
        "Chole Bhature": 600,
        "Paneer Sandwich": 350,
        "Thepla (2 pcs,with Pickle & Curd)": 300
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

        # Shared data: user details, meal selections, sleep, computed metrics.
        self.user_details = {}
        self.meal_selections = {}
        self.sleep = 0.0
        self.total_calories = 0
        self.bmi = 0
        self.health_score = 0

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
        tk.Label(details_frame, text="Name:", font=("Arial", 12), bg="#E3F2FD") \
            .grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Age
        tk.Label(details_frame, text="Age:", font=("Arial", 12), bg="#E3F2FD") \
            .grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.age_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.age_entry.grid(row=1, column=1, padx=5, pady=5)

        # Weight
        tk.Label(details_frame, text="Weight (kg):", font=("Arial", 12), bg="#E3F2FD") \
            .grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.weight_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)

        # Height
        tk.Label(details_frame, text="Height (cm):", font=("Arial", 12), bg="#E3F2FD") \
            .grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.height_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.height_entry.grid(row=3, column=1, padx=5, pady=5)

        button = tk.Button(self, text="Next: Enter Intake", font=("Arial", 12),
                           bg="#2196F3", fg="white", command=self.save_details)
        button.pack(pady=15)

    def save_details(self):
        try:
            name = self.name_entry.get().strip()
            age = int(self.age_entry.get())
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if not name:
                messagebox.showerror("Error", "Please enter your name.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for age, weight, and height.")
            return

        # Save details in the main controller and move to the Intake page
        self.controller.user_details = {"name": name, "age": age, "weight": weight, "height": height}
        self.controller.show_frame(IntakePage)


class IntakePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E3F2FD")
        self.controller = controller

        title = tk.Label(self, text="Enter Meal Selections & Sleep", font=("Arial", 16, "bold"), bg="#E3F2FD")
        title.pack(pady=10)

        # Create meal selection dropdowns
        meals_frame = tk.Frame(self, bg="#E3F2FD")
        meals_frame.pack(pady=10)
        self.meal_vars = {}
        row_index = 0
        for meal in dishes:
            tk.Label(meals_frame, text=f"{meal}:", font=("Arial", 12), bg="#E3F2FD") \
                .grid(row=row_index, column=0, sticky="e", padx=5, pady=5)
            var = tk.StringVar()
            var.set("Select a dish")
            option = tk.OptionMenu(meals_frame, var, *list(dishes[meal].keys()))
            option.config(font=("Arial", 12))
            option.grid(row=row_index, column=1, padx=5, pady=5)
            self.meal_vars[meal] = var
            row_index += 1

        # Sleep hours entry
        sleep_frame = tk.Frame(self, bg="#E3F2FD")
        sleep_frame.pack(pady=10)
        tk.Label(sleep_frame, text="Enter Sleep Hours:", font=("Arial", 12), bg="#E3F2FD") \
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

    def calculate_metrics(self):
        # Save meal choices and sleep hours
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

        self.controller.meal_selections = selections
        self.controller.sleep = sleep_hours

        # Compute BMI
        weight = self.controller.user_details["weight"]
        height = self.controller.user_details["height"]
        bmi = weight / ((height / 100) ** 2)
        self.controller.bmi = bmi
        self.controller.total_calories = total_calories

        # Compute Health Score using a revised formula
        score = (sleep_hours * 10) - (total_calories / 200) - bmi
        score = max(0, min(score, 100))
        self.controller.health_score = score

        self.controller.show_frame(OutputPage)


class OutputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E3F2FD")
        self.controller = controller

        title = tk.Label(self, text="Your Health Metrics", font=("Arial", 16, "bold"), bg="#E3F2FD")
        title.pack(pady=10)

        self.metrics_label = tk.Label(self, font=("Arial", 12), bg="#E3F2FD")
        self.metrics_label.pack(pady=10)

        btn_frame = tk.Frame(self, bg="#E3F2FD")
        btn_frame.pack(pady=15)
        pie_btn = tk.Button(btn_frame, text="View Calorie Distribution", font=("Arial", 12),
                            bg="#4CAF50", fg="white",
                            command=lambda: controller.show_frame(PieChartPage))
        pie_btn.grid(row=0, column=0, padx=10, pady=5)
        back_btn = tk.Button(btn_frame, text="Back", font=("Arial", 12),
                             bg="#9E9E9E", fg="white",
                             command=lambda: controller.show_frame(IntakePage))
        back_btn.grid(row=0, column=1, padx=10, pady=5)
        home_btn = tk.Button(btn_frame, text="Home", font=("Arial", 12),
                             bg="#2196F3", fg="white",
                             command=lambda: controller.show_frame(EnterDetailsPage))
        home_btn.grid(row=0, column=2, padx=10, pady=5)

    def update_data(self):
        bmi = self.controller.bmi
        total_calories = self.controller.total_calories
        health_score = self.controller.health_score
        self.metrics_label.config(
            text=f"BMI: {bmi:.2f}\nTotal Calories: {total_calories} kcal\nHealth Score: {health_score:.2f}"
        )


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
                             bg="#9E9E9E", fg="white",
                             command=lambda: controller.show_frame(OutputPage))
        back_btn.grid(row=0, column=0, padx=10, pady=5)
        home_btn = tk.Button(btn_frame, text="Home", font=("Arial", 12),
                             bg="#2196F3", fg="white",
                             command=lambda: controller.show_frame(EnterDetailsPage))
        home_btn.grid(row=0, column=1, padx=10, pady=5)

    def update_data(self):
        # Clear any existing chart
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        calorie_intake = {}
        for meal, dish in self.controller.meal_selections.items():
            if dish == "Select a dish":
                calorie_intake[meal] = 0
            else:
                calorie_intake[meal] = dishes[meal].get(dish, 0)

        if all(value == 0 for value in calorie_intake.values()):
            tk.Label(self.canvas_frame, text="No meal data available.",
                     font=("Arial", 12), bg="#E3F2FD").pack()
            return

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        colors = ["#FFB74D", "#4CAF50", "#2196F3"]
        ax.pie(calorie_intake.values(), labels=calorie_intake.keys(), autopct='%1.1f%%', colors=colors)
        ax.set_title("Calorie Distribution")
        fig.tight_layout()

        chart = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = HealthTrackerApp()
    app.mainloop()
