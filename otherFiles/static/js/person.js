var groupID = document.getElementById("groupID").innerText
var userid = document.getElementById("userid").innerText
var input = document.getElementById("wishlist");
var done = true

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

function addGift(wishID, wishChecked, info, getID) {
  if(wishChecked){
    var node = document.createElement("div");
    var text = info; 
    var textnode=document.createTextNode(text);
    node.appendChild(textnode);
    node.className = "gift-body"
    document.getElementById("gifts").appendChild(node);
  }
  $.ajax({
  url: "addget",
  data: {getName: info, groupID: groupID, userid: userid, wishID: wishID, wishChecked: wishChecked, getID: getID},
  type: "POST",
  success: function(result){
    if(wishChecked){
      node.id= result+"-gets"
      if(wishID){
        document.getElementById(wishID+"-wish").className = result
        node.id= wishID+"-gets-wish"
      }
    } else {
      if(wishID){
        document.getElementById(wishID+"-wish").className = ""
        document.getElementById(wishID+"-gets-wish").remove()
      }
    }
    done=true
  }
});
}

function goBack(){
  window.history.back();
}

function addWishList(wishID){
  var wishList = document.getElementsByClassName("wishInput")
  $.ajax({
    url: "http://wishlist1.1234567890hihi.repl.co/wishlist/deletewish",
    data: {groupID: groupID},
    type: "POST",
    success: function(result){
      for(var x=0; x<wishList.length; x++){
        if(wishList[x].value){
          $.ajax({
            url: "http://wishlist1.1234567890hihi.repl.co/wishlist/addwish",
            data: {wishName: wishList[x].value, groupID: groupID},
            type: "POST",
            success: function(result){
              window.location.href = ("http://wishlist1.1234567890hihi.repl.co/group/"+groupID)
            }
          });
        }
      }
    }
  });
}

function getWish(wishID){
  if(done){
    done=false
  addGift(wishID, document.getElementById(wishID+"-wish").checked, document.getElementById(wishID+"-info").innerText, document.getElementById(wishID+"-wish").className)
  }
}

function buttonAddWish(){
  if(done && document.getElementById("gift").value != ""){
    done=false
    addGift(null, true, document.getElementById('gift').value)
    document.getElementById("gift").value = ""
  }
}