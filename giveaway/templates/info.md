Status:
+ zmienne z kategoriami przekazane do js
- wykorzystać zmienne w kodzie
- naprawić odzysk danych poprzez użycie form.is_valid
- 



      $.ajax({
        data: {
            //serialize ??????
            quantity: $('input[name=bags]').val(),
            categories: JSON.stringify(institutionCats),
            organization: $('input[name=organization]:checked').parent().parent().attr("id"),
            address: $("input[name=address]").val(),
            city: $("input[name=city]").val(),
            postcode: $("input[name=postcode]").val(),
            phone: $("input[name=phone]").val(),
            data: $("input[name=data]").val(),
            time: $("input[name=time]").val(),
            more_info: $("textarea[name=more_info]").val(),
        }, // get the form data
        type: 'POST', // GET or POST
        url: "#",