;
$(document).ready(function(){
   $(':input[name=select_all]').each(function(){
    $(this).click(function(event) {
      var a = $(this).attr('data');
      var b = ":input[class=" + a +"]";
      if(this.checked) {
          $(b).each(function(){
              this.checked = true;
          });
      }else {
        $(b).each(function(){
              this.checked = false;
          });
         }
    });
  });
 });