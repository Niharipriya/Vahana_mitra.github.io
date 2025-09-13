function getAllLocationInputs() {
  return Array.from(document.querySelectorAll('input')).filter(el => {
    const attr = `${el.id}`.toLowerCase();
    return attr.includes("phone");
  });
}

document.addEventListener("DOMContentLoaded", function() {
  const input = document.getElementById("phone");

  const iti = window.intlTelInput(input, {
    separateDialCode: true,
    initialCountry: "in",
    strictMode: true,
    utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@19.2.16/build/js/utils.js"
  });

  // if (form) {
  //   form.addEventListener("submit", function() {
  //     // Only update the value if it's a valid number
  //     if (iti.isValidNumber()) {
  //       input.value = iti.getNumber();
  //     } else {
  //     // Optionally handle invalid numbers, e.g., clear the value
  //       input.value = "";
  //     }
  //   });
  // }
});