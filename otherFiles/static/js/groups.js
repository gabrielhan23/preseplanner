$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})

function joinGroup(){
  var joinID = document.getElementById("join-id").value
  if(joinID){
    $.ajax({
      url: "joingroup",
      data: {joinID: joinID},
      type: "POST",
      success: function(result){
        $('#addGroup').modal('hide')
        window.location.href=("wishlist/"+result[1])
      }
    });
  }
}

function createGroup(){
  var createName = document.getElementById("create-name").value
  if(createName){
    $.ajax({
      url: "creategroup",
      data: {createName: createName},
      type: "POST",
      success: function(result){
        $('#addGroup').modal('hide')
        window.location.href=("wishlist/"+result)
      }
    });
  }
}

function openGroup(id){
  window.location.href=("group/"+id)
}

function deleteGroup(group){
  $.ajax({
    url: "delete",
    data: {group: group},
    type: "POST",
    success: function(result){
      document.getElementById(group).remove()
      window.location.href=("http://wishlist1.1234567890hihi.repl.co/groups")
    }
  });
}