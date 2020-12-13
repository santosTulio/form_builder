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
    $.callbackAdd = (({url,data, success, error})=>{
         $.ajax({
                    url: url,
                    type: 'POST',
                    contentType: 'application/json',
                    dataType: "json",
                    data:JSON.stringify(data),
                    beforeSend: ((xhr, settings) => {xhr.setRequestHeader("X-CSRFToken", csrftoken)}),
                    success: success,
                    error: error
                })
    })
    $.callbackList = (({url, success, error})=>{
         $.ajax({
                    url: url,
                    type: 'GET',
                    contentType: 'application/json',
                    dataType: "json",
                    beforeSend: ((xhr, settings) => {xhr.setRequestHeader("X-CSRFToken", csrftoken)}),
                    success: success,
                    error: error
                })
    })

    $.changeQuestao = function (id, data, action){
        action = action==undefined ?'':'?action='+action
        $.callbackChange({
            url: urlapi+'question/'+id+action,
            data: data,
            success:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
            error:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
        })
    }
    $.changeQuestionario = function ({data}){
        $.callbackChange({
            url: urlapi,
            data: data,
            success:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
            error:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
        })
    }
    $.changeOrAddChoices = function ({id_question, id, data, action}){
        if (id == undefined || id == null) {
            $.callbackAdd({
                url: urlapi + 'question/' + id_question + '/choice/',
                data: data,
                success:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
                error:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
            })
        }else {
            action = action==undefined ?'':('?action='+action)
            $.callbackChange({
                url: urlapi + 'question/' + id_question + '/choice/' + id+action,
                data: data,
                success:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
                error:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
            })
        }
    }
    $.changeSecao = function ({id, data, action}){
        action = action==undefined ?'':('?action='+action)
        $.callbackChange({
            url: urlapi+'section/'+id+action,
            data: data,
            success:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
            error:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
        })
    }
    $.addSecao = function (secao){
        var {id, titulo, descricao, questoes} = secao

        $('<div class="card shadow mx-2 my-2 rounded border-bottom-primary border-left-primary"></div>')
            .append(
                $('<div class="card-body rounded"></div>')
                    .append(
                        $('<div class="d-flex flex-row justify-content-between mb-1"></div>')
                            .append(
                                $('<span class="card-title my-auto">Seção</span>')
                            ).append(
                                $('<div class="bg-light rounded"></div>')
                                    .append(
                                        $('<button class="btn btn-outline-danger border-0 px-3 py-2"></button>')
                                            .append(
                                                $('<i class="ti-trash"></i>')
                                            ).click((e)=>$.changeSecao({id:id,action:'TRASH'}))
                                    ).append(
                                        $('<button class="btn btn-outline-info border-0 px-3 py-2"></button>')
                                            .append(
                                                $('<i class="ti-arrow-up"></i>')
                                            ).click((e)=>$.changeSecao({id:id,action:'UP'}))
                                    ).append(
                                        $('<button class="btn btn-outline-info border-0 px-3 py-2"></button>')
                                            .append(
                                                $('<i class="ti-arrow-down"></i>')
                                            ).click((e)=>$.changeSecao({id:id,action:'DOWN'}))
                                    )
                            )
                    ).append(
                        $('<div class="form-group my-1"></div>')
                            .append(
                                $('<input type="text" class="form-control form-control-lg readonly-focus hidden" onchange="" ' +
                                    'aria-describedby="Titulo da Secão" placeholder="Titulo da Secão"/>')
                                    .val(titulo!=undefined && titulo!=null ? titulo: '')
                                    .change((e)=>{$.changeSecao({id:id,data:{titulo:e.target.value}})})
                            )
                    ).append(
                        $('<div class="form-group my-1"></div>')
                            .append(
                                $('<label class="text-xs font-weight-bold text-gray-800 text-uppercase mb-1 hidden">Descrição</label>')
                            ).append(
                                $('<textarea class="form-control readonly-focus hidden" id="descricao" placeholder="Descrição" >'+(descricao != undefined && descricao != null?descricao:'')+'</textarea>')
                                    .change((e)=>{$.changeSecao({id:id,data:{descricao:e.target.value}})})
                            )
                    )
            ).appendTo($('#main'))
            questoes.map((questao,i)=>{
            $.addPergunta(id,questao)
        })
    }
    $.addPergunta = function (sid,q){
        var {id, pergunta, type, required, params} = q
        let inicio = $('<div class="card card-body bg-white shadow mx-2 my-2 rounded"></div>')
            .append($('<div class="d-flex flex-row justify-content-between mb-1 pergunta"><span class="card-title my-auto">Pergunta</span></div>')
                .append($('<div class="bg-light rounded"></div>')
                    .append($('<button class="btn btn-outline-danger border-0 px-3 py-2"><i class="ti-trash"></i></button>')
                        .click((e)=>$.changeQuestao(id, {}, 'TRASH')))
                    .append($('<button class="btn btn-outline-info border-0 px-3 py-2"><i class="ti-arrow-up"></i></button>')
                        .click((e)=>$.changeQuestao(id,{},'UP')))
                    .append($('<button class="btn btn-outline-info border-0 px-3 py-2"><i class="ti-arrow-down"></i></button>')
                        .click((e)=>$.changeQuestao(id,{},'DOWN')))))
            .append($('<div class="form-group flex-row"></div>')
                .append($('<input type="text" class="form-control hidden" aria-describedby="Pergunta" placeholder="Pergunta" value="'+pergunta+'"/>')
                    .change((e)=>$.changeQuestao(id,{pergunta:e.target.value}))
                ))
            .appendTo('#main')

        var opcao = function () {
            var {choices, multiple, dropdownlist} = params;
            (choices != null? choices:[]).map((choice)=>{
                inicio
                    .append(
                        $('<div class="form-check form-check-inline w-100 my-2"></div>')
                            .append( dropdownlist ? '': multiple? $('<i class="far fa-square mr-2  my-auto"></i>'):$('<i class="far fa-circle mr-2  my-auto"></i>'))
                            .append($('<input type="text" class="form-control hidden my-auto" aria-describedby="Opção" placeholder="Opção">')
                                    .val(choice.rotulo!=null? choice.rotulo:'')
                                    .change((e)=>$.changeOrAddChoices({id_question:id, id:choice.id, data:{rotulo:e.target.value}})))
                            .append($('<div class="d-flex flex-row"></div>')
                                    .append($('<button class="btn btn-outline-danger btn-light rounded-circle border-0 p-2 mx-1"></button>')
                                            .append($('<i class="ti-trash"></i>'))
                                            .click((e)=>$.changeOrAddChoices({id_question:id, id:choice.id,action:'TRASH'})))
                                    .append($('<button class="btn btn-outline-info btn-light rounded-circle border-0 p-2 mx-1"></button>')
                                            .append($('<i class="ti-arrow-up"></i>'))
                                            .click((e)=>$.changeOrAddChoices({id_question:id, id:choice.id,action:'UP'})))
                                    .append($('<button class="btn btn-outline-info btn-light rounded-circle border-0 p-2 mx-1"></button>')
                                            .append($('<i class="ti-arrow-down"></i>'))
                                            .click((e)=>$.changeOrAddChoices({id_question:id, id:choice.id,action:'DOWN'})))))
            })
                inicio
                    .append($('<div class="form-group flex-row"></div>')
                        .append($('<button class="btn btn-primary"><i class="ti-plus"></i> Adicionar Opção</button>')
                            .click(() => $.changeOrAddChoices({id_question:id}))))
                    .append($('<div class="dropdown-divider"></div>'))
                    .append($('<div class="d-md-flex flex-row justify-content-end hidden"></div>')
                        .append($('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                            .append($('<label class="switch my-auto mr-1"></label>')
                                .append($('<input type="checkbox">')
                                    .attr('checked',dropdownlist)
                                    .change((e)=>$.changeQuestao(id, {dropdownlist:!dropdownlist})))
                                .append('<span class="slider round"></span>'))
                            .append('Lista Suspensa'))
                        .append($('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                            .append($('<label class="switch my-auto mr-1"></label>')
                                .append($('<input '+(dropdownlist?'disabled':'')+' type="checkbox">')
                                    .attr('checked',multiple)
                                    .change((e)=>$.changeQuestao(id, {multiple:!multiple})))
                                .append('<span class="slider round"></span>'))
                            .append('Multiplas resposta'))
                        .append($('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                            .append($('<label class="switch my-auto mr-1"></label>')
                                .append($('<input type="checkbox">')
                                    .attr('checked',required)
                                    .change((e)=>$.changeQuestao(id, {required:!required})))
                                .append('<span class="slider round"></span>'))
                            .append('Obrigatória')))
        }
        var numero = function (){
            var {max, min, decimal} = params
            inicio
                .append($('<div class="form-group flex-row"><input type="number" disabled class="form-control readonly bg-light" placeholder="Número"></div>'))
                .append($('<div class="dropdown-divider"></div>'))
                .append($('<div class="form-row"></div>')
                        .append($('<div class="form-group col-md-6"><label for="inputmin">Min</label></div>')
                                .append($('<input type="number" step="0.5" class="form-control"  name="inputmin">')
                                        .val( min !=='undefined' && min !== 'null'?min:0)
                                        .change((e)=>$.changeQuestao(id, {min: e.target.value}))))
                        .append($('<div class="form-group col-md-6"><label for="inputmax">Max</label></div>')
                                    .append($('<input type="number" step="0.5" class="form-control" name="inputmax">')
                                        .val( max !=='undefined' && max !== 'null'? max:0)
                                        .change((e)=> $.changeQuestao(id, {max: e.target.value})))))
                .append($('<div class="d-md-flex flex-row justify-content-end"></div>')
                        .append($('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append($('<label class="switch my-auto mr-1"></label>')
                                        .append($('<input type="checkbox">')
                                            .attr('checked',decimal)
                                            .change((e)=>$.changeQuestao(id,{decimal:!decimal})))
                                        .append('<span class="slider round"></span>'))
                                .append('Decimal'))
                        .append($('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append( $('<label class="switch my-auto mr-1"></label>')
                                        .append($('<input type="checkbox">')
                                            .attr('checked',required)
                                            .change((e)=>$.changeQuestao(id, {required:!required})))
                                        .append('<span class="slider round"></span>'))
                                .append('Obrigatória')))
        }
        var texto = function() {
            var {long} = params
            inicio
                .append($('<div class="form-group flex-row"></div>')
                        .append(long ? $('<textarea disabled class="form-control readonly" placeholder="Resposta Longa"></textarea>'): $('<input type="text" disabled class="form-control readonly" placeholder="Resposta Texto">')))
                .append($('<div class="dropdown-divider"></div>'))
                .append($('<div class="d-md-flex flex-row justify-content-end"></div>')
                        .append($('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append($('<label class="switch my-auto mr-1"></label>')
                                        .append($('<input type="checkbox">')
                                            .attr('checked', long)
                                            .change((e)=>$.changeQuestao(id,{long:!long})))
                                        .append('<span class="slider round"></span>'))
                                .append('Resposta Longo'))
                        .append($('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append($('<label class="switch my-auto mr-1"></label>')
                                        .append($('<input type="checkbox">')
                                            .attr('checked',required)
                                            .change((e)=>$.changeQuestao(id,{required:!required})))
                                        .append('<span class="slider round"></span>'))
                                .append('Obrigatória')))
        }
        switch (type) {
            case 'CHOICES': opcao();
                break;
            case 'NUMBER': numero();
                break;
            case 'TEXT': texto();
                break;
        }
    }

    $('#adicionaritem .adicionar#adicionar').click(function (e) {
        if(!$(this).hasClass('opened')){
            $(this).addClass('opened')
            $(this).find('span').css('display','none')
            $(this).nextAll().css('display','inline')
        }else{
            $(this).removeClass('opened')
            $(this).find('span').css('display','inline')
            $(this).nextAll().css('display','none')
        }
    })
    $('.add-secao').each((ek,obj)=>$(obj).click(()=>{
        $.callbackAdd({
            url: urlapi+'section/',
            data:{},
            success:(es)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
            error:(es)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
        })
    }))
    $('.add-pergunta-opcao').each((e,obj)=>$(obj).click(()=>{
         $.callbackAdd({
            url: urlapi+'question/',
            data:{'type':'RADIO'},
            success:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
            error:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
        })
    }))
    $('.add-pergunta-texto').each((e,obj)=>$(obj).click(()=>{
         $.callbackAdd({
            url: urlapi+'question/',
            data:{'type':'SHORT_ANSWER'},
            success:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
            error:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
        })
    }))
    $('.add-pergunta-numero').each((e,obj)=>$(obj).click(()=>{
        $.callbackAdd({
            url: urlapi+'question/',
            data:{'type':'INTEGER'},
            success:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
            error:(e)=>$.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}}),
        })
    }))


    $.renderFormularioBuilder=({secoes, titulo, descricao, aceitaResposta,mensagemAgradecimento,dataInicio, dataTermino,...other})=>{

        document.getElementById('main').innerHTML=''
        $('#titulo_formulario')
            .val(titulo)
            .unbind('change')
            .change((e)=>$.changeQuestionario({data:{titulo:e.target.value}}))
        $('#descricao_formulario')
            .val(descricao)
            .unbind('change')
            .change((e)=>$.changeQuestionario({data:{descricao:e.target.value}}))

        $('#aceitacao')
            .unbind('change')
            .change((e)=>$.changeQuestionario({data:{aceitaResposta:e.target.checked}}))

        $('#unicaresposta')
            .unbind('change')
            .change((e)=>$.changeQuestionario({data:{unicaResposta:e.target.checked}}))
        $('#mensagemagradecimento')
            .val(mensagemAgradecimento)
            .unbind('change')
            .change((e)=>$.changeQuestionario({data:{mensagemAgradecimento:e.target.value}}))
        secoes.map((secao,i)=>$.addSecao(secao))
    }

    $.callbackList({url:urlapi, success:(e)=>$.renderFormularioBuilder(e),error:(e)=>{}})

})(jQuery)