$(function(){
    






    $("#signpg").hide()

    $(".signswitch").click(function(){
        $("#signpg").show()
        $("#logpg").hide()
        $(".signswitch").css("background-color", "green")
        $(".loginswitch").css("background-color", "white")
        $("#signpg").addClass("animate__animated animate__bounceIn")

       
    })

    $(".loginswitch").click(function(){
        $("#logpg").show()
        $("#signpg").hide()
        $(".loginswitch").css("background-color", "blue")
        $(".signswitch").css("background-color", "white")
        $("#logpg").addClass("animate__animated animate__bounceIn")

    })
    var $agreeCheckbox = $('#acceptcheckbox');
    var $submitButton = $('#submitbutton');
    function toggleButton() {
        if ($agreeCheckbox.prop('checked')) {
        $submitButton.prop('disabled', false);
        } else {
        $submitButton.prop('disabled', true);
        }
        }
        $agreeCheckbox.change(toggleButton);
     
        // Call toggleButton to set initial
        toggleButton();
   
        

     
})


$(function(){


    var $agreeCheckbox = $('#accept');
    var $submitButton = $('#submit');
    function toggleButton() {
        if ($agreeCheckbox.prop('checked')) {
        $submitButton.prop('disabled', false);
        } else {
        $submitButton.prop('disabled', true);
        }
        }
        $agreeCheckbox.change(toggleButton);
     
        // Call toggleButton to set initial
        toggleButton();
})


$(function(){
    $("form").hide()
        setTimeout(function(){
            $("#welcome").hide()
            $("form").show()
        }, 2000);


        $("#submitbutton").click(function(){
        var pass = document.getElementById("pass").value()
        var confirm =document.getElementById("confirm").value()
        var btn =document.getElementById("submitbutton");
        var check = document.getElementById("acceptcheckbox")
        if(pass == confirm){
            document.getElementById("para").innerHTML=""
        }else{
            document.getElementById("para").innerHTML="password does not match"
            btn.disabled= true;
            check.checked = false
        }
    })



})



var swiper = new Swiper('.swiper', {
    slidesPerView: 3,
    direction: getDirection(),
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    on: {
      resize: function () {
        swiper.changeDirection(getDirection());
      },
    },
  });

  function getDirection() {
    var windowWidth = window.innerWidth;
    var direction = window.innerWidth <= 760 ? 'vertical' : 'horizontal';

    return direction;
  }


$(function(){
var count = 0
var shoping = $("#cart1");

$('#butcount12').click(function(){
    for(var i = 0; i < 1; i++){
        count++;
     
    }
    shoping.text(count[i])
})

})





$(document).ready(function(){
    var clicked = localStorage.getItem('c')
    if (clicked === 'true'){
        $("a.ordersettings").addClass('bg-secondary')
    }

    $(".ordersettings").click(function(){
        $(this).addClass('bg-secondary')

        localStorage.setItem('ordersettingsAnchorClicked','true')
    
    })

    
    })
    



    $(function(){

        $("#cards").hide()
        $("#cards1").hide()
        $("#cards2").hide()
        $("#cards3").hide()
    
    
    let lastKnownScrollPosition = 0;
    let ticking = false;
    
    function doAnimation(scrollPos) {
      const el = document.getElementById("cards")
    
      if(window.scrollY > 1750){
        el.classList.add("animate__animated","animate__bounceInUp","animate__slow")
        $("#cards").show()
      }
      const el_div = document.getElementById("cards2")
      if(window.scrollY > 1912){
        el_div.classList.add("animate__animated","animate__bounceInLeft","animate__slow")
        $("#cards2").show()
      }
    
      const el_div1 = document.getElementById("cards1")
      if(window.scrollY > 560){
        el_div1.classList.add("animate__animated","animate__bounceInRight","animate__slow")
        $("#cards1").show()
      }
    
      const el_div3 = document.getElementById("cards3")
      if(window.scrollY > 2130){
        el_div3.classList.add("animate__animated","animate__fadeInUp","animate__slow")
        $("#cards3").show()
      }
    }
    
    document.addEventListener("scroll", (event) => {
      lastKnownScrollPosition = window.scrollY;
    
      if (!ticking) {
        window.requestAnimationFrame(() => {
          doAnimation(lastKnownScrollPosition);
          ticking = false;
        });
    
        ticking = true;
      }
    });
})


$(function(){
  var count=  0
  $("#addcart").click(function(){
    count= count + 1
   $(this).val('likes')
   
    
      

  })
})