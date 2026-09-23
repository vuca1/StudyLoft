document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', event => {

        // get clicked element
        const element = event.target;   

        // add note
        if (element.classList.contains('add-note')) {

            // prevent deafult click handler
            event.preventDefault();
            
            // find each related HTML element
            const url = `/add_note/${element.dataset.jobId}`;
            const form = element.form;
            const formData = new FormData(form);
            
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
    
            
        // remove note
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


        } else if (element.classList.contains('add-subject')) {
            // prevent deafult click handler
            event.preventDefault();

            const url = 'add_subject';
            const form = element.form;
            const formData = new FormData(form);

            fetch(url, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(result => {
                // check if result is valid on server side
                if (result.success) {
                    // insert new subject
                    document.querySelector("#subjects").insertAdjacentHTML(
                        "beforebegin",
                        result.subject_html
                    );
                    // clear form
                    form.reset();
                    // remove "no subjects" message
                    document.querySelector("#no-subjects-message").remove();
                }
            });
        } else if (element.classList.contains("remove-subject")) {

            // prevent default rerouting
            event.preventDefault();

            const subject_id = element.dataset.subjectId;
            const url = `remove_subject/${subject_id}`

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    document.querySelector(`#subject-${subject_id}`).remove();
                }
            });
        }
    });
});