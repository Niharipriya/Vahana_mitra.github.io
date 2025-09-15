function getAllLocationInputs() {
  return Array.from(document.querySelectorAll('input')).filter(el => {
    const attr = (el.id || el.type == "tel" || el.name).toLowerCase();
    return attr.includes("phone");
  });
}

document.addEventListener("DOMContentLoaded", function() {
  const phoneInputs = getAllLocationInputs();

  phoneInputs.forEach(input => {
    const iti = window.intlTelInput(input, {
      separateDialCode: true,
      initialCountry: "in",
      utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.2.16/build/js/utils.js"
    });

    const form = input.closest("form");
    if (form) {
      form.addEventListener("submit", function() {
        if (iti.isValidNumber()) {
          input.value = iti.getNumber();
        }
      });
    }
  });


});