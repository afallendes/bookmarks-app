$(function () {

    // Add Bootstrap's form-control class to all visible 'input' elements.
    $('input:not([type=hidden])').addClass('form-control');
    $('textarea:not([type=hidden])').addClass('form-control').attr('rows', '2');


    // Add SelectizeJS to main select element for tags.
    $('select[multiple]#id_tags').selectize({
        plugins: ["remove_button"],
        delimiter: ",",
        persist: false,
        onInitialize() {
            this.extraTags = {} // Helper to keep track of current extra Tags
        },
        create(text) {
            return {
                // add a '**' prefix to the extra tag's slug value as a helper
                // for the backend to differentiate if a tag has to be created
                // or already exists.
                value: '**' + text.slugify(),
                text: text
            }
        },
        sortField: {
            field: 'text',
            direction: 'asc'
        },
        onItemAdd(value, $item) {
            if (value.startsWith('**')) {
                // This function only 'value' directly but not its text. It has
                // to be captured from the DOM $item.
                let text = $item[0].innerText.slice(0, -2);
                this.extraTags[value] = text;
                $("select#extra-tags").append(new Option(
                    text, `${value}|${text}`, true, true
                ));
            }
        },
        onItemRemove(value) {
            let text = this.extraTags[value];
            // This delete logic is required due to the way the 'value' of the
            // extra tags is constructed as a joined pair of value/text string.
            $(`select#extra-tags option[value='${value}|${text}']`).remove();
            delete this.extraTags[`${value}|${text}`]
        }

    })
    

    String.prototype.slugify = function (separator = "-") {
        // Converts a string into its slug equivalent.
        // REF: https://gist.github.com/codeguy/6684588#gistcomment-3974852
        return this
            .toString()
            .normalize('NFD') // splits accented letters into their base letters and the accents
            .replace(/[\u0300-\u036f]/g, '') // removes all previously splitted accents
            .toLowerCase()
            .replace(/[^a-z0-9 -]/g, '') // remove chars that aren't letters, numbers, a single space or '-'
            .trim()
            .replace(/\s+/g, separator);
    };

});
