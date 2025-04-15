import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

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
        "Regular white bread toast ": 64,
        "Chole Bhature (1 plate) " :600,
        "Paneer Sandwich (2 slices)	":350,
        "Thepla with Pickle & Curd (2 pcs)":300
    },
    "Lunch": {
        "Select a dish": 0,
        "Rice with Sambar & Rasam": 500,
        "South Indian Veg Thali	": 650,
        "Fish Curry with Rice	": 600,
        "Lemon Rice with Papad	": 450,
        "Roti (2) with Dal & Sabzi	": 450,
        "Rajma Chawal (1 plate)	": 550,
        "Chole Chawal (1 plate)	":550,
        "Paneer Butter Masala with Naan	":700,
        "Stuffed Paratha (2) with Curd	": 500
    },
    "Dinner": {
        "Select a dish": 0,
        "Chapati with Veg Kurma (2 pcs)	": 400,
        "Dosa with Chutney (1 large)	": 350,
        "Roti (2) with Palak Paneer	": 450,
        "Dal Tadka with Jeera Rice	": 500,
        "Aloo Gobi with Chapati (2)	": 450,
        "Kadhi Chawal (1 bowl)	": 500,
        "Litti Chokha (2 pcs)":550
    }
}


class HealthTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Tracker")
        self.root.geometry("500x600")
        self.root.configure(bg="#E3F2FD")

        # User Details Frame
        details_frame = tk.Frame(root, bg="#E3F2FD")
        details_frame.pack(pady=10)

        tk.Label(details_frame, text="Enter Your Details",
                 font=("Arial", 16, "bold"), bg="#E3F2FD") \
            .grid(row=0, column=0, columnspan=2, pady=5)

        # Name
        tk.Label(details_frame, text="Name:", font=("Arial", 12), bg="#E3F2FD") \
            .grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Age
        tk.Label(details_frame, text="Age:", font=("Arial", 12), bg="#E3F2FD") \
            .grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.age_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.age_entry.grid(row=2, column=1, padx=5, pady=5)

        # Weight
        tk.Label(details_frame, text="Weight (kg):", font=("Arial", 12), bg="#E3F2FD") \
            .grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.weight_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)

        # Height
        tk.Label(details_frame, text="Height (cm):", font=("Arial", 12), bg="#E3F2FD") \
            .grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.height_entry = tk.Entry(details_frame, font=("Arial", 12))
        self.height_entry.grid(row=4, column=1, padx=5, pady=5)

        # Meal Selection Frame
        meals_frame = tk.Frame(root, bg="#E3F2FD")
        meals_frame.pack(pady=10)

        tk.Label(meals_frame, text="Select Your Meals",
                 font=("Arial", 16, "bold"), bg="#E3F2FD") \
            .grid(row=0, column=0, columnspan=2, pady=5)

        # Create dropdowns (OptionMenus) for each meal
        self.meal_vars = {}  # store StringVar for each meal
        row_index = 1
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

        # Sleep Hours Entry Frame
        sleep_frame = tk.Frame(root, bg="#E3F2FD")
        sleep_frame.pack(pady=10)
        tk.Label(sleep_frame, text="Enter Sleep Hours:",
                 font=("Arial", 16, "bold"), bg="#E3F2FD") \
            .grid(row=0, column=0, padx=5, pady=5)
        self.sleep_entry = tk.Entry(sleep_frame, font=("Arial", 12))
        self.sleep_entry.grid(row=0, column=1, padx=5, pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(root, bg="#E3F2FD")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Calculate Health Score",
                  command=self.calculate_health_score,
                  bg="#2196F3", fg="white", font=("Arial", 12)) \
            .grid(row=0, column=0, padx=10, pady=5)
        tk.Button(btn_frame, text="Show Calorie Distribution",
                  command=self.plot_calorie_distribution,
                  bg="#4CAF50", fg="white", font=("Arial", 12)) \
            .grid(row=0, column=1, padx=10, pady=5)

    def calculate_health_score(self):
        try:
            # Get sleep and user physical details
            sleep_hours = float(self.sleep_entry.get())
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            # Calculate BMI
            bmi = weight / ((height / 100) ** 2)

            # Calculate total calories from meal selections
            total_calories = 0
            for meal, var in self.meal_vars.items():
                dish_selected = var.get()
                calories = dishes[meal].get(dish_selected, 0)
                total_calories += calories

            # Health Score Formula (revise as needed)
            score = (sleep_hours * 10) - (total_calories / 200) - bmi
            score = max(0, min(score, 100))

            messagebox.showinfo("Health Metrics",
                                f"Your BMI: {bmi:.2f}\n"
                                f"Total Calories: {total_calories} kcal\n"
                                f"Your Health Score: {score:.2f}")
        except ValueError:
            messagebox.showerror("Error",
                                 "Please enter valid numeric details for sleep, weight, and height.")

    def plot_calorie_distribution(self):
        # Gather calorie data from meal selections
        calorie_intake = {}
        for meal, var in self.meal_vars.items():
            dish_selected = var.get()
            if dish_selected == "Select a dish":
                calorie_intake[meal] = 0
            else:
                calorie_intake[meal] = dishes[meal].get(dish_selected, 0)

        if all(value == 0 for value in calorie_intake.values()):
            messagebox.showerror("Error", "No meals selected!")
            return

        plt.figure(figsize=(6, 6))
        colors = ["#FFB74D", "#4CAF50", "#2196F3"]
        plt.pie(calorie_intake.values(), labels=calorie_intake.keys(),
                autopct='%1.1f%%', colors=colors)
        plt.title("Calorie Intake Distribution")
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthTrackerApp(root)
    root.mainloop()