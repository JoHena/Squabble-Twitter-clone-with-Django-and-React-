document.addEventListener('DOMContentLoaded', function() {
    const post_btn = document.querySelector('.post-btn')
    const follow_btn = document.querySelector('.follow-btn')
    const following_header = document.querySelector('.following-header')
    const buttonGroup = document.querySelector(".pages");

    if(following_header != null)
        load_following_posts()
    if(post_btn != null){
        document.querySelector('.post-btn').addEventListener('click', () => create_post())
        load_posts()
    }
    if(follow_btn != null){
        load_posts(document.querySelector('.username').innerHTML)
        document.querySelector('.follow-btn').addEventListener('click', () => follow_user())
    }
    if(buttonGroup != null)
        buttonGroup.addEventListener("click", buttonGroupPressed);
})

const buttonGroupPressed = e => { 
    const following_header = document.querySelector('.following-header')
    const task = e.target.dataset.task
    const max = document.querySelector('.num-pages').innerHTML
    const page = document.querySelector('.page-num')

    if(task === 'back') {
        num = parseInt(page.innerHTML) - 1
        if(between(num, 1, max) )
            page.innerHTML = num
    }
    if(task === 'next'){
        num = parseInt(page.innerHTML) + 1
        if(between(num, 0, max) )
            page.innerHTML = num
    }

    if(following_header != null)
        load_following_posts()
    else{
        load_posts()
    }
}

function create_post() {
    const body = document.querySelector('#post-content');
    const content = body.value;
    body.value = '';

    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            content: content,
        })
    })
    .then(response => response.json())
    .then(result => {
        load_posts()
    })
}

function follow_user() {
    let follow = document.querySelector('.username').innerHTML
    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify({
            follow: follow
        })
    })
    .then(response => response.json())
    .then(result => {
        location.reload();
    })
}

function load_posts(username) {
    const container = document.querySelector('.post-feed');
    const page = document.querySelector('.page-num').innerHTML
    const max = document.querySelector('.num-pages')
    container.innerHTML = '';

    if (typeof username !== 'undefined') {
        fetch(`/posts/get/${username}/${page}`).then(response => response.json())
        .then(posts => {
            max.innerHTML = posts.num_pages 
            CreateFetchedPosts(posts.data, container)
        })
    }
    else {
        let page = document.querySelector(".page-num").innerHTML
        fetch(`/posts/page/${page}`).then(response => response.json())
        .then(posts => {
            max.innerHTML = posts.num_pages 
            CreateFetchedPosts(posts.data, container)
        })
    }
}

function load_following_posts() {
    const container = document.querySelector('.post-feed');
    const page = document.querySelector('.page-num').innerHTML
    const max = document.querySelector('.num-pages')
    container.innerHTML = '';

    fetch(`/posts/get/follow/${page}`).then(response => response.json())
    .then(posts => {
        max.innerHTML = posts.num_pages
        CreateFetchedPosts(posts.data, container)
    })
}

function CreateFetchedPosts(posts, container) {
    for (post in posts) {
        let postcontainer = document.createElement('div')
        let likeCommentBox = document.createElement('div')
        postcontainer.setAttribute('class', 'post')
        postcontainer.innerHTML = `<a href = "/profile/${posts[post].username}" class = post-user><div>( ͡°👅 ͡°)</div><div>${posts[post].username}</div></a><div class = 'post-content'>${posts[post].content}</div><div class= 'post-info'><div><button class = "like-btn"><i class="fa-solid fa-heart"></i></button> ${posts[post].likes}</div><div></div>${posts[post].date}</div>`
        container.append(postcontainer)
    }
}

//Extra

function between(x, min, max) {
    return x >= min && x <= max;
  }
