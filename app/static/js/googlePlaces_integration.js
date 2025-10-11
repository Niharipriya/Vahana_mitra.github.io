
"use strict";

// This loads helper components from the Extended Component Library,
// https://github.com/googlemaps/extended-component-library.
import {APILoader} from 'https://ajax.googleapis.com/ajax/libs/@googlemaps/extended-component-library/0.6.11/index.min.js';

const SHORT_NAME_ADDRESS_COMPONENT_TYPES =
    new Set(['street_number', 'administrative_area_level_1', 'postal_code']);

const ADDRESS_COMPONENT_TYPES_IN_FORM = [
  'location',
  'locality',
  'administrative_area_level_1',
  'postal_code',
  'country',
];

function getFormInputElement(componentType) {
  return document.getElementById(`${componentType}-input`);
}

function getAllLocationInputs() {
  return Array.from(document.querySelectorAll('input')).filter(el => {
    const attr = `${el.id}`.toLowerCase();
    return attr.includes("location") || attr.includes("address");
  });
}

function fillInAddress(place) {
  function getComponentName(componentType) {
    for (const component of place.address_components || []) {
      if (component.types[0] === componentType) {
        return SHORT_NAME_ADDRESS_COMPONENT_TYPES.has(componentType) ?
            component.short_name :
            component.long_name;
      }
    }
    return '';
  }

  function getComponentText(componentType) {
    return (componentType === 'location') ?
        `${getComponentName('street_number')} ${getComponentName('route')}` :
        getComponentName(componentType);
  }

  for (const componentType of ADDRESS_COMPONENT_TYPES_IN_FORM) {
    getFormInputElement(componentType).value = getComponentText(componentType);
  }
}

function fillInCity(place) {
  if (!place || !place.address_components) return '';

  for (const component of place.address_components) {
    if (component.types.includes('locality')) {
      return component.long_name || component.short_name;
    }

    else if (component.types.includes('administrative_area_level_2')) {
      return component.long_name || component.short_name;
    }

  return '';
  }
}

async function initMap() {
  const {Autocomplete} = await APILoader.importLibrary('places');

  const inputs = getAllLocationInputs();

  inputs.forEach(
    (inputEL) => {
      const autocomplete = new Autocomplete(inputEL, {
        componentRestrictions: { country: ["in"] },
        fields: ['address_components', 'geometry', 'name'],
        types: ['address'],
      });

      autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (!place.geometry){
          window.alert(`No details avaiable for input:'${place.name}'`);
          return;
        }
        // fillInAddress(place);
        inputEL.value = fillInCity(place);
      });
    }
  )

}

initMap();
