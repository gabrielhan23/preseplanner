var input = document.getElementById("wishlist");
input.addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  
  if (event.keyCode === 13 && document.getElementById("active-wish").value) {
    // Cancel the default action, if needed
    //event.preventDefault();
    document.getElementById("active-wish").removeAttribute('id')

    var input = document.createElement("input")
    var div = document.createElement("div")
    var br = document.createElement("br")

    input.id = "active-wish"
    input.className = "form-control form-control-lg wishInput"
    input.placeholder = "Enter gift idea"

    div.className = "wish"
    div.append(input)
    div.append(br)

    document.getElementById("wishlist").append(div)
    document.getElementById("active-wish").focus()
  }
});

function addWishList(){
  var wishList = document.getElementsByClassName("wishInput")
  var groupID = document.getElementById('groupID').innerHTML
  for(var x=0; x<wishList.length; x++){
    if(wishList[x].value){
      $.ajax({
        url: "addwish",
        data: {wishName: wishList[x].value, groupID: groupID},
        type: "POST",
        success: function(result){
        }
      });
    }
  }
  window.location.href = ("http://wishlist1.1234567890hihi.repl.co/group/"+document.getElementById('groupID').innerHTML)
}