from shiny import App, ui, render, reactive
import tiny_private_utils as tpu
import numpy as np

app_ui = ui.page_fluid(
    ui.h1("Private Package Demo"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_text("name", "Enter your name:", value="User"),
            ui.input_select(
                "style", 
                "Text style:", 
                choices=["bold", "italic", "code", "normal"]
            ),
            ui.input_slider(
                "num_count", 
                "Number of random values:", 
                min=5, 
                max=50, 
                value=10
            ),
            ui.input_action_button("generate", "Generate Stats")
        ),
        ui.card(
            ui.card_header("Greeting"),
            ui.output_text("greeting")
        ),
        ui.card(
            ui.card_header("Formatted Text"),
            ui.output_ui("formatted_text")
        ),
        ui.card(
            ui.card_header("Statistics"),
            ui.output_text("stats")
        )
    )
)

def server(input, output, session):
    
    @output
    @render.text
    def greeting():
        return tpu.generate_greeting(input.name())
    
    @output
    @render.ui
    def formatted_text():
        sample_text = f"This text is formatted using the '{input.style()}' style"
        formatted = tpu.format_text(sample_text, input.style())
        return ui.HTML(f"<p>{formatted}</p>")
    
    numbers = reactive.value([])
    
    @reactive.effect
    @reactive.event(input.generate)
    def _():
        # Generate random numbers
        numbers.set(np.random.randint(1, 100, input.num_count()))
    
    @output
    @render.text
    def stats():
        if not numbers():
            return "Click 'Generate Stats' to calculate statistics"
        
        stats_dict = tpu.calculate_stats(numbers())
        result = "\n".join([
            f"Count: {stats_dict['count']}",
            f"Sum: {stats_dict['sum']}",
            f"Average: {stats_dict['avg']:.2f}",
            f"Min: {stats_dict['min']}",
            f"Max: {stats_dict['max']}"
        ])
        return result

app = App(app_ui, server)
