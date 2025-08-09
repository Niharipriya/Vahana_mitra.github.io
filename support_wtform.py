from markupsafe import Markup
from wtforms.widgets import TelInput, TextInput

class IntlTelInput(TextInput):
    """
    A WTForms widget that integrates with the intl-tel-input JavaScript library.
    It automatically formats the phone number to E.164 format on form submission.
    """
    def __init__(self, preferred_countries=None, initial_country="in"):
        """
        Initializes the widget with customization options for the intl-tel-input library.

        :param preferred_countries: A list of country codes (e.g., ['us', 'gb']) to be shown at the top of the dropdown.
        :param initial_country: The country to pre-select in the dropdown. "auto" will detect based on user IP.
        """
        super().__init__()
        self.preferred_countries = preferred_countries or ["us", "gb", "in"]
        self.initial_country = initial_country

    def __call__(self, field, **kwargs):
        """
        Renders the TelInput widget along with the necessary JavaScript for
        the intl-tel-input library.
        """
        # Ensure the id attribute is set for the JavaScript to work
        kwargs.setdefault('id', field.id)

        # Render the basic TelInput field
        html = super().__call__(field, **kwargs)

        # Create the JSON string for preferred countries
        preferred_countries_js = str(self.preferred_countries).replace("'", '"')

        # Construct the script for intl-tel-input
        script = f"""
        <script src="https://cdn.jsdelivr.net/npm/intl-tel-input@19.2.16/build/js/intlTelInput.min.js"></script>
        <script>
        document.addEventListener("DOMContentLoaded", function() {{
            const input = document.getElementById("{field.id}");
            const form = input.closest("form");

            const iti = window.intlTelInput(input, {{
                preferredCountries: {preferred_countries_js},
                separateDialCode: true,
                initialCountry: "{self.initial_country}",
                utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.2.16/build/js/utils.js"
            }});

            if (form) {{
                form.addEventListener("submit", function() {{
                    // Only update the value if it's a valid number
                    if (iti.isValidNumber()) {{
                        input.value = iti.getNumber();
                    }} else {{
                        // Optionally handle invalid numbers, e.g., clear the value
                        input.value = "";
                    }}
                }});
            }}
        }});
        </script>"""
        # Combine the input and the script
        return Markup(f'<div>{html}\n{script}</div>')

class GoogleAddressInput(TextInput):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('class', 'form-control')
        html = super().__call__(field, **kwargs)

        script = f"""
        <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_API_KEY&libraries=places"></script>
        <script>
        document.addEventListener("DOMContentLoaded", function () {{
            var input = document.getElementById("{field.id}");
            if (input) {{
                var autocomplete = new google.maps.places.Autocomplete(input, {{
                    types: ['geocode']
                }});
            }}
        }});
        </script>
        """
        return Markup(f'<div>{html}\n{script}</div>')