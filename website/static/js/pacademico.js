$(document).ready(function () {
    $('#id_escuela').change(function() {
        var escuela = $(this).val();
        
        if (escuela) {
            $.ajax({
                url: "/carreras",
                data: { "escuela": escuela },
                dataType: "json",
                success: function (data) {
                    var carreraSelect = $("#id_carrera");
                    carreraSelect.empty();
                    carreraSelect.append('<option value="">Selecciona una carrera</option>');
                    $.each(data.carreras, function(index, carrera){
                        carreraSelect.append('<option value="'+ carrera.idPA +'">'+ carrera.nombre +'</option>');
                    });
                }
            })
        } else {
            $("#id_carrera").empty().append('<option value="">Selecciona una escuela primero</option>');
        }
    })
})