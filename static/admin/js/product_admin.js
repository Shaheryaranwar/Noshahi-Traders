(function ($) {
    'use strict';

    console.log("✅ product_admin.js loaded");

    $(function () {

        const fields = {
            chest: $('.form-row.field-chest_width'),
            shoulder: $('.form-row.field-shoulder_width'),
            waist: $('.form-row.field-waist_width'),
            length: $('.form-row.field-length'),
        };

        const RULES = {
            // Upper wear
            mens_tshirt: ['chest', 'shoulder', 'length'],
            mens_shirt: ['chest', 'shoulder', 'length'],
            mens_kurta: ['chest', 'shoulder', 'length'],
            mens_hoodie: ['chest', 'shoulder', 'length'],
            mens_jacket: ['chest', 'shoulder', 'length'],
            mens_coat: ['chest', 'shoulder', 'length'],
            mens_sweater: ['chest', 'shoulder', 'length'],

            // Bottom wear
            mens_trouser: ['waist', 'length'],
            mens_jeans: ['waist', 'length'],
            mens_short: ['waist', 'length'],

            // Shoes (NO measurements)
            mens_shoes: [],
            womens_shoes: [],
            kids_shoes: [],
        };

        function hideAll() {
            Object.values(fields).forEach(f => f.hide());
        }

        function toggleMeasurements() {
            const type = $('#id_product_type').val();
            hideAll();

            if (!type || !(type in RULES)) return;

            RULES[type].forEach(f => fields[f].show());
        }

        // Initial run
        toggleMeasurements();

        // On change
        $(document).on('change', '#id_product_type', toggleMeasurements);
    });

})(django.jQuery);
