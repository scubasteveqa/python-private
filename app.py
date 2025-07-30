from shiny import App, reactive, render, ui
import matplotlib.pyplot as plt

# Import from our custom package
# In a real scenario, this would be installed from GitHub
from python_private_package import calculate_fibonacci, generate_data_summary, DataProcessor

# Initialize our data processor
processor = DataProcessor()

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_numeric("fib_n", "Fibonacci number (n):", value=10, min=1, max=50),
        ui.input_text("numbers", "Enter numbers (comma-separated):", value="1,2,3,4,5"),
        ui.input_action_button("process", "Process Data", class_="btn-primary"),
        ui.hr(),
        ui.h4("Package Demo"),
        ui.p("This app demonstrates using a custom GitHub package with functions for:")
    ),
    
    ui.card(
        ui.card_header("Fibonacci Calculator"),
        ui.output_text("fibonacci_result")
    ),
    
    ui.card(
        ui.card_header("Data Summary"),
        ui.output_text("data_summary")
    ),
    
    ui.card(
        ui.card_header("Processed Data Visualization"),
        ui.output_plot("processed_plot")
    ),
    
    ui.card(
        ui.card_header("Processing Statistics"),
        ui.output_text("process_stats")
    )
)

def server(input, output, session):
    # Reactive value to store processed data
    processed_data = reactive.value([])
    
    @render.text
    def fibonacci_result():
        n = input.fib_n()
        if n is None:
            return "Please enter a valid number"
        
        fib_value = calculate_fibonacci(int(n))
        return f"The {n}th Fibonacci number is: {fib_value}"
    
    @render.text
    def data_summary():
        numbers_str = input.numbers()
        if not numbers_str.strip():
            return "Please enter some numbers"
        
        try:
            numbers = [float(x.strip()) for x in numbers_str.split(',') if x.strip()]
            summary = generate_data_summary(numbers)
            
            return f"""
            Data Summary:
            • Count: {summary['count']}
            • Sum: {summary['sum']:.2f}
            • Mean: {summary['mean']:.2f}
            • Min: {summary['min']:.2f}
            • Max: {summary['max']:.2f}
            """
        except ValueError:
            return "Error: Please enter valid numbers separated by commas"
    
    @reactive.effect
    @reactive.event(input.process)
    def _():
        numbers_str = input.numbers()
        if not numbers_str.strip():
            return
        
        try:
            numbers = [float(x.strip()) for x in numbers_str.split(',') if x.strip()]
            # Use our custom package's DataProcessor class
            squared_numbers = processor.process_numbers(numbers)
            processed_data.set(squared_numbers)
        except ValueError:
            processed_data.set([])
    
    @render.plot
    def processed_plot():
        data = processed_data()
        if not data:
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.text(0.5, 0.5, 'Click "Process Data" to see visualization', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_yticks([])
            return fig
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x_values = range(1, len(data) + 1)
        ax.bar(x_values, data, color='skyblue', alpha=0.7)
        ax.set_xlabel('Data Point Index')
        ax.set_ylabel('Squared Value')
        ax.set_title('Processed Data (Squared Values)')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    @render.text
    def process_stats():
        count = processor.get_process_count()
        return f"Total processing operations: {count}"

app = App(app_ui, server)
