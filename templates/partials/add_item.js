

$(document).ready(function(event) {

                    // catch the form's submit event
                    $('#add_item{{produto.id}}').submit(function (event) {
                    event.preventDefault();
                var quantidade = document.getElementById("quantidade{{produto.id}}").value;
                var id_produto = document.getElementById("produto{{produto.id}}").value;


                $.ajax({
                    type: "POST",
                    url: "adicionar_item",
                    data: {
                        'csrfmiddlewaretoken': '{{ csrf_token }}',
                        'quantidade' : quantidade,
                        'id_produto' : id_produto,

                    },
                    success: function (data) {
                    $('#pedido_carrinho').html(data);
              },

                    error: function (data) {
                                // alert the error if any error occured
                                showalert((data.erro), "alert-danger");
                                alert(data.erro);
                                console.log(data.erro)
                            },

                }).done(function(event){
                    console.log("done")

                })
                .fail(function(event){
                    console.log('error')
                    console.log(e)
                })

            });
            function showalert(message, alerttype) {
            $('#alert_placeholder').append('<div id="alertdiv" class="alert ' +  alerttype + '" role="alert">' + message + '</div>');
            setTimeout(function() {
                $("#alertdiv").remove();
            }, 5000);
         }

            })







