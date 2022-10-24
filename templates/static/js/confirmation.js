$(document).ready(function () {
	$( "#addBtn" ).click(function() {
    if($('#title').val() != null && $('#title').val() != ""){
        $('#confirmationMsg').html('Are you sure you want to add ('+$('#title').val()+') ?');
        $('#modal').modal('show');
      }else{
        //alert('enter a value in the textbox to submit');
        Swal.fire(
            'Good job!',
            'You clicked the button!',
            'success'
          ) 
      }
  });
  
  $('#confirmedBtn').click(function(){
    $('#modal').modal('hide');
    $( "#question_form" ).submit();
	});
  
});