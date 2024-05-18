// Please see documentation at https://learn.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.

import * as FilePond from 'filepond';

// Create a multi file upload component
const pond = FilePond.create({
    multiple: true,
    name: 'filepond'
});

// Add it to the DOM
document.body.appendChild(pond.element);
