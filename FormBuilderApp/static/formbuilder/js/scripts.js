(function ($){
    $.callbackChange = (({url,data, success, error})=>{
         $.ajax({
                    url: url,
                    type: 'PUT',
                    contentType: 'application/json',
                    dataType: "json",
                    data:JSON.stringify(data),
                    beforeSend: ((xhr, settings) => {xhr.setRequestHeader("X-CSRFToken", csrftoken)}),
                    success: success,
                    error: error
                })
    })
    $('.aceitacao').map((i,elem)=>{
        $(elem)
            .change((e)=>{
                $.callbackChange({
                    url: 'api/form/'+e.target.value+'/questions/',
                    data: {aceitaResposta:e.target.checked},
                    success: ((e)=>(e)),
                    error: ((e)=>(e))
                })
            })
    })

})(jQuery)