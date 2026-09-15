document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', event => {

        console.log("entered click event")

        // get clicked element
        const element = event.target;   

        // if element is 'add-note' button
        if (element.classList.contains('add-note')) {

            // prevent deafult click handler
            event.preventDefault();
            
            // find each related HTML element
            const url = `/add_note/${element.dataset.jobId}`;
            const form = element.form;
            const formData = new FormData(form)
            
            fetch(url, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(result => {
                // check if edit was successful on server-side
                if (result.success) {
                    element.form.querySelector('[name="content"]').value = '';
                    document.querySelector('#notes').insertAdjacentHTML(
                        "beforebegin",
                        result.note_html
                    );
                    document.querySelector("#no-notes-message").remove();
                } else {
                    element.form.querySelector('[name="content"]').value = result.content;
                }
            });
        } else if (element.classList.contains('remove-note')) {

            // prevent from default rerouting
            event.preventDefault();

            // find neccessary elements
            const note_id = element.dataset.noteId;
            const url = `/remove_note/${note_id}`

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    document.querySelector(`#note-${note_id}`).remove();
                }
            });
        }

    });
});