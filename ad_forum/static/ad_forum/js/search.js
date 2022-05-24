$("#search_btn").click(function (){
    $.ajax({
    type: "GET",

    url: "check_search_bar",

    data: {
        'search_input': $("search_input").val(),
    },

    cache: false,

    success: function (data){
        if (data == 'director'){

        }
        else if (data == 'post'){

        }
    }
});
})

