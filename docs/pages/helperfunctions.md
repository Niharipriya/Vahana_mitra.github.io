- ```javascript
  /**
   * Returns all input elements whose ID contains "location" or "address".
   * Useful for binding Google Maps Autocomplete to multiple fields.
   *
   * @returns {HTMLInputElement[]} Array of matching input elements.
   */
  function getAllLocationInputs(){ ... }
  ```
- ```javascript
  /**
   * Autofills an input with the corresponding address component
   * (state, city, area, postal code) based on its ID.
   *
   * @param {HTMLInputElement} input  Target input element.
   * @param {object} places           Place object from the Google Places API.
   */
  function fillInAddress(input, places) { ... }
  ```