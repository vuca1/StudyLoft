document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', event => {

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
                    document.querySelector('#notes').insertAdjacentHTML(
                        "beforebegin",
                        result.note_html
                    );       
                } else {
                    element.form.querySelector('[name="content"]').value = result.content;
                }
            });
        }

    });
});