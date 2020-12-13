(function ($){
    $.checkedSection = (elem)=>{
        $(elem).prevAll().addClass('d-none')
        $(elem).removeClass('d-none')
        $(elem).nextAll().addClass('d-none')
    }

    const section = $("#wizard .section-wizard")

    section.map((i, elem)=>{
         if(i===section.length-1){
            $(elem).append(
                $('<div class="form-group d-flex flex-row '+(section.length===1?'justify-content-end':'justify-content-between')+'"></div>')
                    .append(section.length===1?'':
                        $('<button type="button" class="btn"><span class="text-primary"><i class="ti-arrow-left my-auto"></i> Anterior</span></button>')
                            .click((e)=>$.checkedSection($(elem).prev())))
                    .append($('<button type="submit" class="btn btn-primary"><span>Enviar <i class="far fa-paper-plane"></i></span></button>')))
        }else if(i===0) {
            $(elem)
                .append($('<div class="form-group d-flex flex-row justify-content-end"></div>')
                    .append($('<button type="button" class="btn"><span class="text-primary">Proximo <i class="ti-arrow-right  my-auto"></i></span></button>')
                        .click((e)=>$.checkedSection($(elem).next()))))
        } else{
            $(elem)
                .append($('<div class="form-group d-flex flex-row justify-content-between"></div>')
                    .append($('<button type="button" class="btn"><span class="text-primary"><i class="ti-arrow-left"></i> Anterior</span></button>')
                        .click((e)=>$.checkedSection($(elem).prev())))
                    .append($('<button type="button" class="btn"><span class="text-primary">Proximo <i class="ti-arrow-right"></i></span></button>')
                        .click((e)=>$.checkedSection($(elem).next()))))
        }
          if(i===0){
              $.checkedSection(elem)
          }
    })



    // Custom Steps Jquery Steps
    $('.wizard > .steps li a').click(function(){
    	$(this).parent().addClass('checked');
		$(this).parent().prevAll().addClass('checked');
		$(this).parent().nextAll().removeClass('checked');
    });
    // Custom Button Jquery Steps
    $('.forward').click(function(){
    	$("#wizard").steps('next');
    })
    $('.backward').click(function(){
        $("#wizard").steps('previous');
    })
    // Checkbox
    $('.checkbox-circle label').click(function(){
        $('.checkbox-circle label').removeClass('active');
        $(this).addClass('active');
    })
}
)(jQuery)