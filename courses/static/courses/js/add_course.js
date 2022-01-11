$(document).ready(function () {
            disableOldDate();
            let click = 0
            $('#add-lecture').click(function (event) {
                //add new empty form to add lecture
                if (event) {
                    event.preventDefault();
                }
                click = click + 1;
                //$('.empty-form').clone().appendTo('#course-schedule-form');
                $('#course-schedule-form').children().last().clone().appendTo('#course-schedule-form');
                if (click == 1) {
                    let removeBtnHtml = '<button id="remove-lecture" class="btn btn-sm btn-secondary mx-4" type="button">Remove Lecture</button>';
                    $('#add-lecture').after(removeBtnHtml);
                }
            });

            $(document).on('click', '#remove-lecture', function (event) {
                if (event) {
                    event.preventDefault()
                }
                click = click - 1;
                if (click == 0) {
                    $('#remove-lecture').remove();
                }
                $('#course-schedule-form').children().last().remove()
            });

        });

function disableOldDate(){
    let dateToday = new Date();
}