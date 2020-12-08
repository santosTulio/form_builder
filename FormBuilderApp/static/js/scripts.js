(function ($){
    const questionario = []


    $.callbackUp = function ({id, posicao}){
                return function (){
                    //if(posicao)
                    //var swap = questionario[posicao]
                    //if questionario[posicao]
                }
            }
    $.callbackDown = function ({id}){
                return function (){

                }
            }
    $.callbackDelete = function (){
                    $.ajax({
                    url: urlapi+'delete/section/'+id,
                    type: 'DELETE',
                    contentType: 'application/json',
                    dataType: "json",
                    beforeSend: function (xhr, settings) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    },
                    data:JSON.stringify({'message':'new section'}),
                    success: function (secao) {
                        GetQuestionario()
                    },
                    error: function (data) {
                        console.log(data)
                    }
                })
            }
    $.changeSecaoTitulo = function ({id,value}){
        $.callbackChange({
            url: urlapi+'update/section/'+id,
            data: {titulo:value},
            success: ((e)=>{GetQuestionario}),
            error: ((e)=>{GetQuestionario})
        })
    }
    $.changeSecaoDescricao = function ({id,value}){
        $.callbackChange({
            url: urlapi+'update/section/'+id,
            data: {descricao:value},
            success: ((e)=>{GetQuestionario}),
            error: ((e)=>{GetQuestionario})
        })
    }

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

    $.addSecao = function (secao){
        console.log(secao)
        var {id, titulo, descricao, posicao, onUp, onDown, onDelete, onChangeTitulo, onChangeDescricao, questoes} = secao
        var id_secao ='secao-'+id+'-titulo'

        console.log(descricao)

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
                                            ).click(()=>callbackDelete())
                                    ).append(
                                        $('<button class="btn btn-outline-info border-0 px-3 py-2"></button>')
                                            .append(
                                                $('<i class="ti-arrow-up"></i>')
                                            )
                                    ).append(
                                        $('<button class="btn btn-outline-info border-0 px-3 py-2"></button>')
                                            .append(
                                                $('<i class="ti-arrow-down"></i>')
                                            )
                                    )
                            )
                    ).append(
                        $('<div class="form-group my-1"></div>')
                            .append(
                                $('<input type="text" class="form-control form-control-lg readonly-focus hidden" onchange="" ' +
                                    'aria-describedby="Titulo da Secão" placeholder="Titulo da Secão" id="'+id_secao+'" value="'+titulo+'"/>')
                                    .change((e)=>{$.changeSecaoTitulo({id:id,value:e.target.value})})
                            )
                    ).append(
                        $('<div class="form-group my-1"></div>')
                            .append(
                                $('<label class="t  ext-xs font-weight-bold text-gray-800 text-uppercase mb-1 hidden">Descrição</label>')
                            ).append(
                                $('<textarea class="form-control readonly-focus hidden" id="descricao" placeholder="Descrição" >'+(descricao !== 'undefined' && descricao != null?descricao:'')+'</textarea>')
                                    .change((e)=>{$.changeSecaoDescricao({id:id,value:e.target.value})})
                            )
                    )
            ).appendTo($('#main'))
        questoes.map((questao,i)=>{
            $.addPergunta(questao)
        })
    }
    $.addPergunta = function (questao){

        var {id,pergunta, tipoCampo} = questao
        //console.log(questao)
        let inicio =
            $('<div class="card card-body bg-white shadow mx-2 my-2 rounded"></div>')
                .appendTo('#main')

        var header =
            $('<div class="d-flex flex-row justify-content-between mb-1 pergunta"><span class="card-title my-auto">Pergunta</span></div>')
                .append(
                    $('<div class="bg-light rounded"></div>')
                        .append(
                            $('<button class="btn btn-outline-danger border-0 px-3 py-2"></button>')
                                .append(
                                    $('<i class="ti-trash"></i>')
                                )
                        )
                        .append(
                            $('<button class="btn btn-outline-info border-0 px-3 py-2"></button>')
                                .append(
                                    $('<i class="ti-arrow-up"></i>')
                                )
                        )
                        .append(
                            $('<button class="btn btn-outline-info border-0 px-3 py-2"></button>')
                                .append(
                                    $('<i class="ti-arrow-down"></i>')
                                )
                        )
                ).appendTo(inicio)


        var pergunta = $('<div class="form-group flex-row"></div>')
                            .append(
                                $('<input type="text" class="form-control hidden" aria-describedby="Pergunta" placeholder="Pergunta" value="'+pergunta+'"/>')
                            ).appendTo(inicio)

        var opcao = function (elem) {
                elem.append(
                    $('<div class="form-group flex-row hidden"></div>')
                        .append(
                            $('<button class="btn btn-primary"></button>')
                                .append(
                                    $('<i class="ti-plus"></i>')
                                )
                                .append(" Adicionar Opção")
                                .click(function () {
                                    $(this).parent().prev()
                                        .append(
                                            $('<div class="form-check form-check-inline w-100 my-2"></div>')
                                                .append(
                                                    $('<i class="far fa-circle mr-2  my-auto"></i>')
                                                )
                                                .append(
                                                    $('<input type="text" class="form-control hidden my-auto" aria-describedby="Opção" placeholder="Opção">')
                                                        .change((e)=>{
                                                            e.target.nextElementSibling.innerHTML = e.target.value
                                                        })
                                                )
                                        )
                                })
                        )
                )
                .append(
                    $('<div class="dropdown-divider"></div>')
                )
                .append(
                    $('<div class="d-md-flex flex-row justify-content-end hidden"></div>')
                        .append(
                            $('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append(
                                    $('<label class="switch my-auto mr-1"></label>')
                                        .append('<input type="checkbox">')
                                        .append('<span class="slider round"></span>')
                                )
                                .append('Lista Suspensa')
                        )
                        .append(
                            $('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append(
                                    $('<label class="switch my-auto mr-1"></label>')
                                        .append('<input type="checkbox">')
                                        .append('<span class="slider round"></span>')
                                )
                                .append('Multiplas resposta')
                        )
                        .append(
                            $('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append(
                                    $('<label class="switch my-auto mr-1"></label>')
                                        .append('<input type="checkbox">')
                                        .append('<span class="slider round"></span>')
                                )
                                .append('Obrigatória')
                        )
                )
        }
        var numero = function (elem) {
                elem.append(
                    $('<div class="form-group flex-row"></div>')
                        .append(
                                    $('<div class="form-control readonly bg-light">Número</div>')
                        )
                )
                .append(
                    $('<div class="dropdown-divider"></div>')
                )
                .append(
                    $('<div class="form-row"></div>')
                        .append(
                            $('<div class="form-group col-md-6"></div>')
                                .append(
                                    $('<label for="inputmin"></label>')
                                        .append('Min')
                                )
                                .append(
                                    $('<input type="number" step="0.5" class="form-control" name="inputmin" value="0">')
                                )
                        )
                        .append(
                                $('<div class="form-group col-md-6"></div>')
                                    .append(
                                        $('<label for="inputmax"></label>')
                                            .append('Max')
                                    )
                                    .append(
                                        $('<input type="number" step="0.5" class="form-control" name="inputmax" value="0">')
                                    )
                            )
                )
                .append(
                    $('<div class="d-md-flex flex-row justify-content-end"></div>')
                        .append(
                            $('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append(
                                    $('<label class="switch my-auto mr-1"></label>')
                                        .append('<input type="checkbox">')
                                        .append('<span class="slider round"></span>')
                                )
                                .append('Decimal')
                        )
                        .append(
                            $('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append(
                                    $('<label class="switch my-auto mr-1"></label>')
                                        .append('<input type="checkbox">')
                                        .append('<span class="slider round"></span>')
                                )
                                .append('Obrigatória')
                        )
                )
        }
        var texto = function(elem) {
                elem.append(
                    $('<div class="form-group flex-row"></div>')
                        .append(
                            $('<div class="form-control readonly bg-light">Resposta Texto</div>')
                        )
                )
                .append(
                    $('<div class="dropdown-divider"></div>')
                )
                .append(
                    $('<div class="d-md-flex flex-row justify-content-end"></div>')
                        .append(
                            $('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append(
                                    $('<label class="switch my-auto mr-1"></label>')
                                        .append('<input type="checkbox">')
                                        .append('<span class="slider round"></span>')
                                )
                                .append('Resposta Longo')
                        )
                        .append(
                            $('<div class="d-flex mx-2 my-1 my-md-0"></div>')
                                .append(
                                    $('<label class="switch my-auto mr-1"></label>')
                                        .append('<input type="checkbox">')
                                        .append('<span class="slider round"></span>')
                                )
                                .append('Obrigatória')
                        )
                )
        }
        switch (tipoCampo) {
            case 3:
                opcao(inicio);
                break;
            case 2:
                numero(inicio);
                break;
            case 1:
                texto(inicio);
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

    $.adicionarOpcaoClick = ((urlAdd)=>{})

    $('#adicionaritem .adicionar #add-pergunta-opcao').click(()=>{
         $.ajax({
            url: urlapi+'add/question/',
            type: 'POST',
            contentType: 'application/json',
            dataType: "json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            data:JSON.stringify({'tipo':'choices'}),
            success: function (secao) {
                GetQuestionario()
            },
            error: function (data) {

                GetQuestionario()
            }
        })
    })
    $('#adicionaritem .adicionar #add-pergunta-texto').click(()=>{
        $.ajax({
            url: urlapi+'add/question/',
            type: 'POST',
            contentType: 'application/json',
            dataType: "json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            data:JSON.stringify({'tipo':'text'
                                }
                ),
            success: function (secao) {
                GetQuestionario()
            },
            error: function (data) {

                GetQuestionario()
            }
        })
    })
    $('#adicionaritem .adicionar #add-pergunta-numero').click(()=>{
        $.ajax({
            url: urlapi+'add/question/',
            type: 'POST',
            contentType: 'application/json',
            dataType: "json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            data:JSON.stringify({'tipo':'number'
                                }
                ),
            success: function (secao) {
                GetQuestionario()
            },
            error: function (data) {

                GetQuestionario()
            }
        })
    })
    $('#adicionaritem .adicionar #add-secao').click(()=>{
        $.ajax({
            url: urlapi+'add/section',
            type: 'POST',
            contentType: 'application/json',
            dataType: "json",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            data:JSON.stringify({'message':'new section'}),
            success: function (secao) {
                GetQuestionario()
            },
            error: function (data) {
                console.log(data)
            }
        })
    })

    const GetQuestionario = function (){
        document.getElementById('main').innerHTML=''
        $.ajax({
            url: urlapi+'add/section',
            type: 'GET',
            contentType: 'application/json',
            dataType: "json",
            async: false,
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (res) {
                    res.map((secao,i)=>{
                        questionario.splice(0, questionario.length);
                        questionario.concat([secao])
                        $.addSecao(secao)
                    }
                )
            },
            error: function (data) {
                console.log(data)
            }
        })
    }
    GetQuestionario()


    $('.floating-label input').on('focus', function() { //Quando o foco é o input (for editar)
            $(this).parent('.floating-label').addClass('focused'); // Coloca o estilo da classe focused, na qual a label vai para cima do input(deixa de ser um 'placeholder')
        });
    $('.floating-label input').on('focusout', function() { //Quando o foco não é o input
            if ($(this).val().length === 0) { // Se o input estiver vazio, ele retira a classe 'focused' e a label volta a posição original como 'placeholder'
                $(this).parent('.floating-label').removeClass('focused');
            }
        });

})(jQuery)