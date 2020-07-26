
$(document).ready(function () {

    $("#banner-container div").first().addClass("active")
    let content = $("#banner-container").children();
    var i = 0;

    setInterval(() => {
        console.log(i)
        content.filter(".active").fadeOut(1000);
        setTimeout(() => {
            content.filter(".active").removeClass('active');
            content.eq(i).fadeIn(1000).addClass('active');
        }, 1000);
        i = (i + 1) % content.length; // Wraps around if it hits the end
    }, 7000);

    /* Limits the number of table rows 'shown' to 5.
    When Load More link is clicked, the limit is extended to show full table
    Link is hidden and Show Less link is shownn */
    total_tr = $("#categories tr").length;
    let limit = 5;
    $('#categories tr:lt(' + limit + ')').show();
    $('#loadMore').click(function () {
        // variablename = (condition) ? value1:value2
        limit = total_tr;
        $('#categories tr:lt(' + limit + ')').slideDown(300, "swing", function () {
            $('#showLess').show()
            $('#loadMore').hide()
        });
    });

    /* When Show Less link is clicked, limit is returned to value of 5
    Any table rows excluded from the first 5 rows in the table are hidden */
    $('#showLess').click(function () {
        limit = 5;
        $('#categories tr').not(':lt(' + limit + ')').slideUp(300, "swing", function () {
            $('#showLess').hide()
            $('#loadMore').show()
        });
    });
});


/* Whenever a checkbox is checked (input provided), the form is submiited */
$("form input").change(function () {
    $(this).closest('form').submit();
});



