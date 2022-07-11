const formId = "survey-form"; // ID of the form
const url = location.href; //  href for the page
const formIdentifier = `${url} ${formId}`; // Identifier used to identify the form
let form = document.querySelector(`#${formId}`); // select form
let formElements = form.elements; // get the elements in the form

/**
 * This function gets the values in the form
 * and returns them as an object with the
 * [formIdentifier] as the object key
 * @returns {Object}
 */

const getFormData = () => {
    let data = {[formIdentifier]: {}};
    for (const element of formElements) {
        if (element.name.length > 0) {
            data[formIdentifier][element.name] = element.value;
        }
    }
    return data;
};


form.addEventListener('change', function () {
    event.preventDefault();
    data = getFormData();
    localStorage.setItem(formIdentifier, JSON.stringify(data[formIdentifier]));
});

/**
 * This function populates the form
 * with data from localStorage
 *
 */
const populateForm = () => {
    if (localStorage.key(formIdentifier)) {
        const savedData = JSON.parse(localStorage.getItem(formIdentifier)); // get and parse the saved data from localStorage
        for (const a of formElements) {
            for (const b of Object.keys(savedData)) {
                if (a.name === b) {
                    a.value = savedData[a.name];
                    break;
                }
            }
        }
    }
};

document.onload = populateForm(); // populate the form when the document is loaded