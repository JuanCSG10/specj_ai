import flet as ft

from specj_ai.specj_ai_context import MolecularPropertyPredictor
from specj_ai.load_strategies import load_strategy
from specj_ai.enums.prediction_configuration import PredictionConfiguration


DEFAULT_EXP_FEATURES = {
    "Absorption max (eV)": [],
    "Emission max (eV)": [],
    "log(e/mol-1 dm3 cm-1)": [],
}


def main(page: ft.Page):
    page.title = "SpecJAI Molecular Property Predictor"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 900
    page.padding = 20
    page.scroll = "auto"

    # App state
    selected_system = None
    selected_subsystem = None
    selected_feature_set = None
    exp_feature_controls = {}

    # Principal controls
    molecule_input = ft.TextField(
        label="Chromophore SMILE",
        hint_text="Type chromophore SMILE",
        width=600,
        multiline=True,
    )

    solvent_input = ft.TextField(
        label="Solvent SMILE",
        hint_text="Type solvent SMILE",
        width=600,
    )

    system_dropdown = ft.Dropdown(
        label="Property",
        width=300,
        options=[
            ft.dropdown.Option(key=key, text=key)
            for key in PredictionConfiguration.CONFIG.value.keys()
        ],
    )

    subsystem_dropdown = ft.Dropdown(
        label="Subsystem", width=300, options=[], disabled=True
    )

    feature_set_dropdown = ft.Dropdown(
        label="Feature set", width=300, options=[], disabled=True
    )

    exp_features_container = ft.Container(
        content=ft.Column([], tight=True), padding=10, visible=False
    )

    # Container to show results
    results_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "The inference results will appear here.",
                    style=ft.TextStyle(italic=True, color=ft.colors.GREY_600),
                )
            ]
        ),
        padding=15,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        margin=ft.margin.only(top=20),
        bgcolor=ft.colors.BLUE_50,
        width=600,
        visible=True,
    )

    # Progress bar
    progress_bar = ft.ProgressBar(visible=False, width=600)

    # Function to update subsystems
    def update_subsystems(e):
        nonlocal selected_system
        selected_system = system_dropdown.value

        if selected_system:
            subsystems = PredictionConfiguration.CONFIG.value[selected_system][
                "subsystems"
            ].keys()
            subsystem_dropdown.options = [
                ft.dropdown.Option(key=subsys, text=subsys) for subsys in subsystems
            ]
            subsystem_dropdown.value = None
            subsystem_dropdown.disabled = False

            # Reset susbsytems
            feature_set_dropdown.options = []
            feature_set_dropdown.value = None
            feature_set_dropdown.disabled = True
            exp_features_container.visible = False
            exp_features_container.content = ft.Column([], tight=True)
        else:
            subsystem_dropdown.options = []
            subsystem_dropdown.disabled = True

        page.update()

    # Function to update params
    def update_feature_sets(e):
        nonlocal selected_subsystem
        selected_subsystem = subsystem_dropdown.value

        if selected_subsystem and selected_system:
            feature_sets = PredictionConfiguration.CONFIG.value[selected_system][
                "subsystems"
            ][selected_subsystem]["feature_sets"].keys()
            feature_set_dropdown.options = [
                ft.dropdown.Option(key=fs, text=fs) for fs in feature_sets
            ]
            feature_set_dropdown.value = None
            feature_set_dropdown.disabled = False

            # Resetear feature_sets dependientes
            exp_features_container.visible = False
            exp_features_container.content = ft.Column([], tight=True)
        else:
            feature_set_dropdown.options = []
            feature_set_dropdown.disabled = True

        page.update()

    # Función para actualizar los campos de experimental_features
    def update_exp_features(e):
        nonlocal selected_feature_set, exp_feature_controls
        selected_feature_set = feature_set_dropdown.value

        if selected_feature_set == "mordred_solv":
            exp_feature_controls = {}
            feature_inputs = []

            for feature_name in DEFAULT_EXP_FEATURES.keys():
                feature_label = ft.Text(feature_name, size=16)
                feature_input = ft.TextField(
                    hint_text=f"Value for {feature_name}", width=400
                )
                exp_feature_controls[feature_name] = feature_input

                feature_inputs.append(
                    ft.Column([feature_label, feature_input], spacing=5)
                )

            exp_features_container.content = ft.Column(feature_inputs, tight=True)
            exp_features_container.visible = True
        else:
            exp_features_container.visible = False

        page.update()

    # Función para realizar la predicción
    def make_prediction(e):
        # Mostrar barra de progreso
        progress_bar.visible = True
        page.update()

        try:
            # Verificar entradas
            if not molecule_input.value:
                display_result("Error: Type a valid chromophore SMILE", is_error=True)
                return

            if not solvent_input.value:
                display_result("Error: Type a solvent SMILE", is_error=True)
                return

            if not all([selected_system, selected_subsystem, selected_feature_set]):
                display_result(
                    "Error: Choose all the configuration options", is_error=True
                )
                return

            # Preparar los datos experimentales si es necesario
            experimental_features = {}
            if selected_feature_set == "mordred_solv":
                for feature_name, control in exp_feature_controls.items():
                    values = []
                    if control.value:
                        try:
                            # Intentar interpretar como lista de valores separados por coma
                            value_str = control.value.strip()
                            if value_str:
                                for val in value_str.split(","):
                                    values.append(float(val.strip()))
                        except ValueError:
                            display_result(
                                f"Error: Invalid value for {feature_name}",
                                is_error=True,
                            )
                            return
                    experimental_features[feature_name] = values

            # Cargar el predictor
            predictor = MolecularPropertyPredictor(
                *load_strategy(
                    selected_system, selected_subsystem, selected_feature_set
                )
            )
            # Realizar predicción
            predictions = predictor.predict(
                molecule_input.value,
                solvent_input.value,
                experimental_features if selected_feature_set == "mordred_solv" else {},
            )

            # Mostrar resultados
            result_content = []
            result_content.append(
                ft.Text(
                    "Inference result:",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLUE_700,
                )
            )

            for value in predictions:
                result_content.append(
                    ft.Text(f"{round(value,3)}", selectable=True, size=16)
                )

            # Actualizar el contenedor de resultados
            results_container.content = ft.Column(result_content, spacing=10)
            results_container.bgcolor = ft.colors.BLUE_50
            results_container.visible = True

        except Exception as e:
            display_result(f"Error in inference procedure: {str(e)}", is_error=True)

        # Ocultar barra de progreso
        progress_bar.visible = False
        page.update()

    # Función para mostrar resultados o errores
    def display_result(message, is_error=False):
        color = ft.colors.RED_50 if is_error else ft.colors.BLUE_50
        text_color = ft.colors.RED_700 if is_error else ft.colors.BLUE_700

        icon = ft.Icon(
            name=ft.icons.ERROR if is_error else ft.icons.CHECK_CIRCLE,
            color=text_color,
            size=24,
        )

        results_container.bgcolor = color
        results_container.content = ft.Column(
            [
                ft.Row(
                    [
                        icon,
                        ft.Text(
                            "Error" if is_error else "Inference",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=text_color,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Text(message, selectable=True),
            ],
            spacing=10,
        )

        results_container.visible = True
        progress_bar.visible = False
        page.update()

    # Conectar eventos
    system_dropdown.on_change = update_subsystems
    subsystem_dropdown.on_change = update_feature_sets
    feature_set_dropdown.on_change = update_exp_features

    # Botón de predicción
    predict_button = ft.ElevatedButton(
        "Predict",
        on_click=make_prediction,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_600,
        ),
        icon=ft.icons.SCIENCE,
    )

    # Botón para limpiar los resultados
    def clear_results(e):
        results_container.content = ft.Column(
            [
                ft.Text(
                    "The inference results will appear here.",
                    style=ft.TextStyle(italic=True, color=ft.colors.GREY_600),
                )
            ]
        )
        results_container.bgcolor = ft.colors.BLUE_50
        page.update()

    clear_button = ft.OutlinedButton(
        "Clean results", on_click=clear_results, icon=ft.icons.CLEANING_SERVICES
    )

    # Construir la interfaz
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Molecular property predictor",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_800,
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Input data",
                                    size=20,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.colors.BLUE_700,
                                ),
                                molecule_input,
                                solvent_input,
                            ]
                        ),
                        padding=10,
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.colors.BLACK12,
                            offset=ft.Offset(0, 2),
                        ),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Model configuration",
                                    size=20,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.colors.BLUE_700,
                                ),
                                ft.Row(
                                    [system_dropdown],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    [subsystem_dropdown],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    [feature_set_dropdown],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ]
                        ),
                        padding=10,
                        margin=ft.margin.only(top=15),
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.colors.BLACK12,
                            offset=ft.Offset(0, 2),
                        ),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Experimental features (optional)",
                                    size=20,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.colors.BLUE_700,
                                ),
                                exp_features_container,
                            ]
                        ),
                        padding=10,
                        margin=ft.margin.only(top=15),
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.colors.BLACK12,
                            offset=ft.Offset(0, 2),
                        ),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [predict_button, clear_button],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                                progress_bar,
                            ]
                        ),
                        margin=ft.margin.only(top=20),
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Results",
                                    size=20,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.colors.BLUE_700,
                                ),
                                results_container,
                            ]
                        ),
                        padding=10,
                        margin=ft.margin.only(top=15),
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.colors.BLACK12,
                            offset=ft.Offset(0, 2),
                        ),
                    ),
                ]
            ),
            padding=20,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
