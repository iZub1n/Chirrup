i='';
r=0;
l=0;
dl=0;
document.addEventListener('DOMContentLoaded', () => {
  
    editBtns = document.querySelectorAll('#editBtn')
    dBtns = document.querySelectorAll('#dBtn')
    likeBtns = document.querySelectorAll('#likeBtn')
    dislikeBtns = document.querySelectorAll('#dislikeBtn')

    


    for (const eb of editBtns){
        eb.addEventListener('click',function(event){
            getPost(eb)
            openEditBox(eb);
        })
    }

    for (const db of dBtns){
        db.addEventListener('click',function(event){
        //getPost(element)
           doneBtn(db);
        })
    }

    for (const lb of likeBtns){
        lb.addEventListener('click',function(event){
            getPost(lb)
            post= post.parentElement
            i = post.id
            r=1
        })
    }

    for (const dlb of dislikeBtns){
        dlb.addEventListener('click',function(event){
            getPost(dlb)
            post= post.parentElement
            i = post.id
            r=2
        })
    }


});

let post = null;
function getPost(element){
    post = element.parentElement;
    i = post.id
}


function openEditBox(element){
    post.querySelector('textarea').readOnly=false;
    post.style.backgroundColor = "black";
    post.querySelector("#dBtn").style.visibility = "visible";  
}

function doneBtn(element){
    post.style.backgroundColor = "gray";
    post.querySelector("#dBtn").style.visibility = "hidden";
    post.querySelector('textarea').readOnly=true;
}

$(document).on('submit', "#updateForm", function(e){
    e.preventDefault();
    $.ajax({
       type: 'POST',
       url: '/editPost',
       data: {
          content:(document.querySelector('#'+i)).querySelector('#content').querySelector('textarea').value,
          postID: i,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
       },

       success:function(){
           console.log('successful interaction ajax')
        }
    });
});



function updateReactions(l, dl){
    post.querySelector('#like').innerHTML=l;
    post.querySelector('#dislike').innerHTML=dl;
}

$(document).on('submit', "#reactionForm", function(e){
    e.preventDefault();
    $.ajax({
       type: 'POST',
       url: '/react',
       data: {
          postID: i,
          reaction: r,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
       },

       success:function(response){
           updateReactions(response.likes, response.dislikes)
        }
    });
});