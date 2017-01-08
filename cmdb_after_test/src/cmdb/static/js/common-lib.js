
function sortable(element){
	$(element).footable();
    $('.sort-column').click(function (e) {
        e.preventDefault();
        var footableSort = $(element).data('footable-sort');
        var index = $(this).data('index');
        footableSort.doSort(index, 'toggle');
    });
}

function robTab(element,evt){
	    //Roban's tab
    $(element+" > li ").each(function() {
            $(this).click(function() {
                var id = $(this).attr('id');
                $(this).addClass('active');
                $(this).siblings().removeClass("active");
                $("#" + id + '-content').fadeIn().siblings('div').hide();

                if(evt && evt[id]) {
                	evt[id]();
                }
           
            });
    });

}