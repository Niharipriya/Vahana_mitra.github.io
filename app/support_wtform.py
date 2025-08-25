from markupsafe import Markup
from wtforms.widgets import TelInput, TextInput
from wtforms.widgets import html_params 

class IntlTelInput(TelInput):
    """
    A WTForms widget that integrates with the intl-tel-input JavaScript library.
    It automatically formats the phone number to E.164 format on form submission.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('type', 'tel')
        html = super().__call__(field, **kwargs)
        print(html)
        preferred_countries_js = str(["us", "gb", "in"]).replace("'", '"')

        script = f"""
        <script src="https://cdn.jsdelivr.net/npm/intl-tel-input@19.2.16/build/js/intlTelInput.min.js"></script>
        <script>
        document.addEventListener("DOMContentLoaded", function() {{
            const input = document.getElementById("{field.id}");
            const form = input.closest("form");
            input.classList.add("form-control")

            const iti = window.intlTelInput(input, {{
                preferredCountries: {preferred_countries_js},
                separateDialCode: true,
                initialCountry: "in",
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
        return Markup(f'<div class="form-group">{html}\n{script}</div>  ')

class GoogleAutocomplete(TextInput):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class', 'form-control')
        html = f'<gmp-place-autocomplete {html_params(id=field.id, type="geocode")}></gmp-place-autocomplete>'

        
        script = """
            <script>
              document.addEventListener("DOMContentLoaded", function () {""" + f"const autocompleteElement = document.getElementById({field.id});"
        script = script + """
                // Listen for the place change event
                autocompleteElement.addEventListener("gmp-placechange", () => {
                  const place = autocompleteElement.value;
                  console.log("Selected place:", place);
                });
              });
            </script>
        """
        print(Markup(html+script))
        return Markup(html+script)

class GoogleAddressInput(TextInput):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('class', 'form-control')
        html = super().__call__(field, **kwargs)
 
        script = f"""
        <script>

        document.addEventListener("DOMContentLoaded", function () {{
            var input = document.getElementById("{field.id}");
            if (input) {{
                const autocomplete = new google.maps.places.PlaceAutocompleteElement();
                autocomplete.input = input;
            }}
        }});
        </script>
        """
        return Markup(f'<div>{html}\n{script}</div>')
        # <script>
        #   document.addEventListener("DOMContentLoaded", function () {{
        #     const autocompleteElement = document.getElementById("{field.id}");

        #     // Listen for the place change event
        #     autocompleteElement.addEventListener("change", () => {{
        #       autocompleteElement.value = new google.maps.places.PlaceAutocompleteElement(autocompleteElement, {{
        #         types: ['geocode']
        #       }});
        #       console.log("Selected place:", place);
        #     }});
        #   }});
        # </script>