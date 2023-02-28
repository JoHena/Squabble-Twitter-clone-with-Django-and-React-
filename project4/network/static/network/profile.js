window.onscroll = () => {
    if(window.innerHeight + window.scrollY >= document.body.offsetHeight){
        page_num = document.querySelector('.page-num')
        num_pages = document.querySelector('.num-pages').innerHTML
        if(between(page_num.innerHTML,1, num_pages -1)){
            page_num.innerHTML = parseInt(page_num.innerHTML) + 1
            load_new_posts(document.querySelector('.username').innerHTML)
        } 
    }
}

function load_new_posts(username) {
    const container = document.querySelector('.post-feed');
    const page = document.querySelector('.page-num').innerHTML

    fetch(`/posts/get/${username}/${page}`).then(response => response.json())
    .then(posts => {
        CreateFetchedPosts(posts.data, container)
    })
}