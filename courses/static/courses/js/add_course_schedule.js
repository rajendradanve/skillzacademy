$(document).ready(function () {
            
            let click = 0
            $('#add-lecture').click(function (event) {
                //add new empty form to add lecture
                
                click = click + 1;
                
                //cloneMore('.empty-form:last');
                
                
             
                if (click == 1) {
                    let removeBtnHtml = '<button id="remove-lecture" class="btn btn-sm btn-secondary mx-4" type="button">Remove Lecture</button>';
                    $('#add-lecture').after(removeBtnHtml);
                }
            });

            $(document).on('click', '#remove-lecture', function (event) {
               
                click = click - 1;

                if (click == 0) {
                    $('#remove-lecture').remove();
                }
                $('#course-schedule-form').children().last().remove()

                let total = $('#id_form-TOTAL_FORMS').val();
                total--;
                $('#id_form-TOTAL_FORMS').val(total);
            });

        });

function disableOldDate(){
    let dateToday = new Date();
}

function cloneMore(selector){
    let newElement = $(selector).clone(true);
    let total = $('#id_form-TOTAL_FORMS').val();

    newElement.find(':input').each(function(){
        let name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        let id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });

    newElement.find('label').each(function(){
        let newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
        
    });
/*
    newElement.find('div').each(function(){
        let newId = $(this).attr('id').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('id', newId).addClass('form-group col-md-3');
    });
    */
    total++;
    $('#id_form-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}