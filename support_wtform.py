from wtforms.widgets import TelInput, TextInput
from markupsafe import Markup

class IntlTelInput(TelInput):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('class', 'form-control')  # Add Bootstrap or custom class

        html = super().__call__(field, **kwargs)

        script = f"""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/css/intlTelInput.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/intlTelInput.min.js"></script>
        <script>
        document.addEventListener("DOMContentLoaded", function () {{
            var input = document.querySelector("#{field.id}");
            var form = input.closest("form");

            var iti = window.intlTelInput(input, {{
                preferredCountries: ["in", "us", "gb"],
                separateDialCode: true,
                initialCountry: "in",
                utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js"
            }});

            form.addEventListener("submit", function () {{
                input.value = iti.getNumber(); // sets E.164 format
            }});
        }});
        </script>"""
        return  Markup(f'<div>{html}\n{script}</div>')

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